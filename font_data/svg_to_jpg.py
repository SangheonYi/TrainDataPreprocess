from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

def list_all_files(rootdir, file_list, extend):
    extend_upper = extend.upper()
    for file in os.listdir(rootdir):
        joined_path = os.path.join(rootdir, file)
        if file.endswith(extend) or file.endswith(extend_upper):
            file_list.append({
                "path": joined_path,
                "name": file.split(".")[0]
            })
    
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

ff_path = "/mnt/c/Program Files (x86)/FontForgeBuilds"
result_path = '/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/GNGT'
origin_path = '/mnt/c/Program Files (x86)/FontForgeBuilds'
file_list = []
list_all_files(ff_path, file_list, 'svg')
createDirectory(result_path)
print(len(file_list))

# svglib 사용 시 변형된 결과 확인
drawing = svg2rlg(f"{origin_path}/zero_UntitledTTF.svg")
renderPM.drawToFile(drawing, f"{result_path}/zero_UntitledTTF.png", fmt="PNG")

import aspose.words as aw
# create a document
doc = aw.Document()

# create a document builder and initialize it with document object
builder = aw.DocumentBuilder(doc)

# insert SVG image to document
shape = builder.insert_image(f"{origin_path}/zero_UntitledTTF.svg")

# # OPTIONAL
# # Calculate the maximum width and height and update page settings 
# # to crop the document to fit the size of the pictures.
# pageSetup = builder.page_setup
# pageSetup.page_width = shape.width
# pageSetup.page_height = shape.height
# pageSetup.top_margin = 0
# pageSetup.left_margin = 0
# pageSetup.bottom_margin = 0
# pageSetup.right_margin = 0

# save as PNG
doc.save(f"{result_path}svg-to-png.png")