from pdfminer.layout import LAParams, LTTextLineHorizontal, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pdf2jpg import pdf2jpg

filename = 'test.pdf'
color = "dodgerblue"

# pdf init
fp = open('pdf/' + filename, 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp, check_extractable=True)

# open img
img = Image.open("output/test0.jpg").convert("RGB")
draw = ImageDraw.Draw(img)
    # image size에 맞게 bbox 비율 고려해야 함
    # rate = image size/pdf page size
    # 좌표*rate ± 10 -> inset 부여
# convert pdf to jpg
page_width, page_height = list(pages)[0].mediabox[-2:]
img_rate = 2
print((page_width * img_rate, page_height * img_rate))
pdf2jpg(filename, (page_width * img_rate, page_height * img_rate))
pages = PDFPage.get_pages(fp, check_extractable=True)

def cal_cor(bbox, page_height):
    left_diagon_rate = 0.995 * img_rate
    right_diagon_rate = 1.005 * img_rate
    left, top, right, bottom = bbox
    top = page_height - top
    bottom = page_height - bottom
    return ((left * left_diagon_rate, top * right_diagon_rate),
     (right * right_diagon_rate, bottom * left_diagon_rate))
     # left, bottom, right, top

for page in pages:
    # print(dir(page))
    # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
    interpreter.process_page(page)
    for lobj in device.get_result():
        if isinstance(lobj, LTTextBoxHorizontal):
            for line in lobj:
                if isinstance(line, LTTextLineHorizontal):
                    text = line.get_text()
                    # 영점조절 (bottom-left, top-right)
                    scaled_bbox = cal_cor(line.bbox, page_height)
                    # print("text: ", text, "coor_orig: ", line.bbox, "new_orig: ", [[x0, new_y0], [x1, new_y1]])
                    draw.rectangle(scaled_bbox, outline=color)
                    draw.text(scaled_bbox[0], text, font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    break
img.save("output/highlighted.jpg", "JPEG")
