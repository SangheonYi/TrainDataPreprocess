from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(__dir__) / '../util'))
from recog_valid_unicode import txt2valid_range

with open('sayi_dict.txt', 'r', encoding='utf-8') as sayi_dict:
    sayi_vocab = set([line[0] for line in sayi_dict.readlines()])

def append_label_list(coor, points, crop_list, gt_word, gt_list):
    left, upper, right, lower = coor
    if right - left < 3 or lower - upper < 3: # trash image condition
        return
    if not gt_word: # OOV unicode
        return
    points.append([[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]])
    crop_list.append(coor)
    gt_list.append(gt_word)
    return

def get_OOV(text):
    # global unuse_chars
    # unuse_chars
    # return be true when set(text) - sayi_vocab is empty set
    return set(text) - sayi_vocab

class PDFForTrainData():
    def __init__(self, pdf_name, pdf_path, crop_line_bool:bool, boxed_dir, cropped_dir) -> None:
        # pdf init
        self.pdf_name = pdf_name
        self.fp = open(pdf_path, 'rb')
        self.rsrcmgr = PDFResourceManager()
        self.laparams = LAParams()
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        self.pages = PDFPage.get_pages(self.fp, check_extractable=True)
        self.crop_line = crop_line_bool

        # pdf image directory
        self.boxed_dir = boxed_dir
        self.cropped_dir = cropped_dir
        if boxed_dir:
            os.makedirs(boxed_dir, exist_ok=True)
        os.makedirs(cropped_dir, exist_ok=True)

        # current page member
        self.current_page = None
        self.current_img = None
        self.current_page_num = 0

    def cal_coor(self, bbox):
        # image size에 맞게 bbox 비율 고려해야 함
        page_height = self.current_page.mediabox[-1]
        img_rate = self.current_img.height / page_height # img_heigh / page_height
        bbox = [coor * img_rate for coor in bbox]
        left, pdf_upper, right, pdf_lower = bbox

        # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
        # pdf는 사용자 관점 아래에서 위로 증가하는 y축
        # 이미지는 사용자 관점 위에서 아래로 증가하는 y축
        # 영점조절 (lower-left, upper-right) x축으로 대칭이동해야한다.
        upper = page_height * img_rate - pdf_lower
        lower = page_height * img_rate - pdf_upper
        margin = (lower - upper) * 0.025
        return [left - margin, upper, right + margin, lower] # korean doc fit

    def get_valid_lines_from_page(self):
        valid_lines = []
        self.interpreter.process_page(self.current_page)
        for lobj in self.device.get_result():
            if isinstance(lobj, LTTextBoxHorizontal) :
                for line in lobj:
                    if isinstance(line, LTTextLineHorizontal):
                        valid_lines.append(line)
        return valid_lines

    def set_crop_target(self, image_path):
        self.current_img = Image.open(image_path).convert("RGB")
        self.current_page = self.pages.__next__()
        self.current_page_num += 1
        if self.boxed_dir:
            self.draw_img = self.current_img.copy()
            self.page_draw = ImageDraw.Draw(self.draw_img)

    def save_draw(self, image_path):
        if self.boxed_dir:
            boxed_path = self.boxed_dir / Path(image_path).name
            self.draw_img.save(boxed_path, "JPEG")

    def draw_bboxes(self, text: str, rect_coords, box_color="dodgerblue", font_color="dodgerblue", line_width=2, draw_coord=False, bbox_only=True):
        if self.boxed_dir:
            for i, rect_coord in enumerate(rect_coords):
                int_bbox = [int(long_float) for long_float in rect_coord]
                self.page_draw.rectangle(int_bbox, outline=box_color, width=line_width)
                if not bbox_only:
                    text_to_draw = f'{int_bbox}' if draw_coord else text
                    self.page_draw.text(int_bbox, text_to_draw.strip(), font=ImageFont.truetype("font/Batang.ttf", size=20), fill=font_color)

    def parse_line(self, line):
        line_text = line.get_text().strip()
        while '  ' in line_text:
            line_text = line_text.replace('  ', ' ')
        line_text = txt2valid_range(line_text)
        return self.cal_coor(line.bbox), line_text
    
    def parse_labels(self, line:LTTextLineHorizontal):
        points = []
        crop_list = []
        invalid_line_chrs = set()
        label_text = []
        
        if self.crop_line:
            coor, gt_word = self.parse_line(line)
        else:
            gt_word = ''
            got_left = False
            left, upper, right, lower = 0, 0, 0, 0
            # data inspecting
            for ltchr in line:
                char = ltchr.get_text()
                char = txt2valid_range(char)
                # if char not in target_chr:
                if char == ' ' or char not in sayi_vocab: # both LTchr and LTAnno have get_text() and can be blank character
                    if got_left:
                        coor = [left, upper, right, lower]
                        invalid_line_chrs = invalid_line_chrs.union(get_OOV(gt_word))
                        append_label_list(coor, points, crop_list, gt_word, label_text)
                        gt_word = ''
                    got_left = False
                elif isinstance(ltchr, LTChar) :
                    space_coor = self.cal_coor(ltchr.bbox)
                    if not got_left:
                        left, upper, right, lower = space_coor
                        got_left = True
                    right = space_coor[2]
                    gt_word = f"{gt_word}{char}"
            coor = [left, upper, right, lower]
        invalid_line_chrs = invalid_line_chrs.union(get_OOV(gt_word))
        append_label_list(coor, points, crop_list, gt_word, label_text)
        return label_text, points, crop_list, invalid_line_chrs