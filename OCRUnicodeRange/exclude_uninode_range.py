# Used when creating data with fonts

from OCRUnicodeRange.util import r2l
from OCRUnicodeRange.convert_similar_glyphs import convert_dict_list

exclude_unicodes = {
    # basic latin 0x0020, 0x007F

    # latin_supplement 0x0080, 0x00FF
    "latin_supplement": [0x00aa] + r2l(0x00b2, 0x00b3) + [0x00b9] + r2l(0x00bf, 0x00d6) + 
    r2l(0x00d8, 0x00f6) + r2l(0x00f8, 0x00ff),
    # Latin_Extended-A 0x0100, 0x017F
    # Latin_Extended-B 0x0180, 0x024F
    # IPA_Extensions 0x0250, 0x02AF
    # Spacing_modifier_letters 0x02B0, 0x02FF
    # Combining_Marks 0x0300, 0x036F
    "from_Latin_Extended-A_to_Combining_Marks": r2l(0x0100, 0x036F),
    # Greek_and_Coptic 0x0370, 0x03FF
    "Greek_and_Coptic": r2l(0x0386, 0x0390) + [0x37e, 0x384, 0x387, 0x391, 0x392, 0x394, 0x395, 0x396, 0x397, 0x399, 0x39a, 
    0x39c, 0x39d, 0x39f, 0x3a0, 0x3a1, 0x3a3, 0x3a4, 0x3a5, 0x3a7, 0x3b9, 0x3ba, 0x3bd, 0x3bf,] + r2l(0x03aa, 0x03b0) + r2l(0x03ca, 0x03ce),

    # Cyrillic 0x0400, 0x04FF
    "Cyrillic": r2l(0x0400, 0x04FF),
    # Hangul_jamo 0x1100, 0x11FF option
    "Hangul_jamo": r2l(0x1100, 0x11FF),
    # Latin_Extended_Additional 0x1E00, 0x1EFF pass
    "Latin_Extended_Additional": r2l(0x1E00, 0x1EFF),
    # General_Punctuation 0x2000, 0x206F
    "General_Punctuation": r2l(0x2000, 0x206F),
    # Superscripts_and_Subscripts 0x2070, 0x209F 
    "Superscripts_and_Subscripts": r2l(0x2070, 0x209F),
    # Currency_Symbols 0x20A0, 0x20CF

    # Letterlike_Symbols 0x2100, 0x214F
    "Letterlike_Symbols": [0x02126, 0x212e],
    # Number_Forms 0x2150, 0x218F 
    "Number_Forms": r2l(0x216c, 0x216f) + r2l(0x217c, 0x217f),
    # Arrows 0x2190, 0x21FF 

    # Mathematical_Operators 0x2200, 0x22FF
    "Mathematical_Operators": [0x2212, 0x2215, 0x223c],
    # Miscellaneous_Technical 0x2300, 0x23FF
    "Miscellaneous_Technical": r2l(0x2300, 0x23FF),
    # Enclosed_Alphanumerics 0x2460, 0x24FF
    "Enclosed_Alphanumerics": r2l(0x2474, 0x24b5),
    # Box_Drawing 0x2500, 0x257F
    "Box_Drawing": r2l(0x2500, 0x257F),
    # Box_Elements 0x2580, 0x259F 
    "Box_Elements": r2l(0x2580, 0x259F),
    # Geometric_Shapes 0x25A0, 0x25FF

    # Miscellaneous_Symbols 0x2600, 0x26FF

    # CJK_Symbols_and_Punctuation 0x3000, 0x303F
    "CJK_Symbols_and_Punctuation": [0x3000],

    # Hiragana 0x3040, 0x309F
    # Katakana 0x30A0, 0x30FF
    "Kana": r2l(0x3040, 0x30FF),
    # Hangul_Compatibility_Jamo 0x3130, 0x318F
    "Hangul_Compatibility_Jamo": [0x3130] + r2l(0x3164, 0x318F),
    # Enclosed_CJK_Letters_and_Months 0x3200, 0x32FF  
    "Enclosed_CJK_Letters_and_Months": r2l(0x3200, 0x321c),
    # CJK_Compatibility 0x3300, 0x33FF  

    # CJK_Unified_Ideographs 0x4E00, 0x9FFF  

    # Hangul_Syllables 0xAC00, 0xD7AF 

    # CJK_Compatibility_Ideograph 0xF900, 0xFAFF
    "CJK_Compatibility_Ideograph": r2l(0xF900, 0xFAFF),
    # Alphabetic_Presentation_Forms  0xFB00, 0xFB4F

    # Halfwidth_and_Fullwidth_Forms 0xFF00, 0xFFEF 
    "Halfwidth_and_Fullwidth_Forms": r2l(0xFF00, 0xFFEF),
    # Specials 0xFFF9, 0xFFFF
    "Specials": r2l(0xFFF9, 0xFFFF)
}

total_exclude_unicodes_list = []
for v in exclude_unicodes.values():
    total_exclude_unicodes_list += v
for conv_dict in convert_dict_list:
    total_exclude_unicodes_list += list(conv_dict.keys())