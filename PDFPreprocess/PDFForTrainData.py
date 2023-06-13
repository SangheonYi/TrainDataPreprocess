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
        self.current_page = None

    def cal_coor(self, bbox, img_rate):
        # image size에 맞게 bbox 비율 고려해야 함
        bbox = [coor * img_rate for coor in bbox]
        left, lower, right, upper = bbox
        # pdf의 영점은 좌측 하단 != 이미지의 영점은 좌측 상단
        # pdf는 사용자 관점 아래에서 위로 증가하는 y축
        # 이미지는 사용자 관점 위에서 아래로 증가하는 y축
        # 영점조절 (lower-left, upper-right)
        page_height = self.current_page.mediabox[-1]
        upper = page_height * img_rate - upper
        lower = page_height * img_rate - lower
        margin = (lower - upper) * 0.025
        # return [left - margin, upper - margin , right + margin, lower + margin * 2] # korean doc fit
        return [left - margin, upper + margin * 6, right + margin, lower - margin] # eng paper fit
        # left, lower, right, top

    def get_pdf_aggregator_result(self, page):
        self.current_page = page
        self.interpreter.process_page(page)
        return self.device.get_result()