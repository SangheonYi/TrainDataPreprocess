from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import os

def get_support_chars(font_path):
    font = TTFont(font_path)   # specify the path to the font in question
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            return [chr(i) for i in cmap.cmap.keys() if chr(i).isprintable()]
    return False
    
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def make_image(text_to_draw, font_path):
    # Image size
    W = 30
    H = 30
    # font setting
    font = ImageFont.truetype(font_path, size=28)
    image =Image.new('RGB', (W, H), color = 'white')
    draw = ImageDraw.Draw(image)
    # start position for text
    x_text = 1
    y_text = 1
    # 각 줄의 내용을 적음
    draw.text((x_text, y_text), text_to_draw, font=font, fill="black")
    # 안에 적은 내용을 파일 이름으로 저장
    font_name = font_path[:-4]
    createDirectory(font_name)
    image.save(f'{font_name}/{text_to_draw}.jpg')
# for i in range(0x0010, 0x0080):
#     print(chr(i))
font_path = 'Gulim-01.ttf'
for c in get_support_chars(font_path):
    make_image(c, font_path)