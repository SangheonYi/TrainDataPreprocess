from PIL import Image, ImageDraw
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tqdm import tqdm
import time 
from util.util import create_directories, create_directory, get_file_list, is_valid_rec_list
from multiprocessing import Pool
from os import cpu_count
import os
from pathlib import Path
import json

def draw_bbox(line, draw, rect_coord):
    # text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    # draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def pdf_to_jpg(pdf_path, pdf2jpg_option):
    start = time.time()
    result = convert_from_path(pdf_path, **pdf2jpg_option)
    # print(f"convert spent: {time.time() - start}")
    return result 

def append_label_list(coord, points, crop_list):
    left, upper, right, lower = coord
    points.append([[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]])
    crop_list.append(coord)

def parse_labels(crop_line, line, pdf):
    points = []
    crop_list = []
    line_coor = pdf.cal_coor(line.bbox)
    left, upper, right, lower = line_coor
    line_text = line.get_text().rstrip().replace('  ', ' ')
    if crop_line:
        label_text = [line_text]
        append_label_list(line_coor, points, crop_list)
    else:
        label_text = line_text.split(' ')
        space_count = 0
        crop_left = left
        for ltchr in line:
            if isinstance(ltchr, LTChar) and ltchr.get_text() == ' ':
                space_count += 1
                if space_count >= len(label_text):
                    continue
                space_coor = pdf.cal_coor(ltchr.bbox)
                margin = (space_coor[2] - space_coor[0]) * 0.3
                crop_right = space_coor[0] + margin
                crop_coord = [crop_left, upper, crop_right, lower]
                append_label_list(crop_coord, points, crop_list)
                crop_left = space_coor[2] - margin
        crop_coord = [crop_left, upper, right, lower]
        append_label_list(crop_coord, points, crop_list)
        
    return label_text, points, crop_list

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
    cropped_labels = []
    det_labels = []
    page_det_labels = []
    if directories['boxed_dir']:
        boxed_dir = Path(directories['boxed_dir']) / pdf_name
    else:
        boxed_dir = None
    cropped_dir= Path(directories['cropped_dir']) / pdf_name
    create_directory(boxed_dir)
    create_directory(cropped_dir)
    for page, image_path, page_num in tqdm(zipped_arg, total=total):
        pdf.interpreter.process_page(page)
        # open img
        img = Image.open(image_path).convert("RGB")
        # draw bbox feature is commented
        if boxed_dir:
            draw = ImageDraw.Draw(img)
        crop_idx = 0
        for lobj in pdf.device.get_result():
            if isinstance(lobj, LTTextBoxHorizontal) :
                for line in lobj:
                    if isinstance(line, LTTextLineHorizontal):
                        label_text, points, crop_list = parse_labels(crop_line, line, pdf)
                        for text, bbox_label, crop_coor in zip(label_text, points, crop_list):
                            if bbox_label[0] == bbox_label[1]:
                                continue
                            cropped_path = cropped_dir / f'{page_num}_{crop_idx}.jpg'
                            img.crop(crop_coor).save(cropped_path)
                            cropped_labels.append(f'{cropped_path}\t{text}\n')
                            page_det_labels.append({"transcription": "label_text", "points": bbox_label})
                            if boxed_dir:
                                left, upper, right, lower = crop_coor
                                draw_bbox(line, draw, ((left, lower), (right, upper)))
                            crop_idx += 1

        det_labels.append(f"{image_path}\t{json.dumps(page_det_labels, ensure_ascii=False)}\n")
        if boxed_dir:
            boxed_path = boxed_dir / Path(image_path).name
            img.save(boxed_path, "JPEG")
        img.close()
    # write_label(directories['label_dir'], cropped_labels, f'rec_{pdf_name}')
    # write_label(directories['label_dir'], det_labels, f'det_{pdf_name}')
    return ''.join(det_labels), ''.join(cropped_labels)

def convert_and_crop_pdf_images(directories, pdf_name, pdf2image_bool):
    pdf_path = f"{directories['pdf_dir']}/{pdf_name}.pdf"
    img_rate = 1
    pdf = PDFForTrainData(pdf_path, img_rate)
    converted_dir = Path(directories['pdf_converted_dir']) / pdf_name
    pdf2jpg_option = {
        "fmt": "jpg",
        # "single_file": True,
        "paths_only": True,
        "use_pdftocairo": True,
        "size": (None, pdf.page_height * img_rate),
        "timeout": 1200, 
        "thread_count": 4,
        "output_folder": converted_dir,
        "output_file": pdf_name,
        # "last_page" : 1
    }
    crop_arg = {
        "pdf_name": pdf_name,
        "pdf": pdf,
        "directories": directories,
        "crop_line": False
    }
    converted_list = get_file_list(converted_dir)
    if pdf2image_bool:
        create_directory(converted_dir)
        # print('converting')
        converted_list = pdf_to_jpg(pdf_path, pdf2jpg_option)
    images_size = len(converted_list)
    crop_arg["total"] = images_size
    crop_arg["zipped_arg"] = zip(pdf.pages, converted_list, range(images_size))
    # print('cropping')
    pdf_label = crop_pdf_images(**crop_arg)
    print(f'{pdf_name}.pdf done')
    return pdf_label

def batch_convert_pdf2crop(pool_count, pdf_names, pdf2image_bool=True, directories = {
        'pdf_converted_dir':'converted', 
        'boxed_dir':None, 
        'cropped_dir':'cropped', 
        'label_dir': 'labels',
        'pdf_dir': 'corpus_pdf'
    }):
    pool = Pool(pool_count)
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(directories, pdf_name, pdf2image_bool)) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    rec_label_list = []
    det_label_list = []
    for pdf_name in pdf_names:
        det_label, rec_label = results[pdf_name].get()
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    return ''.join(det_label_list), ''.join(rec_label_list)

def write_label(label_dir, label_list, label_name):
    label = ''.join(label_list)
    label_path = f'{label_dir}/{label_name}.txt'
    with open(label_path, 'a', encoding='utf-8') as label_file:
        label_file.write(label)

if __name__ == '__main__':
    pool_count = os.cpu_count()
    pool_count = 1
    # pdf_names += [f'wind{pdf_index}' for pdf_index in range(10)]
    directories = {
        'pdf_converted_dir':'converted', 
        'boxed_dir':'boxed', # if None not save boxed image
        'cropped_dir':'cropped', 
        'label_dir': 'labels',
        'pdf_dir': 'pdf'
    }
    create_directories(directories.values())

    # font, size pdf
    pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
    for corpus_pdf_path in get_file_list(directories['pdf_dir'])]
    pdf_names = ['jeong']

    det_label_list = []
    rec_label_list = []
    step = pool_count * 2
    step = 1
    for pdf_idx in range(0, len(pdf_names), step):
        det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], pdf2image_bool=True, directories=directories)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    write_label(directories['label_dir'], rec_label_list, 'rec_banila_train')
    write_label(directories['label_dir'], det_label_list, 'det_train')
