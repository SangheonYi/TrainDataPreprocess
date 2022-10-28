from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LAParams, LTTextBox, LTLine, LTTextContainer, LTChar, LTTextLineHorizontal, LTTextBoxHorizontal, LTFigure, LTImage
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.high_level import extract_pages

fp = open(PDF_PATH, 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

pages = PDFPage.get_pages(fp, check_extractable=True)

for page in pages:
    
    # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단

    page_height = page.mediabox[3]
    interpreter.process_page(page)
    layout = device.get_result()

    images = []
    textlines = []
    for lobj in layout:
        if isinstance(lobj, LTTextBoxHorizontal):
            for line in lobj:
                if isinstance(line, LTTextLineHorizontal):
                    text = line.get_text()
                    # 영점조절 (bottom-left, top-right)
                    x0, y0, x1, y1 = line.bbox # (bottoom left, top right)
                    new_y0 = page_height-y0
                    new_y1 = page_height-y1
                    # print("text: ", text, "coor_orig: ", line.bbox, "new_orig: ", [[x0, new_y0], [x1, new_y1]])