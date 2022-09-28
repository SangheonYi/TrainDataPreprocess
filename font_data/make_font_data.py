from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import os
import struct
def r2l(a, b):
    # list of range from a to b include both a and b
    return list(range(a, b + 1))

exclude_unicodes = {
    # basic latin 0x0020 <= i <= 0x007F
    "basic_latin": [0x005c],
    # latin_supplement 0x0080 <= i <= 0x00FF
    "latin_supplement": [0x00aa] + r2l(0x00b2, 0x00b3) + [0x00b9],
    # Latin_Extended-A 0x0100 <= i <= 0x017F
    "Latin_Extended-A": [0x0131, 0x0138],
    # Latin_Extended-B 0x0180 <= i <= 0x024F
    "Latin_Extended-B": [0x00aa] + r2l(0x0184, 0x0185) + [0x0192, 0x0196] + r2l(0x01b5, 0x01b6) \
        + [0x01c0] + r2l(0x01c3, 0x01cc) + r2l(0x01f1, 0x01f3),
    # IPA_Extensions 0x0250 <= i <= 0x02AF
    # Spacing_modifier_letters 0x02B0 <= i <= 0x02FF
    # Combining_Marks 0x0300 <= i <= 0x036F
    "from_IPA_Extensions_to_Combining_Marks": r2l(0x0250, 0x036F),
    # Greek_and_Coptic 0x0370 <= i <= 0x03FF

    # Cyrillic 0x0400 <= i <= 0x04FF

    # Hangul_jamo 0x1100 <= i <= 0x11FF option
    "Hangul_jamo": r2l(0x1100, 0x11FF),
    # Latin_Extended_Additional 0x1E00 <= i <= 0x1EFF pass

    # General_Punctuation 0x2000 <= i <= 0x206F
    "General_Punctuation": r2l(0x2000, 0x200F) + [0x2011] + r2l(0x2028, 0x202F) + r2l(0x205F, 0x206F),
    # Superscripts_and_Subscripts 0x2070 <= i <= 0x209F 
    "Superscripts_and_Subscripts": r2l(0x2070, 0x209F),
    # Currency_Symbols 0x20A0 <= i <= 0x20CF

    # Letterlike_Symbols 0x2100 <= i <= 0x214F

    # Number_Forms 0x2150 <= i <= 0x218F 
    "Number_Forms": r2l(0x216c, 0x216f) + r2l(0x217c, 0x217f),
    # Arrows 0x2190 <= i <= 0x21FF 

    # Mathematical_Operators 0x2200 <= i <= 0x22FF

    # Miscellaneous_Technical 0x2300 <= i <= 0x23FF
    "Miscellaneous_Technical": r2l(0x2300, 0x23FF),
    # Enclosed_Alphanumerics 0x2460 <= i <= 0x24FF

    # Box_Drawing 0x2500 <= i <= 0x257F
    "Box_Drawing": r2l(0x2500, 0x257F),
    # Box_Elements 0x2580 <= i <= 0x259F 
    "Box_Elements": r2l(0x2580, 0x259F),
    # Geometric_Shapes 0x25A0 <= i <= 0x25FF

    # Miscellaneous_Symbols 0x2600 <= i <= 0x26FF

    # CJK_Symbols_and_Punctuation 0x3000 <= i <= 0x303F
    "CJK_Symbols_and_Punctuation": [0x3000],

    # Hiragana 0x3040 <= i <= 0x303F

    # Katakana 0x30A0 <= i <= 0x309F

    # Hangul_Compatibility_Jamo 0x3130 <= i <= 0x318F
    "Hangul_Compatibility_Jamo": [0x3130] + r2l(0x3164, 0x318F),
    # Enclosed_CJK_Letters and Months 0x3200 <= i <= 0x32FF  

    # CJK_Compatibility 0x3300 <= i <= 0x33FF  

    # CJK_Unified_Ideographs 0x4E00 <= i <= 0x9FFF  

    # Hangul_Syllables 0xAC00 <= i <= 0xD7AF 

    # CJK_Compatibility_Ideograph 0xF900 <= i <= 0xFAFF
    "CJK_Compatibility_Ideograph": r2l(0xF900, 0xFAFF),
    # Alphabetic_Presentation_Forms  0xFB00 <= i <= 0xFB4F

    # Halfwidth_and_Fullwidth_Forms 0xFF00 <= i <= 0xFFEF 
    "Halfwidth_and_Fullwidth_Forms": r2l(0xFF00, 0xFFEF),
    # Specials 0xFFF9 <= i <= 0xFFFF
    "Specials": r2l(0xFFF9, 0xFFFF)

}
exclude_unicodes_list = []
for v in exclude_unicodes.values():
    exclude_unicodes_list += v
font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', 'GNGT(견고딕).ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf']
human_empty_glyph_list = [8361]
hyhead_empty_glyph_list = [96]
hyhead_wrong_glyph_list = r2l(162, 163) + r2l(165, 166) + r2l(162, 163) + r2l(162, 163) + r2l(162, 163)
gngt_empty_glyph_list = r2l(0, 31) + r2l(127, 255) + r2l(42196, 42238)
ttf_exclude_glyph = {
    "휴먼명조": human_empty_glyph_list,
    "Dotum": [],
    "hy헤드라인m": hyhead_empty_glyph_list + hyhead_wrong_glyph_list,
    "견고딕": gngt_empty_glyph_list,
    "Gungsuh": [],
    "Batang": [],
    "Gulim": []
}

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except OSError:
        print("Error: Failed to create the directory.")
        return False

def make_font_data(text_to_draw, font_path, encoding, save_dir, font_size=10):
    # Image size
    W = font_size
    H = W
    # font setting
    encode_type = 'unic' if encoding.startswith("utf") else 'wans'
    font = ImageFont.truetype(font_path, size=font_size, encoding=encode_type)
    image =Image.new('RGB', (W, H), color = 'white')
    draw = ImageDraw.Draw(image)
    # start position for text
    position_xy = (1, 1)
    # draw text_to_draw on image
    draw.text(position_xy, text_to_draw, font=font, fill="black")
    # save image
    save_path = f'{save_dir}/{ord(text_to_draw)}.jpg'
    image.save(save_path)
    return save_path

def make_fonts_dataset(font_path_list, font_sizes, mode):
    label_lines = []
    for font_path in font_path_list:
        support_chars, encoding = get_ttf_support_chars(font_path)
        font_name = font_path[:-4]
        if support_chars:
            for font_size in font_sizes:
                save_dir = f'{mode}{font_name}_{font_size}_data'
                if createDirectory(save_dir):
                    for c, label in support_chars:
                        image_path = make_font_data(c, font_path, encoding, save_dir, font_size=font_size)
                        label_lines.append(f"kor_rec_train/{image_path}\t{label}\n")
        else:
            print(f"{font_path} is empty")
    return label_lines

def write_label_file(label_lines):
    with open('train_label.txt', 'w', encoding="utf-8") as label_file:
        label_contents = ''.join(label_lines)
        label_file.write(label_contents)

def get_encoded_chr(i, encoding):
    if not encoding.startswith("utf") and i > 127:
        # euckr encoding
        return struct.pack('>H', i).decode(encoding)
    return chr(i)

def is_valid_decimal(font_name, i):
    if "견고딕" in font_name:
        return i not in gngt_empty_glyph_list
    elif not chr(i).isprintable() or i in exclude_unicodes_list:
        return False

    # check font glyph
    if font_name in ttf_exclude_glyph.keys():
        return i not in ttf_exclude_glyph[font_name]
    print(f"decimal is not valid, {font_name} is unknown font")
    return False

def get_ttf_support_chars(font_path):
    font = TTFont(font_path)   # specify the path to the font in question
    support_chars = []
    font_name = font_path[:-4]
    # print(dir(font))
    print(f"get support character list from {font_path}")
    for cmap in font['cmap'].tables:
        encoding = cmap.getEncoding()
        # print(dir(cmap))
        # print(cmap.isUnicode(), encoding)
        for i in cmap.cmap.keys():
            uni_chr = chr(i)
            if is_valid_decimal(font_name, i):
                try:
                    support_char = (uni_chr, get_encoded_chr(i, encoding))
                    support_chars.append(support_char)
                except:
                    print(f"decimal {i} can't be encoded by {encoding}")
        if support_chars:
            return support_chars, encoding
    return False, ''

font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', 'GNGT(견고딕).ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf']
# font_path_list = ['GNGT(견고딕).ttf']
font_sizes = [100]
# , 10, 11, 13, 16]
label_lines = make_fonts_dataset(font_path_list, font_sizes, 'train')
write_label_file(label_lines)