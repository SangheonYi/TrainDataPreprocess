from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tempfile import TemporaryDirectory
from tqdm import tqdm
import time 
from util.util import create_directory
from multiprocessing import Pool

def draw_bbox(line, draw, rect_coord):
    create_directory('boxed')
    text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def pdf_to_jpg(pdf_path, tmp_path, pdf2jpg_option):
    start = time.time()
    pdf2jpg_option["output_folder"] = tmp_path
    result = convert_from_path(pdf_path, **pdf2jpg_option)
    print(f"convert spent: {time.time() - start}")
    return result 

def crop_pdf_images(
    zipped_arg=None,
    pdf_name=None,
    pdf=None,
    cropped_dir='cropped',
    img_rate=1,
    total=0
):
    cropped_labels = []
    create_directory(cropped_dir)
    for page, image_path, page_num in tqdm(zipped_arg, total=total):
        pdf.interpreter.process_page(page)
        # open img
        img = Image.open(image_path).convert("RGB")
        # draw = ImageDraw.Draw(img)
        for line in pdf.device.get_result():
            cropped_path = f'{cropped_dir}/{pdf_name}-{page_num}-{line.index}.jpg'
            left, upper, right, lower = pdf.cal_coor(line.bbox, img_rate)
            img.crop([left, upper, right, lower]).save(cropped_path)
            label_text = line.get_text().replace('  ', ' ')
            cropped_labels.append(f'{cropped_path}\t{label_text}')
            # draw_bbox(line, draw, ((left, lower), (right, upper)))
        # img.save(image_path.replace(tmp_path, 'boxed'), "JPEG")
        img.close()
    return ''.join(cropped_labels)

def convert_and_crop_pdf_images(pdf_name):
    pdf_dir = 'pdf'
    pdf_path = f"{pdf_dir}/{pdf_name}.pdf"
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
        "last_page" : 2000
    }
    crop_arg = {
        "pdf_name":pdf_name,
        "pdf":pdf,
        "img_rate":img_rate,
    }
    pdf_label = None
    
    with TemporaryDirectory() as tmp_path:
        print(f"converting")
        converted_list = pdf_to_jpg(pdf_path,tmp_path, pdf2jpg_option)
        images_size = len(converted_list)
        print(f"crop from {images_size} converted images")
        crop_arg["total"] = images_size
        crop_arg["zipped_arg"] = zip(pdf.pages, converted_list, range(images_size))
        pdf_label = crop_pdf_images(**crop_arg)
    print(f'{pdf_name}.pdf done')
    return pdf_label

def pdf_batch_work(pdf_names):
    pool = Pool(8)
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(pdf_name,)) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    total_label = ''
    for pdf_name in pdf_names:
        label = results[pdf_name].get()
        total_label = f"{total_label}{label}"
    return total_label

if __name__ == '__main__':
    pdf_names = ['jeong']
    pdf_names += [f'wind and constellation{pdf_index}' for pdf_index in range(6)]
    label = pdf_batch_work(pdf_names)
    with open('train.txt', 'w', encoding='utf-8') as label_file:
        label_file.write(label)
