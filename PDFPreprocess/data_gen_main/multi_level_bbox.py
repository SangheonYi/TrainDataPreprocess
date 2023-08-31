from PDFForTrainData import PDFForTrainData
from merge_bbox import merge_section_bbox
from util import get_file_list, is_valid_rec_list, write_label, to_train_path
from option_args import parse_args, get_pdf2img_option
from OCRLabels import OCRLabels
from OCRUnicodeRange import *
from DataCollector import DataCollector

from pdf2image import convert_from_path
from multiprocessing import Pool, Manager, Queue, Process
from pathlib import Path
from itertools import product
from tqdm import tqdm
import random
import time
import os

def crop_from_page(configs, pdf:PDFForTrainData, page_idx):
    crop_idx = 0
    page_det_labels = []
    label_text, points, crop_list = pdf.parse_labels(page_idx)
    for crop_idx, (text, bbox_label, crop_coor) in enumerate(zip(label_text, points, crop_list)):
        cropped_path = pdf.cropped_dir / f'{page_idx}_{crop_idx}_.png'
        crop_img = pdf.current_img.crop(crop_coor)
        if configs.crop_image_save:
            os.makedirs(pdf.cropped_dir, exist_ok=True)
            crop_img.save(cropped_path)
        crop_train_path = to_train_path(cropped_path)
        if configs.write_tarball:
            pdf.img_q.put((crop_img, crop_train_path))
        pdf.ocr_labels.rec_label_list.append(f'{crop_train_path}\t{text}\n')
        page_det_labels.append({"transcription": text, "points": bbox_label})
    return crop_list, page_det_labels

def crop_pdf_images(configs, pdf: PDFForTrainData, converted_list):
    # for page_idx, image_path in enumerate(tqdm(converted_list, total=len(converted_list))):
    for page_idx, image_path in enumerate(converted_list):
        # open img
        pdf.set_crop_target(image_path)
        crop_list, det_gt = crop_from_page(configs, pdf, page_idx)
        pdf.draw_bboxes('', crop_list, bbox_only=True, line_width=3)
        # merge section label
        det_section_gt = merge_section_bbox(pdf, crop_list) if configs.merge_bbox else []
        pdf.ocr_labels.append_det_label(image_path, det_gt, det_section_gt)
        pdf.save_draw(image_path)
    # write_label(configs.label_dir, pdf.ocr_labels.cropped_labels, f'rec_{pdf_name}')
    # write_label(configs.label_dir, pdf.ocr_labels.det_labels, f'det_{pdf_name}')

    # section label
    # write_label(configs.label_dir, pdf.ocr_labels.det_labels, f'det_{pdf_name}')
    return pdf.ocr_labels, pdf.invalid_chr_set

def convert_pdf2img(configs, pdf_name, pdf_path):
    converted_dir = Path(configs.pdf_converted_dir) / pdf_name
    if configs.pdf2image_bool:
        pdf2img_option = get_pdf2img_option(configs)
        pdf2img_option["output_file"] = pdf_name
        pdf2img_option["output_folder"] = str(converted_dir)
        os.makedirs(pdf2img_option["output_folder"], exist_ok=True)
        converted_list = convert_from_path(pdf_path, **pdf2img_option)
    else:
        converted_list = get_file_list(converted_dir)
    return sorted(converted_list)

def convert_and_crop_pdf_images(configs, pdf_name, img_q: Queue):
    # original pdf data path
    pdf_path = Path(f"{configs.pdf_dir}/{pdf_name}.pdf")
    # specify dpi with pdf name
    if configs.dpi_random:
        configs.dpi = random.choice(range(72, 201, 8))
    pdf_name = f"{pdf_name}_{configs.dpi}"
    boxed_dir = Path(configs.boxed_dir) / pdf_name if configs.bbox_image_save else ''
    cropped_dir = Path(configs.cropped_dir) / pdf_name
    try:
        pdf = PDFForTrainData(pdf_name, pdf_path, configs.crop_line_bool, boxed_dir, cropped_dir, img_q, configs.dpi)
        converted_list = convert_pdf2img(configs, pdf_name, pdf_path)
        if len(converted_list) == 0:
            print('image to crop is not exist. convert pdf first')
        return crop_pdf_images(configs, pdf, converted_list)
    except Exception as e:
        raise Exception(f'{pdf_name}convert and crop error path: {pdf_path}\n{e}')

def convert_pdf2crop(pdf_names, configs, img_q: Queue, idx_dpi):
    excluded_chr_set = set()
    total_labels = OCRLabels()
    with Pool(configs.pool_count) as pool:
        for pdf_idx, dpi in tqdm(idx_dpi):
            configs.dpi = dpi
            pdf_names_sublist = pdf_names[pdf_idx:pdf_idx + configs.pool_count]
            results = pool.starmap(convert_and_crop_pdf_images, 
                               [(configs, pdf_name, img_q) for pdf_name in pdf_names_sublist])
            img_q.put('end')
            for pdf_ocr_labels, invalid_chr_set in results:
                total_labels.merge_ocr_labels(pdf_ocr_labels)
                excluded_chr_set |= invalid_chr_set
    return total_labels, excluded_chr_set

if __name__ == '__main__':
    configs = parse_args()
    start = time.time()
    with open('rec_valid_pdf.txt', 'r', encoding='utf-8') as valid_pdf_file:
        pdf_names = {valid_pdf_name.strip('.pdf\n') for valid_pdf_name in valid_pdf_file.readlines()}
    wrong_pdf_names = {
            "2022년 제6회 지방재정계획심의위원회 개최 결과",
            "결재문서본문 - 2022-10-14T163303.939_88",
            "고창청소년문화센터 민간위탁 심의위원회 개최",
            "아라천 디자인큐브 재위탁 운영 추진계획",
            "2022년 제8차 조례ㆍ규칙심의회 심의 계획",
            "「평생교육 중장기 발전계획 수립」연구용역 중간보고회 개최 계획",
            "결재문서본문 - 2022-09-30T111015.172",
            "결재문서본문 - 2022-10-18T174745.404",
            "관외출장결과보고 (철암보건지소 증축 국·도비 지원 건의)",
            "군산시 공동주택 관리 조례 일부개정 및 규칙 폐지 추진 계획",
            "지역아동센터 냉난방비 지원 (’23년 본예산)",
            "'22년 제2차 재난관리기금운용심의위원회 개최계획.pdf",
            "2022. 청소년어울림마당 청소년가요제 관련 익산시장상 요청에 따른 검토보고",
            "`22년 주거복지분야 정부포상 관련 국토부 출장 결과보고",
            "2022년 3분기 산업안전보건위원회 및 노사협의회 개최계획",
        }
    pdf_names -= wrong_pdf_names
    pdf_names = sorted(list(pdf_names))
    idx_dpi = list(product(range(0, len(pdf_names), configs.pool_count), range(72, 73)))
    print('pdf length', len(pdf_names))

    with Manager() as manager:
        img_q = manager.Queue()
        if configs.write_tarball:
            collector = DataCollector(len(idx_dpi), img_q)
            wirter_process = Process(target=collector.collect, args=(configs.tar_path, 'w:gz'))
            wirter_process.start()
        total_labels, excluded_chr_set = convert_pdf2crop(pdf_names, configs, img_q, idx_dpi)
        if configs.write_tarball:
            wirter_process.join()
    print(f"total spent: {time.time() - start}")
    print("excluded_chr_set:", sorted(excluded_chr_set))
    write_label(configs.label_dir, total_labels.rec_label_list, f"rec_72dpi")
    # write_label(configs.label_dir, total_labels.det_label_list, 'det_train')
    # write_label(configs.label_dir, total_labels.det_section_label_list, 'det_section_train')
    # is_valid_rec_list(f"{configs.label_dir}/eng_adminis_eval.txt")
    print("all pdf converted")
    print(f"total rec label length:{len(total_labels.rec_label_list)}")
    print(f"tar saved:{configs.tar_path}")