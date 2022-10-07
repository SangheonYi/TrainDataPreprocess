from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

class PDFForTrainData():
    def __init__(self, pdf_path) -> None:
        # pdf init
        self.fp = open(pdf_path, 'rb')
        self.rsrcmgr = PDFResourceManager()
        self.laparams = LAParams()
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        self.pages = PDFPage.get_pages(self.fp, check_extractable=True)
        self.page = next(self.pages)
        self.page_width, self.page_height = self.page.mediabox[-2:]

    def cal_coor(self, bbox, img_rate):
        # image size에 맞게 bbox 비율 고려해야 함
        left, lower, right, upper = bbox
        # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
        # 영점조절 (lower-left, upper-right)
        upper = self.page_height - upper
        lower = self.page_height - lower
        margin = (lower - upper) * 0.1 * img_rate
        print(margin)
        return left - margin, \
        upper - (margin) * 2, \
        right + margin, lower + margin
        # left, lower, right, top
    
    def next_page(self):
        self.page = next(self.pages)
