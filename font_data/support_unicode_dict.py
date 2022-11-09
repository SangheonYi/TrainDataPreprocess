def r2l(a, b):
    # list of range from a to b include both a and b
    return list(range(a, b + 1))

exclude_unicodes = {
    # basic latin 0x0020, 0x007F
    "basic_latin": [0x005c],
    "exclude_range": r2l(0x007F, 0x303F),
    # Hiragana 0x3040 <= i <= 0x303F

    # Katakana 0x30A0 <= i <= 0x309F

    # Hangul_Compatibility_Jamo 0x3130 <= i <= 0x318F
    "Hangul_Compatibility_Jamo": [0x3130] + r2l(0x3164, 0x318F),

    "CJK_range": r2l(0x3200 , 0x33FF),
    # CJK_Unified_Ideographs 0x4E00 <= i <= 0x9FFF  

    # Hangul_Syllables 0xAC00 <= i <= 0xD7AF 

    # CJK_Compatibility_Ideograph 0xF900 <= i <= 0xFAFF
    "BMP_Tail_range": r2l(0xF900, 0xFFFF),
}
partial_include = {
		# Miscellaneous Symbols 0x2600, 0x26FF
		"Miscellaneous_Symbols": [0x2661],
		# Dingbats 0x2700, 0x27BF
		"Dingbats": [0x2764],
}
# exclude_unicodes = {
#     # basic latin 0x0020, 0x007F
#     "basic_latin": [0x005c],
#     # latin_supplement 0x0080, 0x00FF
#     "latin_supplement": [0x00aa] + r2l(0x00b2, 0x00b3) + [0x00b9],
#     # Latin_Extended-A 0x0100, 0x017F
#     "Latin_Extended-A": [0x0131, 0x0138],
#     # Latin_Extended-B 0x0180, 0x024F
#     "Latin_Extended-B": [0x00aa] + r2l(0x0184, 0x0185) + [0x0192, 0x0196] + r2l(0x01b5, 0x01b6) \
#         + [0x01c0] + r2l(0x01c3, 0x01cc) + r2l(0x01f1, 0x01f3),
#     # IPA_Extensions 0x0250, 0x02AF
#     # Spacing_modifier_letters 0x02B0, 0x02FF
#     # Combining_Marks 0x0300, 0x036F
#     "from_IPA_Extensions_to_Combining_Marks": r2l(0x0250, 0x036F),
#     # Greek_and_Coptic 0x0370, 0x03FF

#     # Cyrillic 0x0400, 0x04FF

#     # Hangul_jamo 0x1100, 0x11FF option
#     "Hangul_jamo": r2l(0x1100, 0x11FF),
#     # Latin_Extended_Additional 0x1E00, 0x1EFF pass

#     # General_Punctuation 0x2000, 0x206F
    
#     # Superscripts_and_Subscripts 0x2070, 0x209F 
#     "Superscripts_and_Subscripts": r2l(0x2070, 0x209F),
#     # Currency_Symbols 0x20A0, 0x20CF

#     # Letterlike_Symbols 0x2100, 0x214F

#     # Number_Forms 0x2150, 0x218F 
#     "Number_Forms": r2l(0x216c, 0x216f) + r2l(0x217c, 0x217f),
#     # Arrows 0x2190, 0x21FF 

#     # Mathematical_Operators 0x2200, 0x22FF

#     # Miscellaneous_Technical 0x2300, 0x23FF
#     "Miscellaneous_Technical": r2l(0x2300, 0x23FF),
#     # Enclosed_Alphanumerics 0x2460, 0x24FF

#     # Box_Drawing 0x2500, 0x257F
#     "Box_Drawing": r2l(0x2500, 0x257F),
#     # Box_Elements 0x2580, 0x259F 
#     "Box_Elements": r2l(0x2580, 0x259F),
#     # Geometric_Shapes 0x25A0, 0x25FF

#     # Miscellaneous_Symbols 0x2600, 0x26FF

#     # CJK_Symbols_and_Punctuation 0x3000, 0x303F
#     "CJK_Symbols_and_Punctuation": [0x3000],

#     # Hiragana 0x3040, 0x303F

#     # Katakana 0x30A0, 0x309F

#     # Hangul_Compatibility_Jamo 0x3130, 0x318F
#     "Hangul_Compatibility_Jamo": [0x3130] + r2l(0x3164, 0x318F),
#     # Enclosed_CJK_Letters and Months 0x3200, 0x32FF  

#     # CJK_Compatibility 0x3300, 0x33FF  

#     # CJK_Unified_Ideographs 0x4E00, 0x9FFF  

#     # Hangul_Syllables 0xAC00, 0xD7AF 

#     # CJK_Compatibility_Ideograph 0xF900, 0xFAFF
#     "CJK_Compatibility_Ideograph": r2l(0xF900, 0xFAFF),
#     # Alphabetic_Presentation_Forms  0xFB00, 0xFB4F

#     # Halfwidth_and_Fullwidth_Forms 0xFF00, 0xFFEF 
#     "Halfwidth_and_Fullwidth_Forms": r2l(0xFF00, 0xFFEF),
#     # Specials 0xFFF9, 0xFFFF
#     "Specials": r2l(0xFFF9, 0xFFFF)

# }

# partial_include = {
#     # General_Punctuation 0x2000, 0x206F
#     "General_Punctuation": [0x2030, 0x2031, 0x203B, 0x204B], 
# }