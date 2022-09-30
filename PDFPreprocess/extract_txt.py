# pip install pdfminer.six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
 
def convert_pdf_to_txt():
    #pdf리소스 매니저 객체 생성
    rsrcmgr = PDFResourceManager()
    #문자열 데이터를 파일처럼 처리하는 stringio -> pdf 파일 내용이 여기 담김
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    fp = open('1.pdf', 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
 
    for page in PDFPage.get_pages(fp, [], check_extractable=True):
        interpreter.process_page(page)
    #text에 결과가 담김
    text = retstr.getvalue()
 
    fp.close()
    device.close()
    retstr.close()
    return text
 
v = convert_pdf_to_txt()
print(v)
# 2nd
from pdfminer.high_level import extract_text

text = extract_text('1.pdf')
print(text + '🎈')
