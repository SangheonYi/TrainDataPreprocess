from PIL import Image, ImageDraw
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, LTAnno
from pdf2image import convert_from_path
from PDFForTrainData import PDFForTrainData
from tqdm import tqdm
import time 
from util.util import create_directories, create_directory, get_file_list, is_valid_rec_list
from multiprocessing import Pool
from os import cpu_count
import os
from pathlib import Path
import json
from recog_valid_unicode import *
import tarfile

exclude_chr_set = {'\\', '²', '³', '¹', 'ʱ', 'ʲ', 'ʳ', 'ʴ', 'ʵ', 'ʶ', 'ʼ', '˅', 'ˇ', 'ː', '˝', '˪', '˯', 
'˹', '˻',  '́', '̇', '͠', 'ʹ', 'Ϛ',  'ᄒ', 'ᆫ', '‣', '⁃', '⁋', '₃', '⃝', '⃞', '↳', '⇀', '⇄', '⇐', '⇓', '⇛', 
'⇦', '⇨', '⇩', '∎', '∘', '≼', '≽', '⋅', '⋗', '⋯', '⌌', '⌎', '⌜', '⌟', 

'⑯', '⑰', '⑱', '⑲', '⑳', 
# Enclosed CJK Letters and Months Range: 3200–32FF
'㉑', '㉔', '㉕', '㉖', '㉗', '㉘', '㉙', '㉚', '㉛', '㉝', '㉞', '㊞', '㊱', '㊲', '㊳', '㊴', '㊶', '㊷', '㊸', '㊺', 

'⓵', '⓶', '⓷', '─', '━', '│', '┃', '┌', '┍', '┏', '┓', '└', '┕', '┗', '┛', '├', '┠', '┣', '┤', '┨', '┬', 
'┯', '┷', '┼', '╂', '╺', '▄', '▢', '▮', '▴', '▵', '▸', '▹', '▻', '◉', '◌', '◪', '◯', '◼', '◽', '◾', 
'☐', '☑', '⚪', '⚫', '⚬', 
# Dingbats 0x2700 <= i <= 0x27BF
'✍', '✐', '✔', '✕', '✥', '✳', '✻', '❊', '❋', '❖', '❙', '❚', '❯', 
'❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿', '➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈', '➉', 
'➊', '➋', '➌', '➍', '➎', '➏', '➐', '➑', 
'➔', '➙', '➜', '➠', '➡', '➢', '➣', '➤', '➥', '➩', '➪', '➭', '➮', '➯', '➲',
# Miscellaneous Mathematical Symbols-A 0x27C0 <= i <= 0x27EF
 '⟦', '⟧', 
# Supplemental Arrows-A Range: 27F0–27FF
 '⟶', '⟹', '⟺', 
# Miscellaneous Mathematical Symbols-BRange: 2980–29FF
'⦁', '⧠', 
# Miscellaneous Symbols and Arrows Range: 2B00–2BFF
'⬞', '⭕', 
# Supplemental Punctuation Range: 2E00–2E7F
'⸢',
# CJK Symbols and Punctuation Range: 3000–303F
'〇', '〖', '〗', '〜', '〮', 
# Halfwidth and Fullwidth Forms Range: FF00–FFEF
'￭'}
non_printable = {'\x00', '\x81', '\x82', '\x87', '\x8c', '\x8d', '\x8e', '\x8f', '\x9e', '\x9f', '\xa0', '\xad', '\u2002', '\u3000', '\ue047', '\ue06d', '\uf000', '\uf06c', '\uf06d', '\uf06f', '\uf071', '\uf076', '\uf077', '\uf081', '\uf082', '\uf09e', '\uf0a0', '\uf0a6', '\uf0c4', '\uf0e0', '\uf0e8', '\uf0e9', '\uf0f0', '\uf0fe', }
dont_care_icon = {'ࠆ', 'ࠗ', 'ࡐ', 'ࡑ', 'ࡒ', 'ࡓ','❍', '❏', '❐', '❑', '❒', '〫', '◼', 

}
dingbat = {'❍', '❏', '❐', '❑', '❒'}
excluded_chr_set = set()

def draw_bbox(line, draw, rect_coord):
    # text = line.get_text()
    # print("text: ", text, "coor_orig: ", line.bbox)
    draw.rectangle(rect_coord, outline="dodgerblue")
    # draw.text(rect_coord[0], f'{text[:-1]}', font=ImageFont.truetype("font/Batang.ttf", size=20), fill="dodgerblue")
    return 

def is_valid_text(text, pdf_name):
    # global unuse_chars
    # unuse_chars
    # return be true when set(text) - sayi_vocab is empty set
    diff = list(set(text) - sayi_vocab)
    if not diff:
        return True, {}
    # unuse_chars = unuse_chars.union(diff)
    # if diff[0] in non_printable:
    #     return False, {}
    for chr in diff:
        if chr in dingbat:
            print('dingbat:', chr, hex(ord(chr)))
        # print(diff, hex(ord(diff[0])))
    print("issue pdf name:", pdf_name)
    # return False, diff
    return True, diff

def append_label_list(coor, points, crop_list):
    left, upper, right, lower = coor
    points.append([[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]])
    crop_list.append(coor)

def parse_labels(crop_line, line, pdf:PDFForTrainData, img_rate):
    points = []
    crop_list = []
    # print(line.bbox, img_rate)
    coor = pdf.cal_coor(line.bbox, img_rate)
    left, upper, right, lower = coor
    line_text = line.get_text().strip()
    while '  ' in line_text:
        line_text = line_text.replace('  ', ' ')
    line_text = txt2valid_range(line_text)
    if crop_line:
        label_text = [line_text]
        print('crop_line:', label_text)
    else:
        label_text = []
        gt_word = ''
        got_left = False
        # data inspecting
        target_chr = [ '╺',         ]
        for ltchr in line:
            char = ltchr.get_text()
            if char not in target_chr:
            # if char == ' ' or char in sayi_vocab:
            #  or char in exclude_chr_set.union(dont_care_icon).union(non_printable): # both LTchr and LTAnno have get_text() and can be blank character
                if got_left:
                    coor = [left, upper, right, lower]
                    append_label_list(coor, points, crop_list)
                    label_text.append(gt_word)
                    gt_word = ''
                got_left = False
            elif isinstance(ltchr, LTChar) and char in target_chr:
            # and (char in exclude_chr_set or char in dingbat):
                space_coor = pdf.cal_coor(ltchr.bbox, img_rate)
                if not got_left:
                    left = space_coor[0]
                    got_left = True
                right = space_coor[2]
                gt_word = f"{gt_word}{char}"
        label_text.append(gt_word)
        coor = [left, upper, right, lower]
        # print(label_text, crop_list)
    append_label_list(coor, points, crop_list)
    return label_text, points, crop_list

def crop_pdf_images(
    zipped_arg=None,
    pdf_name=None,
    pdf=None,
    directories={
        'boxed_dir': None,
        'cropped_dir': 'cropped'
    },
    total=0,
    crop_line=False, 
    img_rate=1
):
    invalid_chr_set = set()
    cropped_labels = []
    det_labels = []
    page_det_labels = []
    if directories['boxed_dir']:
        boxed_dir = Path(directories['boxed_dir']) / pdf_name
    else:
        boxed_dir = None
    cropped_dir= Path(directories['cropped_dir']) / pdf_name
    create_directory(boxed_dir)
    create_directory(cropped_dir)
    for page, image_path, page_num in tqdm(zipped_arg, total=total):
        page_width, page_height = page.mediabox[-2:]
        if page_width > page_height:
            continue
        pdf.interpreter.process_page(page)
        # open img
        img = Image.open(image_path).convert("RGB")
        # draw bbox feature is commented
        if boxed_dir:
            draw = ImageDraw.Draw(img)
        crop_idx = 0
        for lobj in pdf.device.get_result():
            if isinstance(lobj, LTTextBoxHorizontal) :
                for line in lobj:
                    if isinstance(line, LTTextLineHorizontal):
                        label_text, points, crop_list = parse_labels(crop_line, line, pdf, img_rate)
                        for text, bbox_label, crop_coor in zip(label_text, points, crop_list):
                            left, upper, right, lower = crop_coor
                            is_valid_txt, diff = is_valid_text(text, pdf_name)
                            invalid_chr_set = invalid_chr_set.union(diff)
                            if right - left < 3 or lower - upper < 3: # trash image condition
                                continue
                            if not is_valid_txt or not text: # OOV unicode 
                                continue
                            cropped_path = cropped_dir / f'{page_num}_{crop_idx}_{text}_.jpg'
                            # print(f"{cropped_path}\t{text}")
                            img.crop(crop_coor).save(cropped_path)
                            cropped_labels.append(f'{cropped_path}\t{text}\n')
                            # page_det_labels.append({"transcription": "label_text", "points": bbox_label})
                            page_det_labels.append({"transcription": text, "points": bbox_label})
                            if boxed_dir:
                                draw_bbox(line, draw, ((left, lower), (right, upper)))
                            crop_idx += 1
        det_labels.append(f"{image_path}\t{json.dumps(page_det_labels, ensure_ascii=False)}\n")
        if boxed_dir:
            boxed_path = boxed_dir / Path(image_path).name
            img.save(boxed_path, "JPEG")
        img.close()
    write_label(directories['label_dir'], cropped_labels, f'rec_{pdf_name}')
    write_label(directories['label_dir'], det_labels, f'det_{pdf_name}')
    return ''.join(det_labels), ''.join(cropped_labels), invalid_chr_set

def convert_and_crop_pdf_images(directories, pdf2jpg_option, pdf_name, 
    pdf2image_bool=True, 
    crop_line_bool=False,
    img_rate=1
    ):
    pdf_path = f"{directories['pdf_dir']}/{pdf_name}.pdf"
    pdf = PDFForTrainData(pdf_path, img_rate)
    converted_dir = Path(directories['pdf_converted_dir']) / pdf_name

    pdf2jpg_option["output_file"] = pdf_name
    pdf2jpg_option["output_folder"] = converted_dir
    # img_rate = 1123 / pdf.page_height
    pdf2jpg_option["size"] = (None, pdf.page_height * img_rate)
    converted_list = get_file_list(converted_dir)
    if pdf2image_bool:
        create_directory(converted_dir)
        converted_list = convert_from_path(pdf_path, **pdf2jpg_option)
    else:
        converted_list.sort()
    images_size = len(converted_list)
    crop_arg = {
        "pdf_name": pdf_name,
        "pdf": pdf,
        "directories": directories,
        "crop_line": crop_line_bool,
        "total": images_size,
        "zipped_arg": zip(pdf.pages, converted_list, range(images_size)),
        "img_rate": img_rate
    }
    # print('cropping')
    det_label, rec_label, invalid_chr_set = crop_pdf_images(**crop_arg)
    print(f'{pdf_name}.pdf done')
    return det_label, rec_label, invalid_chr_set

def batch_convert_pdf2crop(pool_count, pdf_names, pdf2jpg_option, 
    conv_and_crop_opt={
        'pdf2image_bool':False, 
        'crop_line_bool':False,
        'img_rate':1
    },
    directories = {
        'pdf_converted_dir' : 'converted', 
        'boxed_dir' : None, 
        'cropped_dir' : 'cropped', 
        'label_dir' : 'labels',
        'pdf_dir' : 'corpus_pdf'
    }):
    pool = Pool(pool_count)
    results = {pdf_name:pool.apply_async(convert_and_crop_pdf_images, args=(directories, pdf2jpg_option, pdf_name), kwds=conv_and_crop_opt) for pdf_name in pdf_names}
    pool.close()
    pool.join()
    rec_label_list = []
    det_label_list = []
    global excluded_chr_set
    for pdf_name in pdf_names:
        det_label, rec_label, invalid_chr_set = results[pdf_name].get()
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
        excluded_chr_set = excluded_chr_set.union(invalid_chr_set)
    return ''.join(det_label_list), ''.join(rec_label_list)

def write_label(label_dir, label_list, label_name):
    label = ''.join(label_list)
    label_path = f'{label_dir}/{label_name}.txt'
    with open(label_path, 'a', encoding='utf-8') as label_file:
        label_file.write(label)

if __name__ == '__main__':
    pool_count = os.cpu_count()
    # pool_count = 8
    # pdf_names += [f'wind{pdf_index}' for pdf_index in range(10)]
    directories = {
        'pdf_converted_dir' : 'converted', 
        'boxed_dir' : 'boxed', # if None not save boxed image
        # 'boxed_dir' : 'pdf/issue/boxed', # if None not save boxed image
        # 'boxed_dir' : '/mnt/c/Exception/', # if None not save boxed image
        # 'boxed_dir' : '/mnt/c/Exception/', # if None not save boxed image
        'cropped_dir' : 'cropped', 
        # 'cropped_dir' : '/mnt/d/cropped', 
        'label_dir': 'labels',
        'pdf_dir': 'pdf/crawled',
        # 'pdf_dir': 'test_pdf',
        # 'pdf_dir': 'pdf/issue',
        # 'pdf_dir': 'pdf',
    }
    create_directories(directories.values())

    # font, size pdf
    pdf_names = [corpus_pdf_path.replace(f"{directories['pdf_dir']}/", '').replace('.pdf', '') 
    for corpus_pdf_path in get_file_list(directories['pdf_dir'])]
    pdf_names = ['창녕군계획 조례 일부개정계획', 
'2022년 하반기 지방재정 적극집행 추진계획', 
'민선8기 구청장 공약사항 실천계획 보고회 개최 결과보고', 
'고창청소년문화센터 민간위탁 심의위원회 개최', 
'2022년 근골격계부담작업 유해요인조사 용역 결과보고', 
'2022년(1._7.) 남구 옴부즈만 운영상황 보고', 
'결재문서본문 - 2022-10-05T162530.655', 
'공적심사위원회 의결서(생산성대상 유공공무원)', 
'건축물관리 조례 제정 계획 보고', 
'대전광역시 참전유공자 지원 조례 일부개정 계획(안)', 
'2022년 적극행정 직장교육 시행계획', 
'2022년도 제2회 추가경정예산(안) 보고', 
'양주시 리·통·반 설치 및 운영에 관한 조례 일부개정조례안', 
'2023년 본예산 확보 대책보고', 
'수질분석실 임기제 공무원 채용계획', 
'2022년 3분기 금천구 산업안전보건위원회 정기회의 결과 보고', 
'청주시 부동산가격공시위원회 위원 위촉 및 해촉', 
'우포늪생태관 제1,2주차장 CCTV 설치 공사 2023년 예산편성 건의', 
'다함께 청!연!전(淸蓮展)추진 결과 보고', 
'복지사각지대 위기가구 기획조사 실시 계획', 
'실국원 탄소중립 실천과제 보고회 개최 계획', 
'2022년 제2회 진주시 아동친화도시 추진단 회의 개최 계획 보고', 
'중대(산업·시민)재해 발생 대비·대응 매뉴얼 시행', 
'「코로나19 방역대책」예산 성립전 사용 승인', 
'결재문서본문 - 2022-09-30T042902.747', 
'공무국외여행 심사의결서', 
'결재문서본문 - 2022-10-01T035352.194', 
'2022 광주통계연보 추진계획(안)', 
'안면읍 창기리 창고시설(농수산물 보관용)건축신고 관련 군계획위원회 심의상정 검토보고', 
'2022년 제1회 UFEZ 분양가심사위원회 개최일 변경 건의', 
'건축물 현황조사 추진계획', 
'민원실 비상상황 대비 모의훈련 계획', 
'2022년 하반기 「직원 및 구민 헌혈의 날」 운영 계획', 
'2022년 제9차 동해시 조례·규칙심의회 개최계획', 
'2022년 하반기 작업환경측정 실시 계획', 
'『부산진구 부전 청소년센터』민간위탁 추진계획', 
'2022년 가축전염병 특별방역대책 추진계획', 
'2022년 읍면동 주민총회 개최결과 보고', 
'2021시설현대화) 부산평화시장 복도포장공사 및 방송시설 교체 완료보고', 
'2022년 탄소중립 시민실천단 워크숍 개최 계획', 
'「인천광역시 연수구 아동 급식지원에 관한 조례」 일부 개정 최종 계획', 
'2023년 보훈예우수당·참전명예수당 인상계획', 
'결재문서본문 - 2022-10-04T141555.918', 
'2022년 제7차 조례규칙심의회 개최 통보(2022. 10. 4.)', 
'2023년 보육가족분야 당초예산(군비) 편성계획', 
'「양양군 고향사랑기부금 모금 및 운용에 관한 조례」제정 계획', 
'대구광역시 서구 저소득주민 국민건강보험료 및 노인장기요양보험료 지원에 관한 조례 일부개정 계획', 
'2022년 강원도 민주화운동 기념사업 지원 예산 변경사용 요청 검토보고', 
'비정규직근로자 채용 수시 사전심사 결과 보고', 
'「대구광역시 수성구 환경공무직 복무 규칙」 일부개정 계획', 
'2023년 중대재해예방 안전·보건 예산 방침결정', 
'구청장 주재 2023년 주요업무계획 보고 결과', 
'동구 청년 정책 아이디어 공모전 접수 현황 보고 및 심사 계획', 
'소규모 환경영향평가서 협의내용 알림[화성시 서신면 매화리 831-9번지 일원 공장부지 조성사업(㈜선조테크 외 8개사)]', 
'시간선택제임기제공무원(치매안심센터) 채용 계획', 
'2021년 저소득층 추가 국민지원금 국고보조금 집행잔액 반납', 
'2022년 금정구의정비심의위원회 회의 개최', 
'2022년 금정구의정비심의위원회 회의 개최 결과 보고', 
'제9회 사하구 희망복지박람회 개최 계획', 
'부산광역시 기장군 읍·면 복지회관 운영 조례 일부개정 계획', 
'동구 어린이·청소년의회 구성 및 지원관리 업무이관 계획', 
'의원발의 조례안 검토보고(충주시 빈집 정비 지원조례)', 
'해운대구 구정혁신 아이디어 공모 계획', 
'20222023년 도로 제설작업을 위한 제설제 구매계획(안)', 
'증평군 코로나19  대응 현황(9. 25. 현재)', 
'결재문서본문 - 2022-10-04T113442.183', 
'민간인 포상 공적심사위원회 심사 (6)', 
'지방시간선택제임기제 공무원(마급) 임용계획', 
'2023년 저소득 노인가구 건강보험료 지원계획', 
'2022년 제8차 조례ㆍ규칙심의회 심의 계획', 
'「인천광역시부평구 지방공무원 정원 규칙·규정」일부개정 변경 계획(안)', 
'「홍천군 대상포진 예방접종 지원에 관한 조례」일부 개정 계획', 
'공동주택 내 보육시설 국공립어린이집 설치·운영 협약 체결(변경)', 
'환경피해대응 주민건강모니터링 용역 중간보고회 개최 계획', 
'공적심사의결서(2022년도 자활분야 우수지자체 포상)', 
'공적심사의결서(모범장병 유공 등 3개 분야)', 
'2022년 지방재정 적극집행 부서별 집행실적 및 신속 집행 요청', 
'산사태 및 호우피해 수목 정비공사(1차) 시행', 
'결재문서본문 - 2022-10-18T192806.186', 
'2023년 상반기 퇴직준비교육(공로연수) 실시계획', 
'채용실태 정기 전수조사 결과 보고', 
'구리시 복지사각지대 발굴·지원 강화 계획', 
'공적심사위원회 의결서(공무원용)', 
'2023년도 중구 주차장 안전실태조사 추진 계획', 
'제5회 시장배 전국 직장인 이스포츠 대회 포상(상장) 계획', 
'수원시 청소년 기본 조례 일부개정 계획', 
'2022년 강서구 지역사회보장협의체 전담직원 채용 계획', 
'2022년 3분기 회의자료', 
'‘22년 기관보육료지원 어린이집 조리원 인건비 보조금 변경내시 및 4분기 교부건의', 
'부구청장 강조사항 알림[10.11.(화) 정례간부회의]', 
'2022년 제26회 노인의 날 모범노인·노인복지기여자(중구청장) 유공 민간인 표창 대상자 선발 계획', 
'동해시 청년정책위원회 위원 재구성 계획', 
'『제30회 대덕구 통계연보』공표 계획', 
'2022 찾아가는 복지 유공자 표창 계획', 
'대호지면 복지회관 방수공사 추진 건의', 
'결재문서본문 - 2022-09-30T033125.517', 
'김향숙 의원 5분 자유발언에 따른 경력단절여성 지원책 마련에 대한 검토 보고', 
'제17회 부산불꽃축제 종합 운영 지원계획', 
'2022년 제2회 달성군 안전정책실무조정위원회 심의 결과 보고', 
'아동친화도 조사 용역 및 시책 사업 신규 편성안 보고', 
'무라카미 다카시展 전시장 누수 및 항온항습 문제 상황보고', 
'“업무혁신 아이디어 발굴 공장(公場)”개최 계획', 
'대구광역시 북구 구민고충처리위원회의 구성 및 운영에 관한 조례 시행규칙 전부개정 계획', 
'결재문서본문 - 2022-10-04T160809.506', 
'결재문서본문 - 2022-10-14T110435.804', 
'일하는 방식 혁신 아이디어 공모 계획', 
'방문건강관리사업 공무직근로자 공개채용 계획', 
'제2회 영도구 안전관리 실무위원회 심의회의 개최 계획', 
'2022년 제9회 조례·규칙심의회 개최 통보', 
'사상구 정신건강복지센터 민간위탁 적정성 검토보고', 
'결재문서본문 - 2022-09-30T041111.083', 
'2023_2027년 중기지방재정계획 수립 추진', 
'「김포시종합사회복지관」 운영에 따른 수탁자선정심의위원회 개최 계획', 
'대형유통시설 화재예방을 위한 특별안전관리 추진계획', 
'봉화군 복지사각지대 발굴·운영 지원사업 계획(안)', 
'「제3차 전라남도 장사시설 지역수급계획 수립」 연구 용역 추진계획(안)', 
'2022년 제3차 산업안전보건위원회 개최 결과 보고', 
'제8기(2023_2026) 지역보건의료계획 수립계획', 
'군수 지시사항 추진 철저(전직원 공람)', 
'인천광역시 연수구 행정기구 설치 조례 시행규칙 일부개정계획(안)', 
'대흥동 행정복지센터 청사 냉난방기 교체공사 추진계획', 
'2022년 4분기 희귀질환자 의료비지원사업 보조금 교부 결정 통지', 
'사회복지사 등의 복지증진 및 처우개선 종합계획', 
'결재문서본문 - 2022-09-30T091332.310', 
'철원군 아동보호 및 복지증진에 관한 조례 일부개정 계획', 
'2023년 자체사업 (기존·신규·증액) 예산반영 계획보고', 
'2022 군산시「청년의 날」행사 결과보고', 
'2022년 생물테러 대비·대응 대규모 모의훈련 실시계획', 
'2022년 8월 일자리종합센터 운영 실적 보고', 
'2022년 하반기 지방세입 징수대책 보고회 계획', 
'영도 경제기반형 도시재생사업 추진계획 보고', 
'「제5기 지역사회보장계획 수립 연구용역」최종보고회 결과 보고', 
'2022년 제6차 조례규칙심의회 개최 통보(2022. 9. 26.)', 
'2022년 소형어선 유류비 지원사업 보조금 지급(2분기) 검토보고', 
'가림막 및 휴대용 영상음성기록장치 구입 계획', 
'2022년 4분기 희귀질환자 의료비지원사업 보조금 교부', 
'지적재조사위원회 심의회(서면) 결과 보고', 
'2022년 우수시책 발굴 최종심사 결과 보고', 
'2023년 노인여가복지시설(경로당) 예산편성(안) 보고', 
'2022년 『공공디자인&#10625;유해환경개선옥외광고물 분야』업무추진실적 평가 및 포상 계획', 
'환경미화원 휴게실 및 청소차 차고지 신축 추진계획', 
'『성남시 소비자정책심의위원회』위원 위&#65381;해촉 보고', 
'「제11회 굿네이버스 누리교육그림그리기대회」참여 우수아동에 대한 상장 시상 계획', 
'찾아가는 어르신 인지력 케어 서비스 운영 계획', 
'직원 건강증진을 위한 청사 체력단련실 장비 구입계획', 
'결재문서본문 - 2022-10-04T140715.782', 
'제5기 함평군 지역사회보장계획 수립용역 최종보고회 개최 계획', 
'『2022년 재난대응 안전한국훈련 기획회의』 결과 보고', 
'연제구 의정비심의위원회 개최 결과 보고', 
'2022년 부산 숲체험한마당 행사 추진계획', 
'부산광역시 남구 주민투표 조례 일부개정 계획', 
'2022년 제3차 용역과제심의위원회 개최 계획', 
'9월 민원 처리상황 및 운영실태 확인ㆍ점검 결과 보고', 
'『찾아가는 보건복지서비스 활동 전시회』개최 계획', 
'결재문서본문 - 2022-10-18T193020.376', 
'2023년 보건의료원 의료지원과(원무팀) 기간제근로자 채용 계획', 
'2022 다문화가족 페스티벌 지원계획', 
'2023년도 기간제근로자 채용 사전심사제 운영계획', 
'제6회 라라라 페스티벌 진행 보고회 개최결과', 
'민선8기 출범 100일 직원 정례조례 개최 계획', 
'장애인주간보호시설 이용장애인 및 종사자 정원 변경(안)', 
'「대구광역시 동구 주민투표 조례」일부개정 계획', 
'2022년 문화예술관련 전국대회 상장지원 검토보고서', 
'2023년 보육교직원 장기근속수당 확대 지원 계획', 
'공적심사의결서(전통시장 활성화 유공 표창)', 
'스마트시티 혁신기술 발굴사업 착수보고회 개최 계획(안)', 
'도곡온천지구 활성화 방안 용역 시행', 
'민선8기 구청장 공약사항 실천계획 및 목록 확정 보고', 
'1530 건강걷기사업 운영 민간위탁 재위탁 계획', 
'2022년 제6회 지방재정계획심의위원회 개최 결과', 
'근골격계 부담작업 유해요인조사 실시계획(안)', 
'결재문서본문 - 2022-10-18T170338.068', 
'결재문서본문 (90)', 
'사회복지포럼 개최 계획', 
'2022년도 희망복지지원단 우수사례집 제12호「아름다운 동행」제작 계획', 
'『민원처리법&#985173; 개정 관련 민원담당자 보호(지원) 계획 보고', 
'제53회 난계국악축제 영동군 난계국악단 공연계획', 
'충남공동근로복지기금 출연금 예산반영 검토보고', 
'간부공무원 탄소중립ESG 교육계획', 
'예산의 변경사용 검토 보고', 
'2023년도 환경관리원 신규채용 계획', 
'여수시도시관리공단 임원(이사장) 임기 시작일 변경 알림', 
'2023년 재난관리자원 비축·관리계획', 
'노숙인 등의 복지사업 담당 공무원 국외연수 계획', 
'제44차 한국동물위생학회 학술발표대회 결과보고', 
'시간선택임기제공무원 근무기간 연장계획', 
'2022년 추석명절 사회복지시설 및 저소득층 위문 계획(안)', 
'물질안전보건자료(MSDS) 조사 및 관리 계획', 
'울산북구장애인복지관 민간위탁 적정성 검토 보고', 
'2022년 6급 중간관리자 교육계획', 
'2022년 제4회 「부천시 기부심사위원회」심사 결과보고', 
'누(리고)나(누는)동네 더불어마을 쉼터 조성사업 주민설명회 개최 계획', 
'자치법규 일제정비 추진에 따른 조례일괄개정 계획', 
'2022년 불법 주·정차 단속 고정식 CCTV 설치 계획(안)', 
'결재문서본문 - 2022-10-14T163303.939', 
'「시흥시 통·반 설치 조례 시행규칙」일부 개정 계획', 
"기획공연 '김영임, 김용임이 함께하는 희희낙락' 추진계획 (2022년 방방곡곡 문화공감 사업)", 
'「제43회 흰 지팡이의 날」장애인 복지 유공자 표창 계획(수정)', 
'민간인 포상 공적심사위원회 심사 (5)', 
'2022년 보건소 코로나19 대응인력 한시지원 보조금 교부결정 통지(2차, 일반회계)', 
'종량제봉투 등 판매소 공급체계 개선 직영 추진 계획', 
'나주시 자치법규 공포', 
'「2022 대한민국 지방자치경영혁신 엑스포」참가 계획', 
'계룡시 어르신 대상포진 예방접종 지원에 관한 조례 제정 계획(안)', 
'2023년도 노인복지기금 운용 계획', 
'제37회 시민의 날 기념식 및 체육대회 개최계획 보고', 
'2032 주거종합계획 및 주거실태조사 용역 시행계획', 
'부산광역시 입법평가위원회 구성(변경) 건의', 
'2022년 대한민국 안전大전환 추진상황 보고회 개최 계획', 
'2022년 9월 보훈명예수당 지급', 
'2022년 제10회 지방보조금심의위원회 서면심의 개최', 
'삼락·화명생태공원 신규 파크골프장 개장 계획보고', 
'2022년 찾아가는 보건복지서비스 동 운영 평가 계획', 
'2022년도 하반기 채용 대행 용역 추진 계획(안) 보고', 
'2022년 하반기 수영구교육행정협의회 협의안건 검토 보고', 
'2030 부산세계박람회 구민 홍보단 발대식 현황 및 향후운영 방안', 
'2022. 수원시 일자리박람회 개최 계획', 
'2023년도 당초예산 정책사업 예산편성계획', 
'2022년 지식커뮤니티 워크숍 개최 계획', 
'동구 의료급여 심의위원회 개최(2022년 제8회)', 
'2022년 공공부문 아동학대예방 사이버교육 추진 계획', 
'본원 폐수처리시설 초음파 수위계 교체 시행', 
'정수물품 정수 배정 계획(2023년 당초예산)', 
'‘22년 7회 공동위원회 및 16회 건축위원회 변경 개최 건의', 
'아동청소년과 한시임기제공무원 채용계획(안)', 
'결재문서본문 - 2022-10-01T064615.268', 
"'23 벼재배면적 감축 논타작물재배사업 추진계획", 
'건강체력증진센터 시간선택제임기제 공무원(마급) 임용계획', 
'「태안군 공무원 행동강령 규칙」 일부 개정 계획', 
'장애인복지위원회 위원 해촉 및 위촉 건의', 
'시간선택제임기제공무원 도시계획전문관 채용계획', 
'2023년 도시관리분야 관련 본예산 편성계획 보고', 
'『전주시 국가보훈대상자 보훈수당 지원 조례』일부개정 계획', 
'부산광역시노인종합복지관 민간위탁(재위탁) 추진계획', 
'건축위원회 심의 효율적 운영 방안 검토 보고', 
'「수원시 국가보훈대상자 예우 및 지원에 관한 조례」일부개정(안) 계획', 
'2022년 제5회 지방임기제공무원 채용계획', 
'2022년 진주시 재난관리기금 운용 심의위원회 (제7회-서면심의) 개최 결과보고', 
'사상구 정신건강복지센터 운영 민간위탁 재계약 추진 계획', 
'『2022년 제22회 소래포구축제』보령시 대표단 방문계획', 
'2023년 지역사회보장협의체 사무국 운영 예산 편성 관련 검토보고', 
'2022년 제3회 동구 도로관리심의회 개최 건의', 
'달홀목욕탕 기간제근로자 채용 재공고 계획', 
'명예시민증 대상자 추천계획', 
'2022년 강화군 의정비심의위원회 위원 선정 결과 및 회의개최 계획 보고', 
'2022년도 노인요양시설 인권지킴이 운영 계획', 
'2023년 산림과 기간제근로자 임금 단가 산정 계획', 
'워케이션센터 우수사례 현장답사 결과보고', 
'2022 재난대응 안전한국훈련 기본계획', 
'제278회 안산시의회 제1차 정례회 부의안건 제출', 
'홍천군 사회복지사 등의 처우 및 지위 향상에 관한 조례 일부개정 계획(안)', 
'2022년 건설공사장 안전점검 결과 보고', 
'사회복지법인 군포시사회복지협의회 설립허가 신청에 따른 검토 보고', 
'2023년도 지방세연구원 출연금 출연 계획(안)', 
'2022년 제2회 규제개혁위원회 개최 결과 보고', 
'2023년 소상공인 지원 분야 당초예산 편성 계획안', 
'2022년 제2회 통합재정안정화기금운용심의위원회 심의 계획', 
'2022년 제5회 조례규칙심의회 서면심의 건의', 
'영암군 안전보건관리(총괄)책임자 변경 선임', 
'정관아쿠아드림파크 정상화 계획 검토보고', 
'시간선택제임기제 공무원 채용 계획', 
'2022년 드림스타트 보육분야 아동통합사례관리사 채용 계획', 
'공적심사의결서(2022년 상반기 재정집행 추진 유공)', 
'2023년 기간제근로자 채용 사전심사제 운영계획', 
'고위공직자 대상 반부패 청렴수준 자기진단 실시 결과보고', 
'고양시 아동친화도시 추진위원회 구성 계획(안)', 
'결재본문 (4)', 
'맞춤형 복지카드 적립금 운영 계획', 
'공적심사위원회 의결서(2022-37)', 
'2023년 옥정신도시 초미세먼지 전용 측정소 설치 계획 보고(변경)', 
'연제구국민체육센터 시간선택제 임기제공무원 채용 변경 계획', 
'자매결연도시 마포구「제29회 마포구민의 날」 참석 계획', 
'2023_2027년 중기지방재정계획 수립계획', 
'세종시 종합주거복지센터 설치 업무협약 체결 계획', 
'2022. 장애인직업재활시설 종사자 충원 계획(안)', 
'대덕구청 직장어린이집 위탁기간 만료에 따른 민간위탁기관 선정심사위원회 개최 계획', 
'규제혁신·적극행정 역량강화 동래아카데미 개최 계획', 
'결재문서본문 - 2022-10-04T151340.124', 
"'22년 제2회 市 지역수자원관리위원회 개최 결과", 
'결재문서본문 - 2022-10-05T164004.377', 
'2022년 지역사회통합건강증진사업 보건소장 과정 교육출장 보고', 
'2022년 9월 민원처리상황 확인·점검 결과 보고', 
'선진교통체계 기반확충을 위한 2023년 당초예산 편성계획(안)', 
'Scale Up 참여업체-건설대기업 간담회 개최 결과보고', 
'결재문서본문 - 2022-10-04T125523.728', 
'2022년도 단체보장성보험 가입계획', 
'대외협력특별보좌관(전문임기제) 채용 계획', 
'[외부출강신고서]외부강의_회의 등 신고서(윤승재, 2022.09.27)', 
'2022년 계룡시 의정비심의위원회 개최 결과 보고', 
'2022년 제9차 안성시의료급여심의위원회 개최 계획(안)', 
'2022년 제3분기 제주시 산업안전보건위원회 회의 개최 계획', 
'계양구 주거복지센터 설치 기본계획(안)', 
'2022년도 제7차 용역과제심의위원회 개최 계획(서면)', 
'ICT 기반 건강관리서비스 대국민 인식 확산을 위한 언론홍보 계획', 
'2023년 사회복지시설 종사자 처우개선비 지원 계획', 
'2021년 사망원인통계 주요지표 결과보고', 
'자치법규 및 행정규칙 공포·발령', 
'도정영상 편집장비 물품구입 수의계약 의뢰', 
'부산광역시 주택시장 모니터링단 정기보고회(5회) 개최 알림', 
'여주시 소상공인지원센터 2022년 사업계획서 및 민간위탁금 교부 검토 보고', 
'보육교사 건강장해 예방 매뉴얼 개발에 따른 외부 집필진 계약 체결', 
'군산시 결산검사위원 선임ㆍ운영 및 실비보상 조례 일부개정 계획', 
'2023년도 기간제근로자 채용 사전심사제 운영계획(안)', 
'제4차 무주군 의료급여심의위원회 개최', 
'2022년 하반기 세외수입 체납액 일제정리 추진 계획', 
'22년도 비상대비 자원관리 유공 표창 대상자 추천 검토 보고', 
'경상북도 공유재산 관리조례 일부개정조례안 조례 규칙 심의회 결과', 
'민원처리 중간소통실적 제출 및 민원전화 원스톱연결점검 통보(전직원 공람)', 
'2022년 하반기 구제역 백신 일제접종 계획', 
'지속가능한 미래를 위한 탄소중립 특강 계획', 
'2022년 제3회 교통국 제1공적심사위원회 개최 계획', 
'2022년 9월 어린이집 만5세아(‘16년생) 필요경비 지급', 
'2023년 동 자원재활용 경진대회 폐지 검토 보고', 
'결재문서본문 - 2022-10-14T112010.380', 
'남면 달산리 숙박시설 건축허가 관련 군계획위원회 심의상정 검토보고', 
'조례규칙 심의회 의결서(12회)', 
'결재문서본문 - 2022-09-30T071611.483', 
'2023년도 증평군청소년상담복지센터 운영을 위한 당초 예산확보 계획', 
'휴일근무 신청', 
'2023년 기간제근로자 사용승인 결정(안)', 
'2022년 사회복지관 우수직원 시장 표창 계획', 
'양주 종합사회복지센터 설계공모 추진계획 보고', 
'2022년 제27차 건설산업기본법(건설업) 위반 업체 행정처분 검토보고', 
'2022년 제1차 장애인복지위원회 서면 회의 개최 계획', 
'수시 제9차 지방재정계획심의위원회 회의(심의)결과 알림', 
'용인환경센터 잉여폐기물(비목재파쇄물) 외부위탁(4차) 처리계획 검토보고', 
'부산광역시 동구 조례 입법평가 조례 제정 계획', 
'2023년 농촌지원과 기간제근로자 인력운용계획', 
'「완도군 청원경찰 복무 규정」 일부개정 계획', 
'고흥군 공무직 및 기간제근로자 관리 규정 일부개정(안)', 
'결재문서본문 - 2022-10-18T115325.780', 
'2022년 제2회 지방재정공시위원회 개최 결과보고', 
'비정규직근로자 채용 정기 사전심사제 운영 계획', 
'코앤핑이비인후과의원 이웃돕기 성품 전달식 개최 보고', 
'BTS 콘서트 개최 대비 도시환경정비 추진 계획', 
'안산시 기간제근로자 관리 규정 일부개정 계획', 
'제576돌 한글날「한글발전유공 표창」계획', 
'2022년 우수 이·통장활동 유공자 표창 계획', 
'양주시체육회·장애인체육회 후생복지비 지원 검토 보고', 
'2022년 구리시 청소년 진로박람회 운영 세부추진계획', 
'결재문서본문 - 2022-10-05T085342.419', 
'2023년 네이버 브랜드검색 활용 홍보 추진 계획', 
'결재문서본문 - 2022-10-18T170539.086', 
'2022 부산국제의료관광컨벤션 개최 계획', 
'신안군의회 조례안 부의안건', 
'2022년 의료급여사업 유공 공무원 표창 대상자 선발계획', 
'2022년 하반기 지방세 체납액 특별정리 추진계획', 
'수원 세모녀 비극 관련 복지사각지대 발굴 현황 및 추진계획', 
'국공립어린이집 재난안전보강공사 추진 계획', 
'코로나19 대응 일일 추진 상황보고 [8. 29.(월)]', 
'- AI·IoT 기반 어르신 건강관리사업 - 시간선택제임기제 공무원 신규채용 검토보고', 
'이정구선생묘 월사집목판 관람환경 개선공사(건축토목)', 
'태안군 청원심의회 운영 규정 제정 계획', 
'공동주택 특별감사 추진계획', 
'2022년 합천군 농축산물 가격안정기금          운용 계획 심의회 개최 계획(안)', 
'『북부권 제2종합사회복지관 건립 특별조정교부금』성립전 예산 사용계획 보고', 
'2022. 제14회 시흥시평생학습축제 종합 추진계획', 
'「군포시 주거 정비 지원센터 설립 및 운영조례」제정계획', 
'수산종자연구소 기간제 근로자 채용계획[안]', 
'결재문서본문 - 2022-09-30T124923.730', 
'2022. 8월 동 지역사회보장협의체 운영현황 보고', 
'2023_2027년도 중기공유재산관리계획 수립 계획', 
'2022년 제2회 지방재정공시심의위원회 개최 계획', 
'대전광역시 중구 법제사무처리 규정 일부개정규정안', 
'2022년 혁신 우수사례 경진대회 개최 계획(안)', 
'결재문서본문 - 2022-10-01T055656.148', 
'폐기물 불법배출 단속 공무직 근로자 채용 계획', 
'제97호 의회소식지 제작·배부 계획', 
'건설공사 관계자 사이버 안전교육 계획', 
'지역맞춤형 통합하천사업 수요조사 제출 관련 보고', 
'2023년 본예산 반영을 위한 유니세프 아동친화도시 사업 검토보고', 
'2022년 9월 민원처리현황 및 운영실태 점검 결과보고', 
'「평생교육 중장기 발전계획 수립」연구용역 중간보고회 개최 계획', 
'2023년 국가보훈대상자 예우 및 지원계획(안)', 
"‘제27회 부산국제영화제' 안전관리실무위원회 결과보고", '시간선택제임기제공무원 채용 연장 계획', 
'바다역 여행자센터 신축 기본 계획(안)', 
'2022년 9월 국민신문고 민원처리상황 점검 결과보고', 
'제8기 지역보건의료계획 수립 추진 계획', 
'삼척시 안전관리실무위원회 개최(9월2차)결과보고(서면)', 
'2022년 재난대응 안전한국훈련 기본계획', 
'무주군 지방규제혁신 TF팀 구성 및 운영 계획', 
'(정책) 2022년 제1회 용역과제심의위원회 개최 계획', 
'민원처리상황 확인 및 점검결과 보고', 
"'23년 보육시설 종사자 처우개선비 등 지원 검토 보고", 
'금정구 성별영향평가위원회 위원 정비 계획', 
'민간인 포상 공적심사위원회 심사 (3)', 
'원전해체산업 발전 유공 장관 표창 후보자 추천 검토보고', 
'2023년 방문건강팀 예산확보 계획', 
'2022년 3분기 신속집행 및 소비투자 부진부서 대책보고회 개최 계획', 
'2023년도 재난관리기금 운용계획(안) 재난관리기금 운용심의위원회 개최 계획', 
'기부심사위원회 심의 계획(서면심의)', 
'식물원 주변 인프라구축 공공용지취득 예산편성 추진계획', 
'태백시 통반 행정구역 조정계획', 
'공사 시행 건의 [2022년 견우천 지류(6-2) 복개구조물 보수공사]', 
'이천시시설관리공단 제89차 이사회 승인요청사항 검토결과 보고', 
"'22년 제2차 재난관리기금운용심의위원회 개최계획", 
'2022년 해운대구 적극행정 우수사례 경진대회 추진계획', 
'일반임기제 직급 조정 및 채용계획 변경 검토보고', 
'지방시간선택제임기제 공무원 채용계획(청소년특화시설운영분야)', 
'2022년 제9차 생활보장위원회 결과보고', 
'풍세보건지소 건강증진장비 구입 계약심사(원가심사) 결과 보고', 
'2022년 하반기 행정구역 정비 조례 개정계획', 
'시정 홍보 확산을 위한「2022 직원 영상 공모전」개최 계획', 
'2023년도 사회적경제 분야 주요사업 추진계획 보고', 
'2022-2023절기 인플루엔자 예방접종 추진계획', 
'「보령시 아동 급식지원 조례」일부개정 계획', 
'2022년 정보보안 관제 사업 용역 관련 낙찰자 결정 및 계약체결 보고', 
'2022 치매극복 건강한마당 개최 계획', 
'결재문서본문 (154)', 
'메디부산 2022! 시민건강박람회 유공 포상 대상 선정보고', 
"'22년도 하반기 폐광산 주변 환경오염도 조사계획", 
"'북구를 만나다' 관광영상·관광캐릭터 공모전 최종 선정 결과보고", 
'2022년 3분기 구청장 지시사항 추진상황 점검결과 보고', 
'「부산광역시 사하구 아동 급식 지원 조례」일부 개정 계획', 
'2022년 도지사 민간인 포상(상장) 계획(2022 전주비빔밥축제)', 
'「2022년 계족산성 긴급보수공사」추진계획', 
"'22년도 국가안전大전환 추진에 따른 상수도분야 집중안전점검 결과 보고", 
'『덕신소하천 정비공사』 총괄2회 및 2차분1회 설계변경 계획 보고', 
'결재문서본문 - 2022-10-04T172051.183', 
'대한민국 안전大전환 `22년 집중안전점검 중간보고회 개최건의', 
'시간선택임기제 마급(금연단속원) 신규(계약만료)채용 계획(안)', 
'2022. 10. 31.기준 5급이하 지방공무원 정기 근무성적평정 실시계획', 
'2022년 제4회 대전광역시 동구 도시계획위원회(분과위원회) 심의(서면) 추진계획', 
'아동보호전담요원 임기제공무원 채용 계획', 
'「강릉시 착한가격업소 지원에 관한 조례」제정 계획', 
'2023년 서면 당초예산 확보계획', 
'인천광역시부평구 공무원 행동강령 규칙 일부 개정 계획', 
'결재문서본문 - 2022-10-14T142255.624', 
'공적심사위원회 공적심의 의결서(민간인)', 
"'22년도 긴급복지 신고의무자 교육 추진계획", 
'2022년 제19회 조례규칙심의회 심의의결서', 
'2022년 제9회 의왕시청소년진로박람회 안전 관리 및 지원 계획', 
'공무원노조 북구지부「조합원 단체 영화관람」행사 동향보고', 
'치매관리팀 기간제 충원계획(안)', 
'2022년 부안 문화재 야행 근무자 명단 및 대체 휴무 실시', 
'2022년 제5회 규제개혁위원회 개최 계획', 
'결재문서본문 - 2022-09-30T110823.252', 
'저소득세대 건강보험료 지원 관련 2023년 소요예산 확보 검토 보고', 
'달홀목욕탕 기간제근로자 채용공고 계획', 
'기간제 근로자 채용계획(도시농업사업)', 
'키르기스스탄 이식쿨주와 업무협약 체결 계획', 
'발달장애인 주간활동서비스 방문 홍보계획', 
'2022년 제7회 건축,경관 공동위원회 및 제16회 건축위원회 개최 알림', 
'제23회「사회복지의 날」유공자 표창 계획', 
'동구 지역사회보장협의체 대표협의체 위원 위·해촉 건의', 
'강릉아레나 1층 바닥면 구조안전진단용역 결과 보고', 
'2022 부안노을아트페스티벌 근무자 대체휴무 및 초과근무인정 실시계획', 
'2022 세계뉴스미디어총회(WNMC) 참가 출장', 
'의정비심의위원회 위촉식 및 회의 개최', 
'2022년 추석 명절 종합대책 추진계획', 
'공원 내 어린이물놀이시설 추진계획', 
'2023년도 예산의 성과계획서 작성 계획', 
'구)대사동 행정복지센터 및 청사 제2별관 활용방안 검토보고', 
'2022년 제8회 의료급여 심의위원회 개최 결과 보고', 
'결재문서본문 - 2022-10-04T144627.229', 
'복지시설팀 2023년 복지시설 사업 및 본예산 편성 계획(안)', 
'지역축제 안전관리계획 심의 결과 보고', 
'결재문서본문 - 2022-10-04T163549.000', 
"제4기('19_'22) 영암군 지역사회보장계획의 2022 연차별 시행계획 이행점검 자체평가 모니터링 계획(안)", 
'고향사랑 기부제 운영 예산편성 검토보고', 
'2022년 제3회 적극행정위원회 개최 계획', 
'「수원시 법정보호종 및 8대 깃대종 포스터 그리기 대회」수원시장상 포상 계획 보고', 
'「저소득층 한시 긴급생활지원금」지급 결과 보고', 
'수시 제9차 지방재정계획심의위원회 회의(심의)결과 보고', 
'구보편집 일반임기제 공무원 채용계획', 
'부산의료관광 동남아 OTT플랫폼 광고 계획', 
'예천군 군세 징수 조례 시행규칙 일부개정규칙안', 
'익산시 지방일반임기제공무원 채용 계획(본문)', 
'연수구 의료급여 심의위원회 개최', 
'인천광역시 중구 기부자 예우 및 기부심사위원회 운영에 관한 조례 일부개정 계획(안)', 
'민속예술관 관리·운영 민간위탁 성과평가 결과보고', 
'아라천 디자인큐브 재위탁 운영 추진계획', 
'춘천시 직영 오수펌프장 관리대행용역 추진계획', 
'2022년 9월 민원처리 운영실태 점검결과', 
'저소득층 한시 긴급생활지원금 최종 지급실적 결과보고', 
"2023년('22년 실적) 제4회 시군평가 대응 보고회 개최 계획", 
'부동산가격공시위원회 심의 결과 보고(제2022-21호)', 
'공공부문 비정규직 채용 사전심사제도 운영 계획', 
'중구 의정비심의위원회 위촉 및 개최 계획', 
'인천광역시 미추홀구 어린이급식관리지원센터 민간위탁 기관 선정 추진계획', 
'「인천광역시부평구 규제혁신TF」구성·운영 계획', 
'전라북도 공공디자인 진흥위원회 개최계획', 
'장애인복지 증진을 위한 업무협약 추진 계획', 
'2022년 제4회 함양군 옥외광고발전기금심의위원회 서면심의 결과보고', 
'관리전환 계획 보고', 
'2022년 제6차 부평구 보육정책위원회 개최결과', 
'국공립어린이집 위탁운영체(자) 선정 계획', 
'「춘천사랑 기부금 모금 및 운용에 관한 조례」제정 계획', 
'동 지역사회보장협의체 위원 해촉 계획', 
'공적심사의결서(전통시장 활성화 유공)', 
'조례 용어의 일괄 정비를 위한 조례 제정 계획', 
'부동산가격공시위원회 심의 결과보고', 
'재난문자방송 송출판단회의 보고(2022.9.27.) - 코로나19 확진자 일일 발생현황(365명)', 
'제4회 동구 사회복지의 날 기념 유공자 표창 계획', 
'공공갈등관리 역량강화『공론화를 통한 갈등해결』운영계획', 
'2023년 사회복지관 운영을 위한 본예산 확보 계획', 
'결재문서본문 - 2022-10-05T144651.819', 
'「서부권 농기계 임대사업장 건축공사」 중지해제 및 변경계약 체결 알림', 
'사상구 정신건강복지센터 민간위탁 운영 성과평가 계획', 
'2022년 제2차 규제개혁위원회 심의 결과', 
'2023_2026년도 의왕시 의정비심의위원회 구성 및 운영계획', 
'2023년도 재단법인 달서문화재단 출연 계획(안)', 
'결재문서본문 - 2022-09-30T110356.541', 
'읍.면 지역사회보장협의체(4기) 위원 변경 위촉 알림', 
'부산중독관리통합지원센터 운영 민간위탁 재위탁 계획', 
'2022년 북구 지역복지박람회 운영 지원계획', 
'2022년도 환경미화원 신규채용 계획(안)', 
'2022년도 제1회 안전정책실무조정위원회 개최 결과 보고', 
'- 2022년 군포시 예비군 -통합방위 태세 확립 유공자 표창 계획', 
'서구 에코센터(재활용선별장) 공무직 채용 계획', 
'울진군 공유재산관리조례 일부 개정 계획', 
'부산광역시 고령친화산업정책심의위원회 위원 위·해촉 검토보고', 
'양천사랑상품권 발행 계획(2차)', 
'결재문서본문 - 2022-10-04T110756.556', 
'2022년 3분기 산업안전보건위원회 및 노사협의회 개최계획', 
'2022년 이천시노동자종합복지관 민간위탁금 지원 검토 보고', 
'식품위생 모범영업주 포상대상자 검토보고', 
'‘22년 제2차 재난관리기금운용심의위원회 결과보고', 
'2022년 제1회 농지위원회 심의 검토 보고서', 
'당진시 재정계획 및 재정공시심의위원회 심의 계획', 
'고창군사회복지시설 제15회 개관기념 복운축제 사회복지유공자 표창 계획', 
'「9. 6. 제11호 태풍(힌남노)」로 인한 사유재산(주택) 피해 조사결과 및 재난지원금 지급에 따른 보고', 
'태안군민대상 조례 일부개정 추진계획', 
'노후 어린이놀이시설 정비 복구계획', 
'도로관리원 신규채용 계획', 
'결재문서본문 - 2022-10-04T143340.286', 
'산모&#61598;신생아 건강관리 서비스 본인부담금 전액지원 변경계획', 
'공적심사위원회 의결서(2022-38)', 
'2022년도 환경미화원 단합대회 개최 계획', 
'2023년 지적재조사 조정금 예산편성 계획', 
'서부산의료원 설립 관련 지역주민 등 설문조사 계획', 
'결재문서본문 - 2022-10-04T175447.825', 
'민간인 포상 공적심사위원회 심사', 
'연수구 장애인복지시설 신축 및 이전 계획 4차 변경(안)', 
'「여성 1인 가구 안심홈 방범세트 지원」예산 성립전 사용 승인', 
'사상구 의료급여심의위원회 심의 개최 계획(2022년 9차)', 
'어린이보호구역 시종점 정비계획', 
'민선8기 핵심과제 구민보고회 개최 계획', 
'금정구 맞춤형 인구정책 리서치 및 리빙랩 추진계획', 
'2023년도 보건소 자체사업 추진계획', 
'공적심사의결서(2022년 장애인직업재활유공자 복지부 포상추천)', 
'2022년 안성문화도시 100만원 해봄실험실 오리엔테이션 개최 계획(안)', 
'2023년 본예산 편성 보고(녹지조경팀)', 
'(재)영화의전당 2022년 제5차 직원 공개채용 사전협의 검토 보고', 
'부곡4동 작은도서관 조성사업 명시이월 검토보고', 
'결재문서본문 - 2022-09-29T203658.494', 
'고향사랑기부금 모금 및 운용에 관한 조례 제정 계획', 
'「울주군 지역치안협의회 설치 및 운영에 관한 조례」일부개정 계획', 
'2023년 사이버보안관제센터 실시간관제 및 정보보안 컨설팅 용역 계획(안)', 
'2022년 제3차 산업안전보건위원회 회의 결과보고', 
'2023년 서면 의용소방대 사무실 수리·수선 계획', 
'「동해시 사무전결 처리규칙」 일부개정 계획', 
'시립합창단 수석단원 특별전형 계획', 
'2022년 제2회 구리시 의정비심의위원회 회의 결과 보고', 
'2022년 누리과정 보육료 예탁금 지급(3차)', 
'2022년 제3회 성남시 감정평가선정위원회 개최 건의', 
'주민친화 하천기술 발굴을 위한 선진지 방문계획', 
'재활용품 수집그물망 구입 계획 보고', 
'제21회 동래구장애인복지증진대회 지원 계획', 
'중간보고회 개최 결과보고', 
'2023년도 옥외광고발전기금 운용계획(안) 보고', 
'『부산시 지방하천 종합정비계획 수립용역』용역기간 연장 보고', 
'금정구 인구정책 아이디어 공모전 추진계획', 
'결재문서본문 - 2022-09-30T140643.652', 
'2023_2027년 중기지방재정계획(안)', 
'2022년 부패방지 청렴문화 주간 운영 계획', 
'「수원시 고향사랑 기부금 모금 및 운용에 관한 조례」제정 계획', 
'민선8기 구청장 취임 100일 맞이『클린진』추진 계획', 
'우수이용자 표창계획(안)', 
'결재문서본문 - 2022-10-04T161507.850', 
'단체민원 접수에 따른 답변 (인창1로 부영아파트 앞 신호등 및 횡단보도 이전 반대)', 
'고향사랑기부금 모금 및 운영에 관한 조례 제정 계획', 
'문화체육국 분장사무 전결권 정비 결과 보고', 
'2022년 경로당 정부양곡비 지급(9월)', 
'『2022년도 수성구 제안공모』제안심사위원회 구성 및 심사계획', 
'지역보건의료계획 수립 연구용역 계획', 
'「인천광역시 중구 긴급복지지원 운영에 관한 조례」일부개정 계획', 
'민선 제8기 구청장 공약사업 실천계획서(행복가정과)', 
'부산광역시 부산진구 의정비심의위원회 제2차 회의 개최 계획', 
'의정비심의위원회 개최 계획', 
'민간인 포상 공적심사위원회 심사 (4)', 
'2022년 국민정책디자인과제 아이디어 워크숍 개최 계획', 
'「청년해방구 AREA 051」지원 계획', 
'(구)장애인복지회관 시설개선 및 장애인편의증진기술지원센터 인력지원 계획', 
'어촌뉴딜사업 지방경비부담 비율 조정에 따른 예산 편성 보고', 
'마스크 착용 의무화 행정명령 재발령(안)', 
'2207차 의료급여 심의위원회 심의계획', 
'스토리가 있는 「충북 관광사진 공모전」 개최 계획', 
'2022년 의정비심의위원회 위촉 및 회의개최 계획(안)', 
'사회복지국 정기 근무성적평정 실시계획', 
'2022년 영유아 보육료 예탁금 지급(3차)', 
'2022년 9월중 민원처리상황 점검 결과 보고', 
'[품의]2021년 긴급복지 국비 집행잔액 반납', 
'구내식당 친환경 농산물 소비 촉진 추진계획', 
'2022년도 제3회 재정투자심사위원회 개최 계획', 
'2023년 보건소 공용차량 구입 계획', 
'2022년 정기 위험성평가 결과 보고', 
'공적심사위원회 의결서(2022-35)', 
'2022년 서부권역 소규모 하천정비사업(3회추경) 실시설계용역 시행', 
'「울주군 주민투표 조례」일부개정 계획', 
'2022년 소셜벤처 경연대회 우수자 시장 포상 검토보고', 
'옥동_농소1 도로개설공사 전면책임감리용역 설계변경(제9회) 시행', 
'2023년 종합사회복지관 운영관리 계획', 
'2022년 보건소 검사요원 감염병 병원체 검사교육 계획', 
'2022년도 맞춤형복지기금 집행계획(안)', 
'제10회 한국수산업경영인 전라남도대회 참석 보조금 지급', 
'제27회 대덕제 대구 앞산 축제 교통통제 용역인력 관리 운영계획', 
'2022년 9월 민원처리실적 보고', 
'`22년 환경기초시설 탄소중립프로그램 태양광 설치공사 추진계획', 
'지방시간선택제 임기제 공무원(흡연단속) 채용 계획(안)', 
'결재문서본문 - 2022-09-30T043104.639', 
'민주평통 대전서구협의회 청소년 통일공감 미디어 콘텐츠 공모전 상장수여 계획', 
'미추홀구 신청사건립사업 추진 현황 정기보고(9월)', 
'2023년도 기간제근로자 채용 사전심사 결과보고', 
'`22년 주거복지분야 정부포상 관련 국토부 출장 결과보고', 
'2023년도 사회복지기금 운용 계획(안)', 
'2022년 무안군 군정발전 아이디어 공모전 개최 계획', 
'공적심사의결서(민간인 and 시군 공무원)', 
'2022년 현업업무종사자  특수건강진단 실시계획(법적의무)', 
'多이로운 익산, 모두를 위한 보석박물관 사업 위탁사업비 교부 계획', 
'영월군 군세 징수 조례 시행규칙 일부개정 계획', 
'제2회 금산군기부심사위원회 심의회 결과보고', 
'2023년 민간위탁금(노사지원팀) 본예산 편성보고', 
'남구 정신건강복지센터 민간위탁 운영 성과평가 계획', 
'본문', 
'2023년 근로자종합복지관 및 노동상담소 본예산 편성보고', 
'태풍 힌남노 중앙&#8231;도 재난피해 합동조사단 조사결과 보고', 
'「단재 신채호선생 생가지 보수공사」추진계획', 
'「울주군 고향사랑 기부금 모금 및 운용에 관한 조례」 제정 계획', 
'2022년 하반기 기초복무 특별점검 감찰 계획', 
'복지위기가구 발굴&#61598;지원 강화를 위한 희망울타리 네트워크 업무협약 협조 요청', 
'어린이집 보육교사들과 함께하는 힐링콘서트 개최 계획', 
'성립전 예산 사용계획(코로나19 입원 및 격리(재택) 치료비 지원)', 
'2022년 제3회 의왕시 민간위탁 운영위원회 결과보고', 
'2023년 재난관리자원 비축·관리계획 보고', 
'2022년 아동학대예방 및 자원봉사자 유공 포상계획', 
'시간선택제 임기제공무원 신규임용 계획', 
'국제크루즈관광 활성화 지원 사업계획 변경 검토보고', 
'삼호대교 정밀안전진단용역(2차) 시행', 
'대구광역시 서구 공유재산관리 조례 일부개정 계획', 
'2022년도 제4회 공단 직원 채용계획 검토 보고', 
'공무국외여행(국외출장) 심사위원회 개최결과', 
'속초시 시세 징수 조례 시행규칙 등 일부개정 계획', 
'평택시 각종 위원회 설치 및 운영 조례 일부개정조례안', 
'아동보호전담요원(시간선택제임기제공무원) 추가 채용 계획', 
'2023년 건설과 토목1팀 소관 본예산 편성계획(안)', 
'2022년 제9차 의료급여 심의위원회 심의계획', 
'거제시청 인터넷전화(국가정보통신서비스) 사업자 선정 계획', 
'2023년 본예산 편성 계획보고', 
'-군포시 비정규직 노동자 지원센터-  리모델링 공사 검토보고', 
'「지방자치단체 회계관리에 관한 훈령」개정에 따른 합천군 자치법규 일괄개정계획(안)', 
'제309회 임시회 상임위(해양도시안전위) 회의결과 보고', 
'고위험군 인지저하자 치매진단검사 홍보용 인지강화꾸러미 구입계획', 
'2022년 9월중 민원 처리현황 점검결과 보고', 
'2023년 공공기관 통합업무서비스 유지관리 추진계획', 
'재난문자방송 송출판단회의 보고(2022.9.28.) - 코로나19 확진자 일일 발생현황(326명)', 
'「부산광역시 사상구 음식판매자동차 영업장소 등에 관한 조례」일부개정 계획', 
'공적심사의결서(기초생활보장 유공)', 
'원안가결 조례 공포안에 대한 검토 보고', 
'출장결과(9.24.)_변동주 총괄본부장, 제수만 실장, 민혜진 차장', 
'인천광역시 미추홀구 보훈수당 관련 조례 일부개정 계획(안)', 
'결재문서본문 - 2022-10-01T074405.367', 
'2022년 재난대응 안전한국훈련 기본 계획', 
'2022년 동부권역 소규모 하천정비사업(3회추경) 실시설계용역 시행', 
'구정혁신(적극행정) 워크숍 개최 계획', 
'2022년 집중 안전점검 결과보고회 개최 계획', 
'「사회복지법인 김제제일복지재단」 정관변경 인가 검토 보고', 
'결재문서본문 - 2022-09-30T124520.630', 
'2022 신발특화 메이커스페이스 구축·운영 보조금 교부 계획', 
'2022년도 공공조형물 관리실태 점검계획', 
'대구광역시 북구 주민투표에 관한 조례 전부개정 계획', 
'자치법규 규제입증책임제 추진 계획', 
'개인정보 목적 외 이용 및 제3자 제공 절차 개선 계획', 
'2023년-2027년 중기지방재정계획 수립 계획', 
'제26회 노인의날 기념행사 표창계획-노인복지기여 민간인', 
'2023년「재난안전예산 사전검토」운영 계획', 
'2022년 제7회 인천광역시부평구 조례·규칙심의회 개최 계획', 
'「인천광역시 연수구 물품관리조례」 수정가결 조례 공포안에 대한 검토 보고', 
'익산시 청사건립기금 심의위원회 위원 해촉', 
'2022년 영동군 주민자치센터 동아리대회 참가경비 지원계획', 
'금정구 아동 급식지원 조례 일부개정 계획', 
'제18회 임업인 한마음대회 참가 계획 보고', 
'2022년 동 행정복지센터 자체감사 결과보고', 
'2022년 제7차 용역과제심의위원회(서면) 개최 결과 보고', 
'외부강의 신고', 
'당진형 마더센터 조성 추진계획', 
'부산광역시 주택시장 모니터링단 정기보고회 개최', 
'2023년 행정ㆍ복지달력 제작 계획', 
'수영구 청소년 전용공간 운영 2023년 예산 편성 계획', 
'당진 역사_인문투어 기업체 유치 계획', 
'2022년 저수지 퇴적토 준설사업 실시설계용역 시행', 
'결재문서본문 - 2022-09-30T111533.013', 
'강진군 회계관계공무원(분임재무관) 직무대리', 
'고령친화도시 조성위원회  위촉식 및 정기회의 개최 계획', 
'임상병리실 운영을 위한 예산증액 검토보고', 
'2022-2023절기 인플루엔자(독감) 예방접종 계획(안)', 
'「세종특별자치시 적극행정 운영 조례」일부개정 계획(안)', 
'전통시장 활성화 종합 추진계획(안)', 
'당부말씀(금산통합돌봄 복지마을 조성사업 중간보고회)', 
'고남면 고남리 자동차관련시설(주차장) 부지조성 관련 군계획위원회 심의상정 검토보고', 
'재활용 및 대형폐기물 수집·운반·처리 민간대행업제 선정 계획', 
'2022년 위기가구 등 복지사각지대 발굴·지원 계획', 
'정무특별보좌관(전문임기제 나급) 채용 계획', 
'「군포시 사회복지사 등의 처우 및 지위 향상에 관한 조례」일부개정 계획', 
'홍성군 지역사회 청소년통합지원체계 운영위원회 위원 정비 계획', 
'전라북도 도세 감면 조례 일부개정 계획', 
'제4차 보성군 지역교통안전 기본계획 수립용역 보고회 개최 결과 보고', 
'대한민국 안전대전환을 위한 집중안전점검 중간보고회 결과 보고', 
'대전광역시 동구 공유수면 점용료·사용료 징수 조례안(확정)', 
'2023년도 증평군청소년수련관 운영을 위한 당초 예산확보 계획', 
'결재문서본문 - 2022-09-30T104024.074', 
'『고창군 가축사육제한 조례』일부개정 추진계획', 
'2022년 추석연휴 재택치료관리 운영 계획', 
'2022년 환경보전 유공자 도지사 표창 계획', 
'공적심사의결서(22년 취약노인 보호 유공자)', 
'「충주시 공무원 당직 및 비상근무 규칙」 일부개정(안) 방침 결정', 
'제26회 부산바다축제 유공자 포상 계획', 
'결재문서본문 - 2022-10-18T194945.096', 
'『엄궁1배수장 외 3개소 자동운영 관리시스템 구축』사업 추진 계획 보고', 
'2022년 사회복지종사자 복지포인트 지원사업 보조금 교부', 
'코로나19 사망자 위로금 및 전염병차단비 국고보조금 송금(4차)', 
'2023년 항측(무허가건축물), 광고물관리 공무직 채용계획', 
'결재문서본문 - 2022-10-14T124301.783', 
'전작 특화작물 시험포장 전력간선 증설공사 추진']
    # pdf_names = ['test_font_sizes', ]
    # pdf_names = [
    #     # '2022년(1._7.) 남구 옴부즈만 운영상황 보고', 
    #     '2021년 저소득층 추가 국민지원금 국고보조금 집행잔액 반납', 
    # ]
    # inspecting
    pdf_names = ['본문']
    pdf_names = list(set(pdf_names))
    print('pdf length', len(pdf_names))
    pdf_names.sort()
    det_label_list = []
    rec_label_list = []
    step = pool_count * 2

    pdf2jpg_option = {
        "fmt": "jpg",
        # "single_file": True,
        "paths_only": True,
        "use_pdftocairo": True,
        "timeout": 1200, 
        "thread_count": 4,
        # "last_page" : 1,
    }
    conv_and_crop_opt={
        'pdf2image_bool':True, 
        'crop_line_bool':False,
        # 1654 x 2339 200dpi
        'img_rate': 2339 / 841
    }
    # katakana middle dot 0xff65
    # middle dot 0x00b7
    with open('sayi_dict.txt', 'r', encoding='utf-8') as sayi_dict:
        sayi_vocab = set([line[0] for line in sayi_dict.readlines()])
    
    for pdf_idx in range(0, len(pdf_names), step):
        det_label, rec_label = batch_convert_pdf2crop(pool_count, pdf_names[pdf_idx:pdf_idx + step], pdf2jpg_option, conv_and_crop_opt=conv_and_crop_opt, directories=directories)
        rec_label_list.append(rec_label)
        det_label_list.append(det_label)
    write_label(directories['label_dir'], rec_label_list, 'rec_banila_train')
    write_label(directories['label_dir'], det_label_list, 'det_train')
    with tarfile.open('pdf_cropped.tar.gz', 'w:gz') as test_tar:
        test_tar.add(directories['cropped_dir'])
    print("excluded_chr_set:", sorted(excluded_chr_set))