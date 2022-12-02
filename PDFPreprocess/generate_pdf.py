#-*- coding: utf-8 -*- 
# doc.py
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from itertools import product
from util.util import create_directories
from multiprocessing import Pool
from os import cpu_count
import os
from tqdm import tqdm 
from pathlib import Path

# return splited corpus list by split size(50) lines  
def get_corpus_list(file, corpus_count):
    # 50 split_size is fastest size to generate pdf
    split_size = 50
    # get corpus_count length split_size size corpus list

    # kor_tech
    # 50 split_size -> 9KB raw text
    # 9KB generate 3.2MB pdfs with 6 different fonts, 5 different sizes. these pdf generate 4K GT
    # -> 9KB, 1font generate 0.53MB
    with open(file, 'r', encoding='utf-8') as raw_text_file:
        total_corpus = raw_text_file.readlines()
        return [''.join(total_corpus[idx * split_size:(idx + 1) * split_size]) for idx in range(corpus_count)]

def make_doc_path(pdf_dir, font_name, font_size, corpus_name, corpus_idx):
    extend = '.ttf' if '.ttf' in font_name else '.otf'
    pdf_file_name = font_name.replace(extend, f"_{font_size}_{corpus_name}_{corpus_idx}.pdf")
    return f"{pdf_dir}/{pdf_file_name}"

def generate_pdf(text, font_path, font_size, doc_path):
    if Path(font_path).exists():
        font = TTFont("HCR Batang", font_path)
    else:
        print(f"{font_path} font not found")
        return

    pdfmetrics.registerFont(font)
    styles = getSampleStyleSheet()
    leading = round(font_size * 1.2)
    if leading % 2 == 1:
        leading += 1
    styles.add(ParagraphStyle(name="Hangul", fontName="HCR Batang", fontSize=font_size, leading=leading))

    story = []
    story.append(Paragraph(text, style=styles["Hangul"]))
    doc = SimpleDocTemplate(doc_path, pagesize=A4)
    doc.build(story)
    # print(f'corpus_pdf/{doc_name}')
    # print(f'build spent {time.time() - start}')

def batch_convert_co2pdf(pool_count, corpus, font_name_size_product:product, directories={
        'pdf_dir': 'corpus_pdf',
        'font_dir': 'font'
    }):
    # pool_count = 8
    pool = Pool(pool_count)
    for font_name, font_size in font_name_size_product:
        font_path = f"{directories['font_dir']}/{font_name}"
        doc_path = make_doc_path(directories['pdf_dir'], font_name, font_size, corpus['name'], corpus['idx'])
        if not Path(doc_path).exists():
            pool.apply_async(generate_pdf, args=(corpus['text'], font_path, font_size, doc_path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    font_sizes = [8, 10, 14, 20, 24]
    font_sizes = [8]
    font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]
    font_names = ['human_myoungjo.ttf']
    corpus_name = 'kor_tech'
    corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', 1)
    pool_count = cpu_count()
    directories = {
        'pdf_dir': 'corpus_pdf',
        'font_dir': 'font'
    }
    create_directories(directories.values())
    generate_pdf("hello 안녕 세계 world", 'font/human_myoungjo.ttf', 8, 'corpus_pdf/test.pdf')
    # for corpus_idx, text in tqdm(enumerate(corpus_list), total=len(corpus_list)):
    #     corpus = {
    #         'idx': corpus_idx,
    #         'text': text,
    #         'name': corpus_name
    #     }
    #     batch_convert_co2pdf(pool_count, corpus, product(font_names, font_sizes), directories=directories)
