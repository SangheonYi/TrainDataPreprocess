from pdfminer.high_level import extract_pages
for page_layout in extract_pages("DCN.pdf"):
    for element in page_layout:
        print(element)