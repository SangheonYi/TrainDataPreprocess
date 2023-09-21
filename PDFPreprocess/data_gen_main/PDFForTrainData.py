from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from multiprocessing import Queue
import os
import sys
import fitz  # PyMuPDF

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(__dir__) / '../util'))
from recog_valid_unicode import txt2valid_range
from OCRLabels import OCRLabels

with open('sayi_dict.txt', 'r', encoding='utf-8') as sayi_dict:
    sayi_vocab = set([line[0] for line in sayi_dict.readlines()])

def append_label_list(coor, points, crop_list, gt_word, gt_list):
    left, upper, right, lower = coor
    if right - left < 1 or lower - upper < 1: # trash image condition
        return
    if not gt_word: # OOV unicode
        return
    # opencv poly bbox style use in detection
    points.append([[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]])
    # hocr style use for crop
    crop_list.append(coor)
    gt_list.append(gt_word)

class PDFForTrainData():
    def __init__(self, pdf_name, pdf_path, crop_line_bool:bool, boxed_dir, cropped_dir, img_q: Queue, dpi) -> None:
        # pdf init
        self.pdf_name = pdf_name
        self.crop_line = crop_line_bool
        self.pdf_document = fitz.open(pdf_path)
        self.scale = dpi / 72
        self.current_img = None

        # pdf image directory
        self.boxed_dir = boxed_dir
        self.cropped_dir = cropped_dir

        # ocr data
        self.invalid_chr_set = set()
        self.ocr_labels = OCRLabels()
        self.img_q = img_q

    def set_crop_target(self, image_path):
        self.current_img = Image.open(image_path).convert("RGB")
        if self.boxed_dir:
            self.draw_img = self.current_img.copy()
            self.page_draw = ImageDraw.Draw(self.draw_img)

    def save_draw(self, image_path):
        if self.boxed_dir:
            os.makedirs(self.boxed_dir, exist_ok=True)
            boxed_path = self.boxed_dir / Path(image_path).name
            self.draw_img.save(boxed_path, "JPEG")

    def draw_bboxes(self, text: str, rect_coords, box_color="dodgerblue", font_color="dodgerblue", line_width=2, draw_coord=False, bbox_only=True):
        if self.boxed_dir:
            for i, rect_coord in enumerate(rect_coords):
                int_bbox = [int(long_float) for long_float in rect_coord]
                self.page_draw.rectangle(int_bbox, outline=box_color, width=line_width)
                if not bbox_only:
                    text_to_draw = f'{int_bbox}' if draw_coord else text
                    self.page_draw.text((int_bbox[0], int_bbox[1] + 10), text_to_draw.strip(), font=ImageFont.truetype("font/Batang.ttf", size=20), fill=font_color)
    
    def parse_labels(self, page_idx):
        points = []
        crop_list = []
        label_text = []
        current_page = self.pdf_document[page_idx].get_textpage()
        if self.crop_line:
            # TODO parse line object
            current_page.extractDICT()
        else:
            for word in current_page.extractWORDS():
                word_gt = txt2valid_range(word[4])
                coord = [e * self.scale for e in word[:4]]
                coord[1] -= 2
                invalid_chars = set(word_gt) - sayi_vocab
                if invalid_chars:
                    self.invalid_chr_set |= invalid_chars
                    self.draw_bboxes(word_gt, [coord], box_color='orange', font_color="red", bbox_only=False)
                else:
                    append_label_list(coord, points, crop_list, word_gt, label_text)
        return label_text, points, crop_list