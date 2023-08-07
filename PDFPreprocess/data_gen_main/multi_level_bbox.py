from PDFForTrainData import PDFForTrainData
from merge_bbox import merge_section_bbox
from util import get_file_list, is_valid_rec_list, write_label, to_train_path
from option_args import parse_args, get_pdf2img_option
from OCRLabels import OCRLabels
from OCRUnicodeRange import *
from DataCollector import DataCollector

from pdf2image import convert_from_path
from multiprocessing import Pool, Manager, Queue
from pathlib import Path
from itertools import product
from tqdm import tqdm
import random
import time
import json
import os

def crop_from_page(args, pdf:PDFForTrainData):
    crop_idx = 0
    word_bbox_list = []
    page_det_labels = []

    for line in pdf.get_valid_lines_from_page():
        label_text, points, crop_list = pdf.parse_labels(line)
        word_bbox_list += crop_list
        pdf.draw_bboxes("word box", crop_list, draw_coord=True, bbox_only=True, box_color='grey', line_width=1)
        for text, bbox_label, crop_coor in zip(label_text, points, crop_list):
            cropped_path = pdf.cropped_dir / f'{pdf.current_page_num}_{crop_idx}_.png'
            crop_img = pdf.current_img.crop(crop_coor)
            if args.crop_image_save:
                crop_img.save(cropped_path)
            pdf.img_q.put((crop_img, to_train_path(cropped_path)))
            pdf.ocr_labels.rec_label_list.append(f'{to_train_path(cropped_path)}\t{text}\n')
            page_det_labels.append({"transcription": text, "points": bbox_label})
            crop_idx += 1
    return word_bbox_list, page_det_labels

def crop_pdf_images(args, pdf: PDFForTrainData, converted_list):
    for image_path in tqdm(converted_list, total=len(converted_list)):
        # open img
        pdf.set_crop_target(image_path)
        # draw bbox feature is commented
        word_bbox_list, det_labels = crop_from_page(args, pdf)
        det_label = f"{to_train_path(image_path)}\t{json.dumps(det_labels, ensure_ascii=False)}\n"
        # merge section label
        det_section_labels = merge_section_bbox(pdf, word_bbox_list)
        det_section_label = f"{to_train_path(image_path)}\t{json.dumps(det_section_labels, ensure_ascii=False)}\n"
        pdf.ocr_labels.append_det_label(det_label, det_section_label)
        # pdf.save_draw(image_path)
    # write_label(args.label_dir, pdf.ocr_labels.cropped_labels, f'rec_{pdf_name}')
    # write_label(args.label_dir, pdf.ocr_labels.det_labels, f'det_{pdf_name}')

    # section label
    # write_label(args.label_dir, pdf.ocr_labels.det_labels, f'det_{pdf_name}')
    return pdf.ocr_labels, pdf.invalid_chr_set

def convert_pdf2img(args, pdf_name, pdf_path):
    converted_dir = Path(args.pdf_converted_dir) / pdf_name
    if args.pdf2image_bool:
        pdf2img_option = get_pdf2img_option(args)
        pdf2img_option["output_file"] = pdf_name
        pdf2img_option["output_folder"] = str(converted_dir)
        os.makedirs(pdf2img_option["output_folder"], exist_ok=True)
        converted_list = convert_from_path(pdf_path, **pdf2img_option)
    else:
        converted_list = get_file_list(converted_dir)
        converted_list.sort()
    return converted_list

def convert_and_crop_pdf_images(args, pdf_name, img_q: Queue):
    # original pdf data path
    pdf_path = Path(f"{args.pdf_dir}/{pdf_name}.pdf")
    # specify dpi with pdf name
    if args.dpi_random:
        args.dpi = random.choice(range(72, 201, 8))
    pdf_name = f"{pdf_name}_{args.dpi}"
    boxed_dir = Path(args.boxed_dir) / pdf_name if args.boxed_dir else None
    cropped_dir = Path(args.cropped_dir) / pdf_name
    try:
        pdf = PDFForTrainData(pdf_name, pdf_path, args.crop_line_bool, boxed_dir, cropped_dir, img_q)
        converted_list = convert_pdf2img(args, pdf_name, pdf_path)
        if len(converted_list) == 0:
            print('image to crop is not exist. convert pdf first')
        return crop_pdf_images(args, pdf, converted_list)
    except Exception as e:
        raise Exception(f'{pdf_name}convert and crop error path: {pdf_path}\n{e}')

def convert_pdf2crop(pdf_names, args, img_q: Queue, idx_dpi):
    excluded_chr_set = set()
    total_labels = OCRLabels()
    for pdf_idx, dpi in idx_dpi:
        args.dpi = dpi
        pdf_names_sublist = pdf_names[pdf_idx:pdf_idx + args.pool_count]
        pool = Pool(args.pool_count)
        results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(args, pdf_name, img_q)) 
                for pdf_name in pdf_names_sublist}
        pool.close()
        pool.join()
        img_q.put('end')
        for pdf_name in pdf_names_sublist:
            pdf_ocr_labels, invalid_chr_set = results[pdf_name].get()
            total_labels.merge_ocr_labels(pdf_ocr_labels)
            excluded_chr_set |= invalid_chr_set
    return total_labels, excluded_chr_set

if __name__ == '__main__':
    args = parse_args()
    start = time.time()
    pdf_names = [corpus_pdf_path.stem for corpus_pdf_path in get_file_list(args.pdf_dir)]
    pdf_names.sort()
    idx_dpi = list(product(range(0, len(pdf_names), args.pool_count), range(72, 73)))
    print('pdf length', len(pdf_names))
    with Manager() as manager:
        img_q = manager.Queue()
        collector = DataCollector(len(idx_dpi), img_q)
        total_labels, excluded_chr_set = convert_pdf2crop(pdf_names, args, img_q, idx_dpi)
    print(f"cropped img spent: {time.time() - start}")
    write_label(args.label_dir, total_labels.rec_label_list, 'rec_72dpi')
    # write_label(args.label_dir, total_labels.det_label_list, 'det_train')
    # write_label(args.label_dir, total_labels.det_section_label_list, 'det_section_train')
    # is_valid_rec_list(f"{args.label_dir}/eng_adminis_eval.txt")
    print("all pdf converted")
    print(f"total rec label length:{len(total_labels.rec_label_list)}")
    print("excluded_chr_set:", sorted(excluded_chr_set))