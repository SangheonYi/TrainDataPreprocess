from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tqdm import tqdm
from util import get_file_list, is_valid_rec_list, write_label
from option_args import parse_args, get_pdf2img_option
from multiprocessing import Pool
from pathlib import Path
import random
import json

from OCRUnicodeRange import *
from itertools import product
from merge_bbox import merge_overlapping_rectangles, add_merge_margin
from functools import partial
import time
from pprint import pprint

excluded_chr_set = set()

def crop_from_page(pdf:PDFForTrainData, cropped_labels):
    crop_idx = 0
    word_bbox_list = []
    page_det_labels = []
    invalid_page_chrs = set()

    for line in pdf.get_valid_lines_from_page():
        label_text, points, crop_list, invalid_line_chrs = pdf.parse_labels(line)
        word_bbox_list += crop_list
        invalid_page_chrs = invalid_page_chrs.union(invalid_line_chrs)
        pdf.draw_bboxes("word box", crop_list, draw_coord=True, bbox_only=True, box_color='grey', line_width=1)
        for text, bbox_label, crop_coor in zip(label_text, points, crop_list):
            cropped_path = pdf.cropped_dir / f'{pdf.current_page_num}_{crop_idx}_.png'
            pdf.current_img.crop(crop_coor).save(cropped_path)
            cropped_labels.append(f'{cropped_path}\t{text}\n')
            page_det_labels.append({"transcription": text, "points": bbox_label})
            crop_idx += 1
    pdf.current_img.close()
    return word_bbox_list, page_det_labels, invalid_page_chrs

def margin_and_merge_bbox(low_level_bbox_list, margin_rate, pdf: PDFForTrainData,
                           is_horizon=True, margin_box_color='red', merged_box_color='green', draw_margin_box=False, draw_high_level_box=False):
    add_merge_margin_partial = partial(add_merge_margin, margin_rate=margin_rate, is_horizon=is_horizon)
    margined_bbox_list = list(map(add_merge_margin_partial, low_level_bbox_list))
    high_level_bbox_list = merge_overlapping_rectangles(margined_bbox_list)
    if draw_margin_box:
        pdf.draw_bboxes("margined box", margined_bbox_list, box_color=margin_box_color, line_width=8)
    if draw_high_level_box:
        pdf.draw_bboxes("high_level_coord", high_level_bbox_list, box_color=merged_box_color, line_width=6)
    return high_level_bbox_list

def merge_section_bbox(pdf: PDFForTrainData, word_bbox_list):
    # draw word box
    pdf.draw_bboxes("word box", word_bbox_list, draw_coord=True, bbox_only=True)
    # merge horizontal
    line_bbox_list = margin_and_merge_bbox(word_bbox_list, 0.23, pdf)
    # merge vertical
    section_bbox_list = margin_and_merge_bbox(line_bbox_list, 0.3, pdf, 
                                              is_horizon=False, margin_box_color='blue', merged_box_color='yellow', draw_high_level_box=True)
    page_det_section_labels = []
    for i, merged_coord in enumerate(section_bbox_list):
        left, upper, right, lower = merged_coord
        section_gt = [[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]]
        page_det_section_labels.append({"transcription": f"section {i}", "points": section_gt})
    return page_det_section_labels

def crop_pdf_images(args,
    converted_list=None,
    pdf_name=None,
    pdf:PDFForTrainData=None,
    total=0,
):
    cropped_labels = []
    det_labels = []
    det_section_labels = []
    invalid_chr_set = set()
    for image_path in tqdm(converted_list, total=total):
        # open img
        pdf.set_crop_target(image_path)
        # draw bbox feature is commented
        word_bbox_list, page_det_labels, invalid_page_chrs = crop_from_page(pdf, cropped_labels)
        invalid_chr_set = invalid_chr_set.union(invalid_page_chrs)
        det_labels.append(f"{image_path}\t{json.dumps(page_det_labels, ensure_ascii=False)}\n")
        # merge section label
        page_det_section_labels = merge_section_bbox(pdf, word_bbox_list)
        pdf.save_draw(image_path)
        det_section_labels.append(f"{image_path}\t{json.dumps(page_det_section_labels, ensure_ascii=False)}\n")
    # write_label(args.label_dir, cropped_labels, f'rec_{pdf_name}')
    # write_label(args.label_dir, det_labels, f'det_{pdf_name}')

    # section label
    # write_label(args.label_dir, det_labels, f'det_{pdf_name}')
    return ''.join(det_labels), ''.join(det_section_labels), ''.join(cropped_labels), invalid_chr_set

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

def convert_and_crop_pdf_images(args, pdf_name):
    # original pdf data path
    pdf_path = Path(f"{args.pdf_dir}/{pdf_name}.pdf")
    # specify dpi with pdf name
    if args.dpi_random:
        args.dpi = random.choice(range(72, 201, 8))
    pdf_name = f"{pdf_name}_{args.dpi}"
    boxed_dir = Path(args.boxed_dir) / pdf_name if args.boxed_dir else None
    cropped_dir = Path(args.cropped_dir) / pdf_name
    pdf = PDFForTrainData(pdf_path, args.crop_line_bool, boxed_dir, cropped_dir)
    try:
        converted_list = convert_pdf2img(args, pdf_name, pdf_path)
    except:
        print('convert and crop error:', pdf_name)
        return
    
    images_size = len(converted_list)
    if images_size == 0:
        print('image to crop is not exist. convert pdf first')
    crop_arg = {
        "pdf_name": pdf_name,
        "pdf": pdf,
        "total": images_size,
        "converted_list": converted_list,
    }
    det_label, det_section_label, rec_label, invalid_chr_set = crop_pdf_images(args, **crop_arg)
    print(f'{pdf_name}.pdf done')
    return det_label, det_section_label, rec_label, invalid_chr_set

def batch_convert_pdf2crop(pdf_names, args):
    pool = Pool(args.pool_count)
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(args, pdf_name)) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    rec_label_list = []
    det_label_list = []
    det_section_label_list = []
    global excluded_chr_set
    for pdf_name in pdf_names:
        det_label, det_section_label, rec_label, invalid_chr_set = results[pdf_name].get()
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
        det_section_label_list.append(det_section_label)
        excluded_chr_set = excluded_chr_set.union(invalid_chr_set)
    return ''.join(det_label_list), ''.join(det_section_label_list), ''.join(rec_label_list)

if __name__ == '__main__':
    # pool_count = 8
    # pdf_names += [f'wind{pdf_index}' for pdf_index in range(10)]
    args = parse_args()
    # create_directories(directories.values())

    # font, size pdf
    pdf_names = [corpus_pdf_path.stem for corpus_pdf_path in get_file_list(args.pdf_dir)]

    # with open('rec_valid_pdf.txt', 'r', encoding='utf-8') as rec_valid_pdf_file:
    #     pdf_names = [valid_pdf.strip().strip('.pdf') for valid_pdf in rec_valid_pdf_file.readlines()]
    "어린이 통학로 교통안전 기본계획 용역 중간보고회 결과보고"
    print('pdf length', len(pdf_names))
    pdf_names.sort()
    det_label_list = []
    rec_label_list = []
    det_section_label_list = []
    step = args.pool_count
    
    for pdf_idx, dpi in product(range(0, len(pdf_names), step), range(200, 201)):
        args.dpi = dpi
        pdf_names_sublist = pdf_names[pdf_idx:pdf_idx + step]
        det_label, det_section_label, rec_label = batch_convert_pdf2crop(pdf_names_sublist, args)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
        det_section_label_list.append(det_section_label)
    write_label(args.label_dir, rec_label_list, 'eng_adminis_eval')
    # write_label(args.label_dir, det_label_list, 'det_train')
    write_label(args.label_dir, det_section_label_list, 'det_section_train')
    # is_valid_rec_list(f"{args.label_dir}/eng_adminis_eval.txt")
    print("all pdf converted")
    print("excluded_chr_set:", sorted(excluded_chr_set))