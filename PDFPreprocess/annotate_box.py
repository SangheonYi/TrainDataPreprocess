from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from PIL import Image, ImageDraw, ImageFont
from pdf2jpg import pdf2jpg

file_name = 'jeong'
pdf_path = f"pdf/{file_name}.pdf"
color = "dodgerblue"

# pdf init
fp = open(pdf_path, 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp, check_extractable=True)

# convert pdf to jpg
page_width, page_height = list(pages)[0].mediabox[-2:]
img_rate = 2
print((page_width * img_rate, page_height * img_rate))
pdf2jpg(file_name, (page_width * img_rate, page_height * img_rate), mode="testt")
pages = PDFPage.get_pages(fp, check_extractable=True)

def cal_cor(bbox, page_height):
    # image size에 맞게 bbox 비율 고려해야 함
    # rate = image size/pdf page size
    # 좌표*rate ± 10 -> inset 부여
    left_diagon_rate = 0.995 * img_rate
    right_diagon_rate = 1.005 * img_rate
    left, top, right, bottom = bbox
    # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
    # 영점조절 (bottom-left, top-right)
    top = page_height - top
    bottom = page_height - bottom
    return left * left_diagon_rate, top * right_diagon_rate, \
    right * right_diagon_rate, bottom * left_diagon_rate
     # left, bottom, right, top

def draw_bbox(line, draw):
    text = line.get_text()
    left, bottom, right, top = cal_cor(line.bbox, page_height)
    scaled_bbox = ((left, bottom), (right, top))
    # print("text: ", text, "coor_orig: ", line.bbox, "new_orig: ", [[x0, new_y0], [x1, new_y1]])
    draw.rectangle(scaled_bbox, outline=color)
    draw.text(scaled_bbox[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return [left, top, right, bottom]

if 0:
    for i, page in enumerate(pages):
        page_name =f"{file_name}-{i}p"
        interpreter.process_page(page)
        # open img
        img = Image.open(f"output/{file_name}{i}.jpg").convert("RGB")
        draw = ImageDraw.Draw(img)
        for line in device.get_result():
            crop_bbox = draw_bbox(line, draw)
            img.crop(crop_bbox).save(f"cropped/{page_name}-{line.index}.jpg")
        img.save(f"output/{page_name}.jpg", "JPEG")
        break
