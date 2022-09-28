from fontTools.ttLib import TTFont
import os

font_path_list = ['휴먼명조.ttf', 'Dotum-03.ttf', 'hy헤드라인m.ttf']
font = TTFont(font_path_list[1])   # specify the path to the font in question
print(dir(font))
print(len(font.getBestCmap().keys()))
print(font.keys())
print(font.tables)
print(dir(font['maxp']))