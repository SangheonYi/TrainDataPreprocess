from PIL import Image, ImageFont, ImageDraw, ImageEnhance

def highlight_bbox():
    source_img = Image.open("Bulldog.jpg").convert("RGB")
    draw = ImageDraw.Draw(source_img)
    draw.rectangle(((0, 00), (100, 100)), outline="black")
    draw.text((20, 70), "dkjffjfffffffffffffffffffffffffffffffffff", font=ImageFont.truetype("Batang.ttf", size=50), fill="dodgerblue")
    source_img.save("highlighted.jpg", "JPEG")
highlight_bbox()
