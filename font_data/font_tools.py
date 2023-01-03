from fontTools.ttLib import TTFont
import os

font_path_list = ['휴먼명조.ttf', 'Dotum.ttf', 'hy헤드라인m.ttf']
font_path_list = ['견고딕.ttf','Dotum.ttf',]
for font_path in font_path_list:
    font = TTFont(font_path)   # specify the path to the font in question
    # print(dir(font))
    # print(font.getBestCmap())
    print(font_path)
    for cmap in font['cmap'].tables:
        for item in cmap.cmap.items():
            print(item)
print(font.keys())
print(font.tables)
print(dir(font['maxp']))