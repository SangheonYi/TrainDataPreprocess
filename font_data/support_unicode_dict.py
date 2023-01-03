def r2l(a, b):
    # list of range from a to b include both a and b
    return list(range(a, b + 1))

# exclude_unicodes = {
#     # basic latin 0x0020, 0x007F
#     "basic_latin": [0x005c],
#     "exclude_range": r2l(0x007F, 0x303F),
#     # Hiragana 0x3040 <= i <= 0x303F

#     # Katakana 0x30A0 <= i <= 0x309F

#     # Hangul_Compatibility_Jamo 0x3130 <= i <= 0x318F
#     "Hangul_Compatibility_Jamo": [0x3130] + r2l(0x3164, 0x318F),

#     "CJK_range": r2l(0x0000 , 0x33FF),
#     # CJK_Unified_Ideographs 0x4E00 <= i <= 0x9FFF  

#     # Hangul_Syllables 0xAC00, 0xD7AF 
#     "Hangul_Syllables": r2l(0xAC00, 0xD7AF ),

#     # CJK_Compatibility_Ideograph 0xF900 <= i <= 0xFAFF
#     "BMP_Tail_range": r2l(0xFAFF, 0xFFFF),
#     # "BMP_Tail_range": r2l(0xF900, 0xFFFF),
# }
partial_include = {
		# Miscellaneous Symbols 0x2600, 0x26FF
		"Miscellaneous_Symbols": [0x2661],
		# Dingbats 0x2700, 0x27BF
		"Dingbats": [0x2764],
}
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

partial_include = {
    # General_Punctuation 0x2000, 0x206F
    "General_Punctuation": [0x2030, 0x2031, 0x203B, 0x204B], 
}

# convert dict
cjk_comp_ideo_to_unif_dict = {
    0xf900: 0x8c48,
    0xf901: 0x66f4,
    0xf902: 0x8eca,
    0xf903: 0x8cc8,
    0xf904: 0x6ed1,
    0xf905: 0x4e32,
    0xf906: 0x53e5,
    0xf907: 0x9f9c,
    0xf908: 0x9f9c,
    0xf909: 0x5951,
    0xf90a: 0x91d1,
    0xf90b: 0x5587,
    0xf90c: 0x5948,
    0xf90d: 0x61f6,
    0xf90e: 0x7669,
    0xf90f: 0x7f85,
    0xf910: 0x863f,
    0xf911: 0x87ba,
    0xf912: 0x88f8,
    0xf913: 0x908f,
    0xf914: 0x6a02,
    0xf915: 0x6d1b,
    0xf916: 0x70d9,
    0xf917: 0x73de,
    0xf918: 0x843d,
    0xf919: 0x916a,
    0xf91a: 0x99f1,
    0xf91b: 0x4e82,
    0xf91c: 0x5375,
    0xf91d: 0x6b04,
    0xf91e: 0x721b,
    0xf91f: 0x862d,
    0xf920: 0x9e1e,
    0xf921: 0x5d50,
    0xf922: 0x6feb,
    0xf923: 0x85cd,
    0xf924: 0x8964,
    0xf925: 0x62c9,
    0xf926: 0x81d8,
    0xf927: 0x881f,
    0xf928: 0x5eca,
    0xf929: 0x6717,
    0xf92a: 0x6d6a,
    0xf92b: 0x72fc,
    0xf92c: 0x90de,
    0xf92d: 0x4f86,
    0xf92e: 0x51b7,
    0xf92f: 0x52de,
    0xf930: 0x64c4,
    0xf931: 0x6ad3,
    0xf932: 0x7210,
    0xf933: 0x76e7,
    0xf934: 0x8001,
    0xf935: 0x8606,
    0xf936: 0x865c,
    0xf937: 0x8def,
    0xf938: 0x9732,
    0xf939: 0x9b6f,
    0xf93a: 0x9dfa,
    0xf93b: 0x788c,
    0xf93c: 0x797f,
    0xf93d: 0x7da0,
    0xf93e: 0x83c9,
    0xf93f: 0x9304,
    0xf940: 0x9e7f,
    0xf941: 0x8ad6,
    0xf942: 0x58df,
    0xf943: 0x5f04,
    0xf944: 0x7c60,
    0xf945: 0x807e,
    0xf946: 0x7262,
    0xf947: 0x78ca,
    0xf948: 0x8cc2,
    0xf949: 0x96f7,
    0xf94a: 0x58d8,
    0xf94b: 0x5c62,
    0xf94c: 0x6a13,
    0xf94d: 0x6dda,
    0xf94e: 0x6f0f,
    0xf94f: 0x7d2f,
    0xf950: 0x7e37,
    0xf951: 0x964b,
    0xf952: 0x52d2,
    0xf953: 0x808b,
    0xf954: 0x51dc,
    0xf955: 0x51cc,
    0xf956: 0x7a1c,
    0xf957: 0x7dbe,
    0xf958: 0x83f1,
    0xf959: 0x9675,
    0xf95a: 0x8b80,
    0xf95b: 0x62cf,
    0xf95c: 0x6a02,
    0xf95d: 0x8afe,
    0xf95e: 0x4e39,
    0xf95f: 0x5be7,
    0xf960: 0x6012,
    0xf961: 0x7387,
    0xf962: 0x7570,
    0xf963: 0x5317,
    0xf964: 0x78fb,
    0xf965: 0x4fbf,
    0xf966: 0x5fa9,
    0xf967: 0x4e0d,
    0xf968: 0x6ccc,
    0xf969: 0x6578,
    0xf96a: 0x7d22,
    0xf96b: 0x53c3,
    0xf96c: 0x585e,
    0xf96d: 0x7701,
    0xf96e: 0x8449,
    0xf96f: 0x8aaa,
    0xf970: 0x6bba,
    0xf971: 0x8fb0,
    0xf972: 0x6c88,
    0xf973: 0x62fe,
    0xf974: 0x82e5,
    0xf975: 0x63a0,
    0xf976: 0x7565,
    0xf977: 0x4eae,
    0xf978: 0x5169,
    0xf979: 0x51c9,
    0xf97a: 0x6881,
    0xf97b: 0x7ce7,
    0xf97c: 0x826f,
    0xf97d: 0x8ad2,
    0xf97e: 0x91cf,
    0xf97f: 0x52f5,
    0xf980: 0x5442,
    0xf981: 0x5973,
    0xf982: 0x5eec,
    0xf983: 0x65c5,
    0xf984: 0x6ffe,
    0xf985: 0x792a,
    0xf986: 0x95ad,
    0xf987: 0x9a6a,
    0xf988: 0x9e97,
    0xf989: 0x9ece,
    0xf98a: 0x529b,
    0xf98b: 0x66c6,
    0xf98c: 0x6b77,
    0xf98d: 0x8f62,
    0xf98e: 0x5e74,
    0xf98f: 0x6190,
    0xf990: 0x6200,
    0xf991: 0x649a,
    0xf992: 0x6f23,
    0xf993: 0x7149,
    0xf994: 0x7489,
    0xf995: 0x79ca,
    0xf996: 0x7df4,
    0xf997: 0x806f,
    0xf998: 0x8f26,
    0xf999: 0x84ee,
    0xf99a: 0x9023,
    0xf99b: 0x934a,
    0xf99c: 0x5217,
    0xf99d: 0x52a3,
    0xf99e: 0x54bd,
    0xf99f: 0x70c8,
    0xf9a0: 0x88c2,
    0xf9a1: 0x8aaa,
    0xf9a2: 0x5ec9,
    0xf9a3: 0x5ff5,
    0xf9a4: 0x637b,
    0xf9a5: 0x6bae,
    0xf9a6: 0x7c3e,
    0xf9a7: 0x7375,
    0xf9a8: 0x4ee4,
    0xf9a9: 0x56f9,
    0xf9aa: 0x5be7,
    0xf9ab: 0x5dba,
    0xf9ac: 0x601c,
    0xf9ad: 0x73b2,
    0xf9ae: 0x7469,
    0xf9af: 0x7f9a,
    0xf9b0: 0x8046,
    0xf9b1: 0x9234,
    0xf9b2: 0x96f6,
    0xf9b3: 0x9748,
    0xf9b4: 0x9818,
    0xf9b5: 0x4f8b,
    0xf9b6: 0x79ae,
    0xf9b7: 0x91b4,
    0xf9b8: 0x96b7,
    0xf9b9: 0x60e1,
    0xf9ba: 0x4e86,
    0xf9bb: 0x50da,
    0xf9bc: 0x5bee,
    0xf9bd: 0x5c3f,
    0xf9be: 0x6599,
    0xf9bf: 0x6a02,
    0xf9c0: 0x71ce,
    0xf9c1: 0x7642,
    0xf9c2: 0x84fc,
    0xf9c3: 0x907c,
    0xf9c4: 0x9f8d,
    0xf9c5: 0x6688,
    0xf9c6: 0x962e,
    0xf9c7: 0x5289,
    0xf9c8: 0x677b,
    0xf9c9: 0x67f3,
    0xf9ca: 0x6d41,
    0xf9cb: 0x6e9c,
    0xf9cc: 0x7409,
    0xf9cd: 0x7559,
    0xf9ce: 0x786b,
    0xf9cf: 0x7d10,
    0xf9d0: 0x985e,
    0xf9d1: 0x516d,
    0xf9d2: 0x622e,
    0xf9d3: 0x9678,
    0xf9d4: 0x502b,
    0xf9d5: 0x5d19,
    0xf9d6: 0x6dea,
    0xf9d7: 0x8f2a,
    0xf9d8: 0x5f8b,
    0xf9d9: 0x6144,
    0xf9da: 0x6817,
    0xf9db: 0x7387,
    0xf9dc: 0x9686,
    0xf9dd: 0x5229,
    0xf9de: 0x540f,
    0xf9df: 0x5c65,
    0xf9e0: 0x6613,
    0xf9e1: 0x674e,
    0xf9e2: 0x68a8,
    0xf9e3: 0x6ce5,
    0xf9e4: 0x7406,
    0xf9e5: 0x75e2,
    0xf9e6: 0x7f79,
    0xf9e7: 0x88cf,
    0xf9e8: 0x88e1,
    0xf9e9: 0x91cc,
    0xf9ea: 0x96e2,
    0xf9eb: 0x533f,
    0xf9ec: 0x6eba,
    0xf9ed: 0x541d,
    0xf9ee: 0x71d0,
    0xf9ef: 0x7498,
    0xf9f0: 0x85fa,
    0xf9f1: 0x96a3,
    0xf9f2: 0x9c57,
    0xf9f3: 0x9e9f,
    0xf9f4: 0x6797,
    0xf9f5: 0x6dcb,
    0xf9f6: 0x81e8,
    0xf9f7: 0x7acb,
    0xf9f8: 0x7b20,
    0xf9f9: 0x7c92,
    0xf9fa: 0x72c0,
    0xf9fb: 0x7099,
    0xf9fc: 0x8b58,
    0xf9fd: 0x4ec0,
    0xf9fe: 0x8336,
    0xf9ff: 0x523a,
    0xfa00: 0x5207,
    0xfa01: 0x5ea6,
    0xfa02: 0x62d3,
    0xfa03: 0x7cd6,
    0xfa04: 0x5b85,
    0xfa05: 0x6d1e,
    0xfa06: 0x66b4,
    0xfa07: 0x8f3b,
    0xfa08: 0x884c,
    0xfa09: 0x964d,
    0xfa0a: 0x898b,
    0xfa0b: 0x5ed3,
}

middledot_dict = {
    0x0387: 0x00b7, # · · Greek and Coptic Greek Ano Teleia
    0x119E: 0x00b7, # ᆞ· hangul jamo 아래 아 
    0x2022: 0x00b7, # • · general punctuation Bullet
    0x2024: 0x00b7, # ․ · general punctuation one dot leader
    0x2027: 0x00b7, # ‧ · general punctuation hyphenation point
    0x2219: 0x00b7, # ∙ · Mathematical Bullet Operator
    0x22C5: 0x00b7, # ⋅ · Mathematical Operators Dot Operator
    0x2981: 0x00b7, # ⦁ · Miscellaneous Mathematical Symbols-B Z NOTATION SPOT
    0x30fb: 0x00b7, # ・ · katakana middle dot 
    0x318d: 0x00b7, # ㆍ · hangul compatibility jamo 아래 아 
    0xff65: 0x00b7, # ･ · specials katakana middle dot 
}

half_full_to_ascii = {0xff00 + ascii_code - 32:ascii_code for ascii_code in range(33, 127)}

empty_circle = {
    # ○ Geometric Shapes white circle 0x25cb
    0x25ef: 0x25cb, # ◯ ○ Geometric Shapes Large Circle
    0x26aa: 0x25cb, # ⚪ ○ Miscellaneous Symbols MEDIUM WHITE CIRCLE
    0x3007: 0x25cb, # 〇 ○ CJK Symbols and Punctuation Ideographic Number Zero

    # ° 0x00b0 상단 위치
    # ◦ Geometric Shapes White Bullet 0x25e6 중단 위치
    0x2218: 0x25e6, # ∘ ◦ Mathematical Operators Ring Operator
    0x26AC: 0x25e6, # ⚬ ◦ Miscellaneous Symbols Medium Small White Circle
}

cjk_punctu = {
    0xff61: 0x3002, # ｡ 。 Halfwidth and Fullwidth Forms Halfwidth Ideographic Full Stop 하단 위치
    0xff62: 0x300c, # ｢ 「
    0xff63: 0x300d, # ｣ 」
    0xff64: 0x3001, # ､ 、
    0x3008: 0x003c, # 〈 < CJK Symbols and Punctuation Left Angle Bracket
    0x3009: 0x003e, # 〉 > CJK Symbols and Punctuation Right Angle Bracket
}

right_triangle = {
    0x25B8:0x2023, # ▸ ‣ Geometric Shapes Black Right-Pointing Small Triangle
}

empty_square = {
    0x2610:0x25A2, # ☐ ▢ Miscellaneous Symbols Ballot Box
}

black_squre = { # end of proof
    0x25ae:0x220e, # ▮ ∎ Geometric Shapes Black Vertical Rectangle
    0x25fc:0x220e, # ◼ ∎ Geometric Shapes Black Medium Square
    0x25fe:0x220e, # ◾ ∎ Geometric Shapes Black Medium Small Square
}

dingbats_to_enclosed = { encl + 800 : encl for encl in range(0x2460, 0x246A)}

dingbats_negative_circled = { neg_circ + 20 : neg_circ for neg_circ in range(0x2776, 0x2780)}

dingbats_to_arrows = {
    0x2794:0x2192, # ➔ → Dingbats Heavy Wide-Headed Rightwards Arrow
    0x279c:0x2192, # ➜ → Dingbats Heavy Round-Tipped Rightwards Arrow
    0x27a0:0x2192, # ➠ → Dingbats Heavy Dashed Triangle-Headed Rightwards Arrow
    0x27a1:0x2192, # ➡ → Dingbats Black Rightwards Arrow
    0x27a5:0x2192, # ➥ → Dingbats Heavy Black Curved Downwards and Rightwards Arrow
    0x27a9:0x21E8, # ➩ ⇨ Dingbats Right-Shaded White Rightwards Arrow
    0x27aa:0x21E8, # ➪ ⇨ Dingbats Left-Shaded White Rightwards Arrow
    0x27ad:0x21E8, # ➭ ⇨ Dingbats Heavy Lower Right-Shadowed White Rightwards Arrow
    0x27ae:0x21E8, # ➮ ⇨ Dingbats Heavy Upper Right-Shadowed White Rightwards Arrow
    0x27f6:0x2192, # ⟶ → Dingbats Long Rightwards Arrow
    0x27f9:0x21D2, # ⟹ ⇒ Dingbats Rightwards Double Arrow
    0x27fa:0x21D4, # ⟺ ⇔ Dingbats LONG LEFT RIGHT DOUBLE ARROW
}

tilde = {
    0x223C:0x007E, # ∼ ~ Mathematical Operators Tilde Operator
    0x301C:0x007E, # 〜 ~ CJK Symbols and Punctuation Operators Wave Dash
}

similar_dict_list = [
    cjk_comp_ideo_to_unif_dict, 
    middledot_dict, 
    half_full_to_ascii, 
    empty_circle, 
    cjk_punctu, 
    right_triangle, 
    empty_square, 
    black_squre, 
    dingbats_to_enclosed, 
    dingbats_negative_circled, 
    dingbats_to_arrows, 
    tilde
]