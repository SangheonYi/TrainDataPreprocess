from pathlib import Path

crawled_dir = Path('/home/sayi/workspace/OCR/TrainDataPreprocess/PDFPreprocess/pdf/crawled')
crawled_pdfs = set(pdf_path.stem for pdf_path in crawled_dir.iterdir())
with open('inf_res.log', 'r', encoding='utf-8') as red_log:
    parsed_list = list(set([line[:-1].split('path: ')[-1].split('/')[1] for line in red_log.readlines() if 'path: cropped/' in line]))
    parsed_list.sort()
    for file in parsed_list:
        if file in crawled_pdfs:
            print(f"\"{file}\",")