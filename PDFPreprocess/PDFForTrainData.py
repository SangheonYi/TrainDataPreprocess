from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

class PDFForTrainData():
    def __init__(self, pdf_path, img_rate) -> None:
        # pdf init
        self.fp = open(pdf_path, 'rb')
        self.rsrcmgr = PDFResourceManager()
        self.laparams = LAParams()
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)
        self.pages = PDFPage.get_pages(self.fp, check_extractable=True)
        meta_page = next(PDFPage.get_pages(self.fp, check_extractable=True, maxpages=1))
        self.page_width, self.page_height = meta_page.mediabox[-2:]
        self.img_rate = img_rate

    def cal_coor(self, bbox, img_rate):
        # image size에 맞게 bbox 비율 고려해야 함
        left, lower, right, upper = bbox
        print(f"bf left: {left}, lower: {lower}, right: {right}, upper: {upper}")
        bbox = [coor * img_rate for coor in bbox]
        left, lower, right, upper = bbox
        print(f"af left: {left}, lower: {lower}, right: {right}, upper: {upper}")
        # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
        # 영점조절 (lower-left, upper-right)
        upper = self.page_height - upper
        lower = self.page_height - lower
        margin = (lower - upper) * 0.1 * self.img_rate

        return [left , upper , right , lower ]
        return [left - margin, upper - (margin) * 2, right + margin, lower + margin]
        # left, lower, right, top