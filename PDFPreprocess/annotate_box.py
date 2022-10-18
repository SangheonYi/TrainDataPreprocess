from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from pdfminer.layout import LTTextBoxHorizontal
from PDFForTrainData import PDFForTrainData
from tempfile import TemporaryDirectory
from tqdm import tqdm
import time 
from util.util import create_directory

def draw_bbox(line, draw, rect_coord):
    create_directory('boxed')
    text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def pdf_to_jpg(tmp_path):
    start = time.time()
    pdf2jpg_option["output_folder"] = tmp_path
    result = convert_from_path(pdf_path, **pdf2jpg_option)
    print(f"convert spent: {time.time() - start}")
    return result 

def crop_pdf_images():
    # pdftoppm Bulldog.pdf Bulldog -jpeg 
    # convert pdf to jpg 
    with TemporaryDirectory() as tmp_path, open('train.txt', 'a', encoding='utf-8') as label_file:
        print(f"converting")
        converted_list = pdf_to_jpg(tmp_path)
        create_directory(cropped_dir)
        images_size = len(converted_list)
        print(f"crop from {images_size} converted images")
        for page, image_path, page_num in tqdm(zip(pdf.pages, converted_list, range(images_size)), total=images_size):
            pdf.interpreter.process_page(page)
            # open img
            img = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            for line in pdf.device.get_result():
                # if isinstance(line, LTTextBoxHorizontal):
                    # print(line)
                    # print(dir(line))
                cropped_path = f'{cropped_dir}/{pdf_name}-{page_num}-{line.index}.jpg'
                left, upper, right, lower = pdf.cal_coor(line.bbox, img_rate)
                img.crop([left, upper, right, lower]).save(cropped_path)
                label_text = line.get_text().replace('  ', ' ')
                label_file.write(f'{cropped_path}\t{label_text}')
                draw_bbox(line, draw, ((left, lower), (right, upper)))
            img.save(image_path.replace(tmp_path, 'boxed'), "JPEG")
            img.close()

if __name__ == '__main__':
    for pdf_index in range(6):
        pdf_name = f'wind and constellation{pdf_index}'
        # pdf_name = f'jeong'
        pdf_dir = 'pdf'
        pdf_path = f"{pdf_dir}/{pdf_name}.pdf"
        cropped_dir = 'cropped'
        img_rate = 1
        pdf = PDFForTrainData(pdf_path)
        pdf2jpg_option = {
            "fmt": "jpg",
            # "single_file": True,
            "paths_only": True,
            "use_pdftocairo": True,
            "size": (None, pdf.page_height * img_rate),
            "timeout": 1200, 
            "thread_count": 4,
            "output_file": pdf_name,
            # "last_page" : 2
        }
        crop_pdf_images()
        print(f'{pdf_index}th pdf done')