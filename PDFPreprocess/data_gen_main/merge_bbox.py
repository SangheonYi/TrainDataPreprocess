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