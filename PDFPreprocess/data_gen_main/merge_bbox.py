from PDFForTrainData import PDFForTrainData
from functools import partial

def margin_and_merge_bbox(low_level_bbox_list, margin_rate, pdf: PDFForTrainData,
                           is_horizon=True, margin_box_color='red', merged_box_color='green', draw_margin_box=False, draw_high_level_box=False):
    add_merge_margin_partial = partial(add_merge_margin, margin_rate=margin_rate, is_horizon=is_horizon)
    margined_bbox_list = list(map(add_merge_margin_partial, low_level_bbox_list))
    high_level_bbox_list = merge_overlapping_rectangles(margined_bbox_list)
    if draw_margin_box:
        pdf.draw_bboxes("margined box", margined_bbox_list, box_color=margin_box_color, line_width=8)
    if draw_high_level_box:
        pdf.draw_bboxes("high_level_coord", high_level_bbox_list, box_color=merged_box_color, line_width=6)
    return high_level_bbox_list

def merge_section_bbox(pdf: PDFForTrainData, word_bbox_list):
    # draw word box
    # pdf.draw_bboxes("word box", word_bbox_list, draw_coord=True, bbox_only=True)
    # merge horizontal
    line_bbox_list = margin_and_merge_bbox(word_bbox_list, 0.23, pdf)
    # merge vertical
    section_bbox_list = margin_and_merge_bbox(line_bbox_list, 0.3, pdf, 
                                              is_horizon=False, margin_box_color='blue', merged_box_color='yellow', draw_high_level_box=False)
    det_section_labels = []
    for i, merged_coord in enumerate(section_bbox_list):
        left, upper, right, lower = merged_coord
        section_gt = [[int(left), int(upper)], [int(right), int(upper)], [int(right), int(lower)], [int(left), int(lower)]]
        det_section_labels.append({"transcription": f"section {i}", "points": section_gt})
    return det_section_labels

def add_merge_margin(rectangle, margin_rate, is_horizon=True):
    left, upper, right, lower = rectangle
    margin = (lower - upper) * margin_rate
    horizon_margin = margin if is_horizon else 0
    vertical_margin = 0 if is_horizon else margin
    return [left - horizon_margin, upper - vertical_margin, right + horizon_margin, lower + vertical_margin]
    
def merge_overlapping_rectangles(rectangles):
    src_rects = rectangles
    while True:
        merged_rectangles = []
        need_merge = False
        for rect in src_rects:
            x1, y1, x2, y2 = rect
            merged = False
            for i, merged_rect in enumerate(merged_rectangles):
                mx1, my1, mx2, my2 = merged_rect
                if not (mx2 < x1 or x2 < mx1 or my2 < y1 or y2 < my1):
                    # Rectangles overlap, merge them
                    merged_rectangles[i] = [min(x1, mx1), min(y1, my1), max(x2, mx2), max(y2, my2)]
                    merged = True
                    need_merge = True
                    break
            if not merged:
                merged_rectangles.append(rect)
        if not need_merge:
            break
        src_rects = merged_rectangles
    return merged_rectangles

if __name__ == '__main__':
    from PIL import Image, ImageDraw

    image_path = '/mnt/d/WSL/workspace/ocr/OOCR/exprsc/2_1_.png'
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size=(1200, 1200))
    draw_img = img.copy()
    draw = ImageDraw.Draw(draw_img)
    coordinates = [(0, 10, 10, 20), (8, 13, 18, 23), (10, 23, 18, 30), (10, 50, 18, 60)]
    coordinates = [[280, 282, 534, 218], [512, 282, 835, 218], [813, 282, 1063, 218]]
    coordinates =[[297, 219, 517, 275], [529, 219, 818, 275],  [297, 275, 605, 330], [611, 275, 764, 330]]

    merged_rectangles = merge_overlapping_rectangles(coordinates)
    for merged_coord in merged_rectangles:
        left, upper, right, lower = merged_coord
        print("merged result: ", left, upper, right, lower)
        draw.rectangle(merged_coord, outline="blue",  width=5)
    draw_img.save('merged_box_test.jpg', "JPEG")