#-*- coding: utf-8 -*- 
# doc.py
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from itertools import product
from util.util import get_file_list, create_directory
from multiprocessing import Pool
from os import cpu_count
from tqdm import tqdm 
import time

def get_corpus_list(file, list_len, split_size):
    # 50 split_size(fastest size to generate pdf)

    # kor_tech
    # 50 split_size -> 9KB raw text
    # 9KB generate 3.2MB pdfs with 6 different fonts, 5 different sizes
    # -> 9KB, 1font generate 0.53MB
    with open(file, 'r', encoding='utf-8') as raw_text_file:
        total_corpus = raw_text_file.readlines()
        return [''.join(total_corpus[idx * split_size:(idx + 1) * split_size]) for idx in range(list_len)]

def font_path_to_doc_name(font_name, font_size, corpus_name):
    global reapeat_idx
    extend = '.ttf' if '.ttf' in font_name else '.otf'
    return font_name.replace(extend, f"_{font_size}_{corpus_name}_{reapeat_idx}.pdf")

def generate_pdf(text, font_name, font_size, corpus_name):
    font = TTFont("HCR Batang", f"font/{font_name}")
    pdfmetrics.registerFont(font)

    styles = getSampleStyleSheet()
    leading = round(font_size * 1.2)
    if leading % 2 == 1:
        leading += 1
    styles.add(ParagraphStyle(name="Hangul", fontName="HCR Batang", fontSize=font_size, leading=leading))

    story = []
    story.append(Paragraph(text, style=styles["Hangul"]))
    doc_name = font_path_to_doc_name(font_name, font_size, corpus_name)
    doc = SimpleDocTemplate(f'corpus_pdf/{doc_name}', pagesize=A4)
    doc.build(story)
    # print(f'corpus_pdf/{doc_name}')
    # print(f'build spent {time.time() - start}')

def batch_convert(pool_count, corpus, corpus_name):
    # pool_count = 8
    pool = Pool(pool_count)
    for font_name, font_size in product(font_names, font_sizes):
        pool.apply_async(generate_pdf, args=(corpus, font_name, font_size, corpus_name))
    pool.close()
    pool.join()

reapeat_idx = 0
font_sizes = [8, 10, 14, 20, 24]
# font_sizes = [8, 20]
font_names = ['NanumMyeongjoExtraBold.ttf', 'Dotum.ttf', 'hy_headline_m.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', ]
# font_names = ['Batang.ttf']
corpus_name = 'kor_tech'
corpus_list = get_corpus_list(f'corpus/{corpus_name}.txt', 1, 50)
pool_count = cpu_count()
create_directory('corpus_pdf')

for idx, corpus in tqdm(enumerate(corpus_list), total=len(corpus_list)):
    reapeat_idx = idx
    batch_convert(pool_count, corpus, corpus_name)
