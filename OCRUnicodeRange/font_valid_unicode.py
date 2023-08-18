from OCRUnicodeRange.util import r2l
from fontTools.ttLib import TTFont
from OCRUnicodeRange import partial_include

# 견고딕은 인코딩 이슈가 자주 발생하는 euc-kr이고 문자 셋도 적어서 제외하고 HY견고딕로 대체하는 편이다.
font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf', '견고딕.ttf', 'Gungsuh.ttf', 'Batang.ttf', 'Gulim.ttf', 'HY견고딕.ttf']
font_sizes = [27, 47, 66] # 8, 14, 20 pt in 200dpi, 더 작은 글자 인식 필요. 현재 140dpi 8pt부터 인식률 무너짐
human_empty_glyph_list = [8361]
hyhead_empty_glyph_list = [96]
hyhead_wrong_glyph_list = r2l(162, 163) + r2l(165, 166) + r2l(169, 175) + [181, 187]
hygyengo_empty_glyph_list = [96]
hygyengo_wrong_glyph_list = r2l(162, 163) + r2l(165, 166) + r2l(169, 175) + [181, 187]
gngt_empty_glyph_list = r2l(0, 31) + r2l(127, 255) + r2l(42196, 42238)
ttf_exclude_glyph = {
    "휴먼명조": human_empty_glyph_list,
    "Dotum": [],
    "hy헤드라인m": hyhead_empty_glyph_list + hyhead_wrong_glyph_list,
    "견고딕": gngt_empty_glyph_list,
    "Gungsuh": [],
    "Batang": [],
    "Gulim": [],
    "HY견고딕": hygyengo_empty_glyph_list + hygyengo_wrong_glyph_list
}

won_dict = {
    "휴먼명조": {
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "hy헤드라인m": {
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "견고딕": {
      0x5c: chr(0x20a9), # \ ₩ basic latin back slash
    },
    "Dotum": {
      0x5c: chr(0x20a9), # \ ₩ basic latin back slash
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gungsuh": {
      0x5c: chr(0x20a9), # \ ₩ basic latin back slash
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Batang": {
      0x5c: chr(0x20a9), # \ ₩ basic latin back slash
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "Gulim": {
      0x5c: chr(0x20a9), # \ ₩ basic latin back slash
      0xffe6: chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    },
    "HY견고딕": {
      0xffe6: chr(0x20a9) # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
    }
}

def convert_won_glyph(src_str: str, font_won_dict: dict):
    for k, v in font_won_dict.items():
        src_str = src_str.replace(k, v)
    return src_str

def is_valid_decimal(font_name, i, exclude_unicodes_list):
    if "견고딕" == font_name:
        return i not in gngt_empty_glyph_list
    # exclude unuse unicode-level glyph
    elif not chr(i).isprintable() or i in exclude_unicodes_list:
        return False
    # check font-level invalid glyph
    if font_name in ttf_exclude_glyph.keys():
        return i not in ttf_exclude_glyph[font_name]
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