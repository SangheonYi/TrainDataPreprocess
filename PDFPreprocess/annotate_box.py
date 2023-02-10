from PIL import Image, ImageDraw
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, LTAnno
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tqdm import tqdm
from util.util import create_directories, create_directory, get_file_list, is_valid_rec_list
from multiprocessing import Pool
import os
from pathlib import Path
import json
from recog_valid_unicode import *

with open('sayi_dict.txt', 'r', encoding='utf-8') as sayi_dict:
    sayi_vocab = set([line[0] for line in sayi_dict.readlines()])
excluded_chr_set = set()

def draw_bbox(line, draw, rect_coord):
    # text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    # draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def get_OOV(text):
    # global unuse_chars
    # unuse_chars
    # return be true when set(text) - sayi_vocab is empty set
    oov_set = list(set(text) - sayi_vocab)
    return oov_set

def append_label_list(coor, points, crop_list, gt_word, gt_list):
    invalid_chr_set = set()
    left, upper, right, lower = coor
    if right - left < 3 or lower - upper < 3: # trash image condition
        return invalid_chr_set
    oov_set = get_OOV(gt_word)
    invalid_chr_set = invalid_chr_set.union(oov_set)
    if oov_set or not gt_word: # OOV unicode 
        return invalid_chr_set
    points.append([[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]])
    crop_list.append(coor)
    gt_list.append(gt_word)
    return invalid_chr_set

def parse_labels(crop_line, line, pdf:PDFForTrainData, img_rate):
    points = []
    crop_list = []
    # print(line.bbox, img_rate)
    coor = pdf.cal_coor(line.bbox, img_rate)
    line_text = line.get_text().strip()
    while '  ' in line_text:
        line_text = line_text.replace('  ', ' ')
    line_text = txt2valid_range(line_text)
    if crop_line:
        label_text = [line_text]
    else:
        label_text = []
        gt_word = ''
        got_left = False
        left, upper, right, lower = coor
        # data inspecting
        for ltchr in line:
            char = ltchr.get_text()
            # if char not in target_chr:
            if char == ' ' or char not in sayi_vocab: # both LTchr and LTAnno have get_text() and can be blank character
                if got_left:
                    coor = [left, upper, right, lower]
                    invalid_chr_set = append_label_list(coor, points, crop_list, gt_word, label_text)
                    gt_word = ''
                got_left = False
            elif isinstance(ltchr, LTChar) :
                space_coor = pdf.cal_coor(ltchr.bbox, img_rate)
                if not got_left:
                    left = space_coor[0]
                    got_left = True
                right = space_coor[2]
                gt_word = f"{gt_word}{char}"
        coor = [left, upper, right, lower]
        # print(label_text, crop_list)
    invalid_chr_set = append_label_list(coor, points, crop_list, gt_word, label_text)
    return label_text, points, crop_list, invalid_chr_set

def crop_pdf_images(
    zipped_arg=None,
    pdf_name=None,
    pdf=None,
    directories={
        'boxed_dir': None,
        'cropped_dir': 'cropped'
    },
    total=0,
    crop_line=False
):
    invalid_chr_set = set()
    cropped_labels = []
    det_labels = []
    if directories['boxed_dir']:
        boxed_dir = Path(directories['boxed_dir']) / pdf_name
    else:
        boxed_dir = None
    cropped_dir= Path(directories['cropped_dir']) / pdf_name
    create_directory(boxed_dir)
    create_directory(cropped_dir)
    for page, image_path, page_num in tqdm(zipped_arg, total=total):
        page_det_labels = []
        # open img
        img = Image.open(image_path).convert("RGB")
        # draw bbox feature is commented
        if boxed_dir:
            draw_img = img.copy()
            draw = ImageDraw.Draw(draw_img)
        img_rate = img.height / page.mediabox[-1] # img_heigh / page_height
        crop_idx = 0
        for lobj in pdf.get_pdf_aggregator_result(page):
            if isinstance(lobj, LTTextBoxHorizontal) :
                for line in lobj:
                    if isinstance(line, LTTextLineHorizontal):
                        label_text, points, crop_list, invalid_chr_set = parse_labels(crop_line, line, pdf, img_rate)
                        for text, bbox_label, crop_coor in zip(label_text, points, crop_list):
                            left, upper, right, lower = crop_coor
                            cropped_path = cropped_dir / f'{page_num}_{crop_idx}_.png'
                            # cropped_path = f'/home/sayi/workspace/OCR/PaddleOCR/sayi/resource/pdf_dataset/{pdf_id}_{page_num}_{crop_idx}_.png'
                            # print(f"{cropped_path}\t{text}")
                            img.crop(crop_coor).save(cropped_path)
                            cropped_labels.append(f'{cropped_path}\t{text}\n')
                            page_det_labels.append({"transcription": text, "points": bbox_label})
                            if boxed_dir:
                                draw_bbox(line, draw, ((left, lower), (right, upper)))
                            crop_idx += 1
        det_labels.append(f"{image_path}\t{json.dumps(page_det_labels, ensure_ascii=False)}\n")
        if boxed_dir:
            boxed_path = boxed_dir / Path(image_path).name
            draw_img.save(boxed_path, "JPEG")
        img.close()
    # write_label(directories['label_dir'], cropped_labels, f'rec_{pdf_name}')
    # write_label(directories['label_dir'], det_labels, f'det_{pdf_name}')
    return ''.join(det_labels), ''.join(cropped_labels), invalid_chr_set

def convert_and_crop_pdf_images(directories, pdf2img_option, pdf_name,
    pdf2image_bool=True, 
    crop_line_bool=False,
    ):
    pdf_path = f"{directories['pdf_dir']}/{pdf_name}.pdf"
    pdf = PDFForTrainData(pdf_path)
    converted_dir = Path(directories['pdf_converted_dir']) / pdf_name

    pdf2img_option["output_file"] = pdf_name
    pdf2img_option["output_folder"] = converted_dir
    # pdf2img_option["size"] = (None, pdf.page_height * img_rate) # preserve aspect ratio with pdf.page_height * img_rate pixels height
    converted_list = get_file_list(converted_dir)
    if pdf2image_bool:
        create_directory(converted_dir)
        converted_list = convert_from_path(pdf_path, **pdf2img_option)
    else:
        converted_list.sort()
    images_size = len(converted_list)
    crop_arg = {
        "pdf_name": pdf_name,
        "pdf": pdf,
        "directories": directories,
        "crop_line": crop_line_bool,
        "total": images_size,
        "zipped_arg": zip(pdf.pages, converted_list, range(images_size)),
    }
    # print('cropping')
    det_label, rec_label, invalid_chr_set = crop_pdf_images(**crop_arg)
    print(f'{pdf_name}.pdf done')
    return det_label, rec_label, invalid_chr_set

def batch_convert_pdf2crop(pool_count, pdf_names, pdf2img_option, 
    conv_and_crop_opt={
        'pdf2image_bool':False, 
        'crop_line_bool':False,
    },
    directories = {
        'pdf_converted_dir' : 'converted', 
        'boxed_dir' : None, 
        'cropped_dir' : 'cropped', 
        'label_dir' : 'labels',
        'pdf_dir' : 'corpus_pdf'
    }):
    pool = Pool(pool_count)
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(directories, pdf2img_option, pdf_name), kwds=conv_and_crop_opt) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    rec_label_list = []
    det_label_list = []
    global excluded_chr_set
    for pdf_name in pdf_names:
        det_label, rec_label, invalid_chr_set = results[pdf_name].get()
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
        excluded_chr_set = excluded_chr_set.union(invalid_chr_set)
    return ''.join(det_label_list), ''.join(rec_label_list)

def write_label(label_dir, label_list, label_name):
    label = ''.join(label_list)
    label_path = f'{label_dir}/{label_name}.txt'
    with open(label_path, 'w', encoding='utf-8') as label_file:
        label_file.write(label)


if __name__ == '__main__':
    pool_count = os.cpu_count()
    # pool_count = 8
    # pdf_names += [f'wind{pdf_index}' for pdf_index in range(10)]
    directories = {
        'pdf_converted_dir' : 'converted', 
        # 'boxed_dir' : 'boxed', # if None not save boxed image
        'boxed_dir' : 'pdf/issue/boxed', # if None not save boxed image
        # 'boxed_dir' : '/mnt/c/Exception/', # if None not save boxed image
        # 'cropped_dir' : 'cropped', 
        'cropped_dir' : 'pdf/issue/cropped', 
        # 'cropped_dir' : '/mnt/d/cropped', 
        'label_dir': 'labels',
        # 'pdf_dir': 'pdf/crawled',
        # 'pdf_dir': 'pdf/selenium_alert_handled',
        # 'pdf_dir': 'pdf/issue',
        'pdf_dir': 'pdf/issue/중간에 종횡비 바뀜',
    }
    create_directories(directories.values())

    # font, size pdf
    pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
    for corpus_pdf_path in get_file_list(directories['pdf_dir'])]
    print('pdf length', len(pdf_names))
    pdf_names.sort()
    det_label_list = []
    rec_label_list = []
    step = pool_count * 2

    pdf2img_option = {
        "fmt": "png",
        # "single_file": True,
        "paths_only": True,
        "use_pdftocairo": False,
        "timeout": 1200, 
        "thread_count": 4,
        # "last_page" : 1,
    }
    conv_and_crop_opt={
        'pdf2image_bool':True, 
        'crop_line_bool':False,
        # 1654 x 2339 200dpi
    }
    
    for pdf_idx in range(0, len(pdf_names), step):
        det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], pdf2img_option, conv_and_crop_opt=conv_and_crop_opt, directories=directories)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    write_label(directories['label_dir'], rec_label_list, 'rec_banila_train')
    write_label(directories['label_dir'], det_label_list, 'det_train')
    is_valid_rec_list(f"{directories['label_dir']}/rec_banila_train.txt")
    print("all pdf converted")
    print("excluded_chr_set:", sorted(excluded_chr_set))