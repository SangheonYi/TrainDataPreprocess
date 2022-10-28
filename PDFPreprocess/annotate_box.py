import json
from PIL import Image, ImageDraw, ImageFont
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tqdm import tqdm
import time 
from util.util import create_directories, create_directory
from multiprocessing import Pool
from os import cpu_count
import os

def draw_bbox(line, draw, rect_coord):
    # text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    # draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def pdf_to_jpg(pdf_path, pdf2jpg_option):
    start = time.time()
    result = convert_from_path(pdf_path, **pdf2jpg_option)
    print(f"convert spent: {time.time() - start}")
    return result 

def get_file_list(path):
    for root, dir, file_list in os.walk(path):
        return [os.path.join(root, file) for file in file_list]

def crop_pdf_images(
    zipped_arg=None,
    pdf_name=None,
    pdf=None,
    img_rate=1,
    total=0
):
    cropped_labels = []
    det_labels = []
    boxed_dir = os.path.join('boxed', pdf_name)
    cropped_dir= os.path.join('cropped', pdf_name)
    create_directory(boxed_dir)
    create_directory(cropped_dir)
    for page, image_path, page_num in tqdm(zipped_arg, total=total):
        pdf.interpreter.process_page(page)
        # open img
        img = Image.open(image_path).convert("RGB")
        # draw bbox feature is commented
        draw = ImageDraw.Draw(img)
        img_det_label = []
        for lobj in pdf.device.get_result():
            if isinstance(lobj, LTTextBoxHorizontal) :
                for line in lobj:
                    if isinstance(line, LTTextLineHorizontal):
                        cropped_path = f'{cropped_dir}/{page_num}_{lobj.index}.jpg'
                        left, upper, right, lower = pdf.cal_coor(line.bbox, img_rate)
                        img.crop([left, upper, right, lower]).save(cropped_path)
                        label_text = line.get_text().replace('  ', ' ')
                        cropped_labels.append(f'{cropped_path}\t{label_text}')
                        points = [[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]]
                        img_det_label.append({"transcription": "label_text", "points": points})
                        draw_bbox(line, draw, ((left, lower), (right, upper)))
        det_labels.append(f"{image_path}\t{json.dumps(img_det_label, ensure_ascii=False)}")
        img.save(image_path.replace("converted", 'boxed'), "JPEG")
        img.close()
    rec_label = ''.join(cropped_labels)
    det_label = '\n'.join(det_labels)
    write_labels(det_label, rec_label, f'rec_{pdf_name}', f'det_{pdf_name}')
    return det_label, rec_label

def convert_and_crop_pdf_images(pdf_name, convert_bool):
    pdf_dir = 'pdf'
    pdf_path = f"{pdf_dir}/{pdf_name}.pdf"
    img_rate = 1
    pdf = PDFForTrainData(pdf_path)
    converted_dir = os.path.join("converted", pdf_name)
    pdf2jpg_option = {
        "fmt": "jpg",
        # "single_file": True,
        "paths_only": True,
        "use_pdftocairo": True,
        "size": (None, pdf.page_height * img_rate),
        "timeout": 1200, 
        "thread_count": 1,
        "output_folder": converted_dir,
        "output_file": pdf_name,
        "last_page" : 1
    }
    crop_arg = {
        "pdf_name":pdf_name,
        "pdf":pdf,
        "img_rate":img_rate,
    }
    print(f"converting")
    converted_list = get_file_list(converted_dir)
    if convert_bool:
        create_directory(converted_dir)
        converted_list = pdf_to_jpg(pdf_path, pdf2jpg_option)
    images_size = len(converted_list)
    print(f"crop from {images_size} converted images")
    crop_arg["total"] = images_size
    crop_arg["zipped_arg"] = zip(pdf.pages, converted_list, range(images_size))
    pdf_label = crop_pdf_images(**crop_arg)
    print(f'{pdf_name}.pdf done')
    return pdf_label

def pdf_batch_work(pdf_names):
    pool = Pool(cpu_count())
    print("cpu count:", cpu_count())
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(pdf_name, True)) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    rec_total_label = ''
    det_total_label = ''
    for pdf_name in pdf_names:
        det_label, rec_label = results[pdf_name].get()
        rec_total_label = f"{rec_total_label}{rec_label}"
        det_total_label = f"{det_total_label}{det_label}"
    return det_total_label, rec_total_label

def write_labels(det_label, rec_label, rec_label_name='rec_banila_train', det_label_name='det_train'):
    with open(f'labels/{rec_label_name}.txt', 'w', encoding='utf-8') as rec_label_file:
        rec_label_file.write(rec_label)
    with open(f'labels/{det_label_name}.txt', 'w', encoding='utf-8') as det_label_file:
        det_label_file.write(det_label)

if __name__ == '__main__':
    # pdf_names = ['real']
    pdf_names = ['jeong']
    # pdf_names += [f'wind{pdf_index}' for pdf_index in range(10)]
    directories = ['converted', 'boxed', 'cropped', 'labels']
    create_directories(directories)
    det_label, rec_label = pdf_batch_work(pdf_names)
    write_labels(det_label, rec_label)
