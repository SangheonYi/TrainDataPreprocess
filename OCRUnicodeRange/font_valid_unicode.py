from OCRUnicodeRange.util import r2l
from fontTools.ttLib import TTFont
from OCRUnicodeRange import partial_include

font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', '견고딕.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf']
font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi
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

won_dict = {
    "휴먼명조": {
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "hy헤드라인m": {
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "견고딕": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
    },
    "Dotum": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gungsuh": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Batang": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gulim": {
        chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
        chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
}

def is_valid_decimal(font_name, i, exclude_unicodes_list):
    if "견고딕" in font_name:
        return i not in gngt_empty_glyph_list
    elif not chr(i).isprintable() or i in exclude_unicodes_list:
        return False
    # check font glyph
    if font_name in ttf_exclude_glyph.keys():
        return i not in ttf_exclude_glyph[font_name] or i in partial_include
    print(f"decimal is not valid, {font_name} is unknown font")
    return False

def get_ttf_support_chars(font_path:str, exclude_unicodes_list):
    font = TTFont(font_path)
    support_chars = []
    font_name = font_path.split('/')[-1][:-4]
    print(f"get support character list from {font_path}")
    for cmap in font['cmap'].tables:
        encoding = cmap.getEncoding()
        for i in cmap.cmap.keys():
            uni_chr = chr(i)
            if is_valid_decimal(font_name, i, exclude_unicodes_list):
                try:                    
                    support_chars.append(uni_chr)
                except:
                    print(f"decimal {i} can't be encoded by {encoding}")
        if support_chars:
            return support_chars, encoding
    return False, ''