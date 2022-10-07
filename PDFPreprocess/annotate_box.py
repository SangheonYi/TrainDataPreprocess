from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tempfile import TemporaryDirectory
import os

def print_progress(i, list_len):
    progress = round(i / list_len, 2) * 100
    if i % 100 == 0:
        print(f'{i} done')
    if progress % 5 == 0 : 
        print(f'{progress}%')

def draw_bbox(line, draw, rect_coord):
    # text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox, "new_orig: ", [[x0, new_y0], [x1, new_y1]])
    draw.rectangle(rect_coord, outline=color)
    # draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def create_directory(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error: Failed to create the directory.")

def get_crop_img_path(tmp_path, image_path):
    file_name_replaced = image_path.replace('.jpg', f'-{line.index}.jpg')
    return 'cropped/test' + f'-{line.index}.jpg'
    return file_name_replaced.replace(tmp_path, 'cropped')

file_name = 'jeong'
pdf_path = f"pdf/{file_name}.pdf"
color = "dodgerblue"
img_rate = 1

pdf = PDFForTrainData(pdf_path)
pdf2jpg_option = {
	"fmt": "jpg",
	"single_file": True,
	"paths_only": True,
	"use_pdftocairo": True,
	"size": (None, pdf.page_height * img_rate),
	"timeout": 1200, 
	"thread_count": 4,
	# "output_file": file_name
}

if 1:
    # pdftoppm Bulldog.pdf Bulldog -jpeg 
    # convert pdf to jpg 
    with TemporaryDirectory() as tmp_path:
        pdf2jpg_option["output_folder"] = tmp_path
        converted_list = convert_from_path(f"pdf/{file_name}.pdf", **pdf2jpg_option)
        print(f"converted images: {len(converted_list)}")
        for i, image_path in enumerate(converted_list):
            print(image_path)
            pdf.interpreter.process_page(pdf.page)
            # open img
            img = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            for line in pdf.device.get_result():
                left, upper, right, lower = pdf.cal_coor(line.bbox, img_rate)
                img.crop([left, upper, right, lower]).save(get_crop_img_path(tmp_path, image_path))
                # draw_bbox(line, draw, ((left, bottom), (right, top)))
            # img.save(image_path.replace(tmp_path, 'boxed'), "JPEG")
            img.close()
            print_progress(i, len(converted_list))
            pdf.next_page()
            break