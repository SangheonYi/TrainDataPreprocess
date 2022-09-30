from pdf2image import convert_from_path
# (595, 842)
# file_name = "Bulldog.pdf"
def pdf2jpg(file_name, save_size):
	pages = convert_from_path("pdf/" + file_name, size=save_size)
	# pages = convert_from_path("pdf/" + file_name)
	for i, page in enumerate(pages):
		page.save(f"output/{file_name[:-4] + str(i)}.jpg", "JPEG")