# update sayi_dict with pdf char set 
# convert back slash with currency won for scraped pdfs

# for scraped pdfs filter
dont_care = {'ʱ', '˯', 'Ϛ', '⭕', 'ʵ', '〮', '⸱', '˻', 'ʳ', 'ʴ', 'ʶ', '▄', 'ʲ', '⸢', '˪'}
need_pdf_check = {'▢', '〜', '❖', '◯', '￭', 'ʼ'}
wrong_glyph = {
    # '\\': ['2022년 누리과정 보육료 예탁금 지급(3차)', '결재문서본문 - 2022-10-04T151340.124', '결재문서본문 - 2022-10-18T193020.376', '2022년 동부권역 소규모 하천정비사업(3회추경) 실시설계용역 시행', '결재문서본문 - 2022-10-18T115325.780', '2022년 저수지 퇴적토 준설사업 실시설계용역 시행', '보육교사 건강장해 예방 매뉴얼 개발에 따른 외부 집필진 계약 체결', '결재문서본문 - 2022-10-04T175447.825', '결재문서본문 - 2022-09-30T124520.630', '결재문서본문 - 2022-10-01T074405.367', '결재문서본문 - 2022-10-04T160809.506', '2022년 경로당 정부양곡비 지급(9월)', '도곡온천지구 활성화 방안 용역 시행', '결재문서본문 - 2022-10-04T161507.850', '2022년 서부권역 소규모 하천정비사업(3회추경) 실시설계용역 시행'],
    'ʱ': ['당진형 마더센터 조성 추진계획', '당진 역사_인문투어 기업체 유치 계획', '의정비심의위원회 개최 계획', '근골격계 부담작업 유해요인조사 실시계획(안)', '2022년 합천군 농축산물 가격안정기금          운용 계획 심의회 개최 계획(안)', '제4회 동구 사회복지의 날 기념 유공자 표창 계획', '제8기 지역보건의료계획 수립 추진 계획', '당진시 재정계획 및 재정공시심의위원회 심의 계획'],
    'ʲ': ['당진형 마더센터 조성 추진계획', '당진 역사_인문투어 기업체 유치 계획', '의정비심의위원회 개최 계획', '근골격계 부담작업 유해요인조사 실시계획(안)', '2022년 합천군 농축산물 가격안정기금          운용 계획 심의회 개최 계획(안)', '제4회 동구 사회복지의 날 기념 유공자 표창 계획', '제8기 지역보건의료계획 수립 추진 계획'],
    'ʳ': ['근골격계 부담작업 유해요인조사 실시계획(안)', '당진 역사_인문투어 기업체 유치 계획', '제8기 지역보건의료계획 수립 추진 계획', '제4회 동구 사회복지의 날 기념 유공자 표창 계획', '2022년 합천군 농축산물 가격안정기금          운용 계획 심의회 개최 계획(안)'],
    'ʴ': ['근골격계 부담작업 유해요인조사 실시계획(안)', '당진 역사_인문투어 기업체 유치 계획', '제8기 지역보건의료계획 수립 추진 계획', '2022년 합천군 농축산물 가격안정기금          운용 계획 심의회 개최 계획(안)'],
    'ʵ': ['근골격계 부담작업 유해요인조사 실시계획(안)', '제8기 지역보건의료계획 수립 추진 계획'],
    'ʶ': ['제8기 지역보건의료계획 수립 추진 계획'],
    'ʼ': ['공공부문 비정규직 채용 사전심사제도 운영 계획'],
    '˪': ['「보령시 아동 급식지원 조례」일부개정 계획'],
    '˯': ['환경피해대응 주민건강모니터링 용역 중간보고회 개최 계획', '자매결연도시 마포구「제29회 마포구민의 날」 참석 계획', '아동청소년과 한시임기제공무원 채용계획(안)'],
    '˻': ['2023년 민간위탁금(노사지원팀) 본예산 편성보고'],
    'Ϛ': ['민선8기 구청장 공약사항 실천계획 및 목록 확정 보고', '2022년 탄소중립 시민실천단 워크숍 개최 계획', '수시 제9차 지방재정계획심의위원회 회의(심의)결과 보고', '고령친화도시 조성위원회  위촉식 및 정기회의 개최 계획', '지속가능한 미래를 위한 탄소중립 특강 계획', '태안군민대상 조례 일부개정 추진계획', '수시 제9차 지방재정계획심의위원회 회의(심의)결과 알림', '중간보고회 개최 결과보고', '아동청소년과 한시임기제공무원 채용계획(안)'],
    '❖': ['2023년도 지방세연구원 출연금 출연 계획(안)',] ,
    '⸢': ['미추홀구 신청사건립사업 추진 현황 정기보고(9월)'],
    '⸱': ['신안군의회 조례안 부의안건'],
    '〜': ['「제11회 굿네이버스 누리교육그림그리기대회」참여 우수아동에 대한 상장 시상 계획', '「평생교육 중장기 발전계획 수립」연구용역 중간보고회 개최 계획', '2022 찾아가는 복지 유공자 표창 계획', '2022년 제8차 조례ㆍ규칙심의회 심의 계획', ],
    '〮': ['결재문서본문 - 2022-10-01T064615.268'],
    '￭': ['조례규칙 심의회 의결서(12회)', ],
}

wrong_glyph_set = set()
wrong_glyph_chr = set(wrong_glyph.keys())
for pdf_list in wrong_glyph.values():
    wrong_glyph_set = wrong_glyph_set.union(pdf_list)

exclude_range = [    
    # Combining Diacritical Marks 0x0300 - 0x036F 제외
    [chr(comb_mark) for comb_mark in range(0x0300, 0x036F)] + 
    # Superscripts and Subscripts 0x2070 <= i <= 0x209F 
    [chr(script) for script in range(0x2070, 0x20a0)] +
    # Combining Diacritical Marks for Symbols 0x20D0 - 0x20FF 제외
    [chr(comb_symbol) for comb_symbol in range(0x20D0, 0x20FF)] +
    # CJK Symbols and Punctuation 0x3000 <= i <= 0x303F 중 0x302A ~ 0x302F
    [chr(comb_code) for comb_code in range(0x302a, 0x3030)]
]

convert_dicts_keys = set()
convert_dicts_vals = set()

from OCRUnicodeRange import convert_dict_list

convert_won_dict = {
    chr(0x5c): chr(0x20a9), # \ ₩ basic latin back slash
    chr(0xffe6): chr(0x20a9), # ￦ ₩ Halfwidth and Fullwidth Forms Fullwidth won sign
}
convert_dict_list = convert_dict_list + convert_won_dict

for convert_dict in convert_dict_list:
    convert_dicts_keys = convert_dicts_keys.union(convert_dict.keys())
    convert_dicts_vals = convert_dicts_vals.union(convert_dict.values())

def replace_to_valid_chr(txt_chr_set, txt, convert_dict):
    for chr in txt_chr_set.intersection(convert_dict.keys()):
        txt = txt.replace(chr, convert_dict[chr])
    return txt

def txt2valid_range(txt):
    txt_chr_set = set(txt)
    need_convert_chars = txt_chr_set.intersection(convert_dicts_keys)
    if need_convert_chars:
        for convert_dict in convert_dict_list:
            txt = replace_to_valid_chr(need_convert_chars, txt, convert_dict)
    return txt

if __name__ == '__main__':
    print(txt2valid_range('\\'))
    # with open('../font_data/korean_dict.txt', 'r', encoding='utf-8') as sayi_dict:
    #     sayi_vocab = set([line[0] for line in sayi_dict.readlines()])
    
    # for i, convert_dict in enumerate(convert_dict_list):
    #     print(f'{i}th diff val:', set(convert_dict.values()) - sayi_vocab)
    # non_printable = {'\x00', '\x81', '\x82', '\x87', '\x8c', '\x8d', '\x8e', '\x8f', '\x9e', '\x9f', '\xa0', '\xad', '\u2002', '\u3000', '\ue047', '\ue06d', '\uf000', '\uf06c', '\uf06d', '\uf06f', '\uf071', '\uf076', '\uf077', '\uf081', '\uf082', '\uf09e', '\uf0a0', '\uf0a6', '\uf0c4', '\uf0e0', '\uf0e8', '\uf0e9', '\uf0f0', '\uf0fe', }
    # dont_care_icon = {'ࠆ', 'ࠗ', 'ࡐ', 'ࡑ', 'ࡒ', 'ࡓ','❍', '❏', '❐', '❑', '❒', '〫', '◼'}
    # dingbat = {'❍', '❏', '❐', '❑', '❒'}    
    # exclude_chr_set = {'\\', '²', '³', '¹', 'ʱ', 'ʲ', 'ʳ', 'ʴ', 'ʵ', 'ʶ', 'ʼ', '˅', 'ˇ', 'ː', '˝', '˪', '˯', 
    # '˹', '˻',  '́', '̇', '͠', 'ʹ', 'Ϛ',  'ᄒ', 'ᆫ', '‣', '⁃', '⁋', '₃', '⃝', '⃞', '↳', '⇀', '⇄', '⇐', '⇓', '⇛', 
    # '⇦', '⇨', '⇩', '∎', '∘', '≼', '≽', '⋅', '⋗', '⋯', '⌌', '⌎', '⌜', '⌟', 

    # '⑯', '⑰', '⑱', '⑲', '⑳', 
    # # Enclosed CJK Letters and Months Range: 3200–32FF
    # '㉑', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚', '㉛', '㉝', '㉞', '㊞', '㊱', '㊲', '㊳', '㊴', '㊶', '㊷', '㊸', '㊺', 

    # '⓵', '⓶', '⓷', '─', '━', '│', '┃', '┌', '┍', '┏', '┓', '└', '┕', '┗', '┛', '├', '┠', '┣', '┤', '┨', '┬', 
    # '┯', '┷', '┼', '╂', '╺', '▄', '▢', '▮', '▴', '▵', '▸', '▹', '▻', '◉', '◌', '◪', '◯', '◼', '◽', '◾', 
    # '☐', '☑', '⚪', '⚫', '⚬', 
    # # Dingbats 0x2700 <= i <= 0x27BF
    # '✍', '✐', '✔', '✕', '✥', '✳', '✻', '❊', '❋', '❖', '❙', '❚', '❯', 
    # '❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿', '➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈', '➉', 
    # '➊', '➋', '➌', '➍', '➎', '➏', '➐', '➑', 
    # '➔', '➙', '➜', '➠', '➡', '➢', '➣', '➤', '➥', '➩', '➪', '➭', '➮', '➯', '➲',
    # # Miscellaneous Mathematical Symbols-A 0x27C0 <= i <= 0x27EF
    # '⟦', '⟧', 
    # # Supplemental Arrows-A Range: 27F0–27FF
    # '⟶', '⟹', '⟺', 
    # # Miscellaneous Mathematical Symbols-BRange: 2980–29FF
    # '⦁', '⧠', 
    # # Miscellaneous Symbols and Arrows Range: 2B00–2BFF
    # '⬞', '⭕', 
    # # Supplemental Punctuation Range: 2E00–2E7F
    # '⸢',
    # # CJK Symbols and Punctuation Range: 3000–303F
    # '〇', '〖', '〗', '〜', '〮', 
    # # Halfwidth and Fullwidth Forms Range: FF00–FFEF
    # '￭'}
