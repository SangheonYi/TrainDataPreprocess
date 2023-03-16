from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
import time

def logging_time(original_fn):
	def wrapper_fn(*args, **kwargs):
		start_time = time.time()
		original_fn(*args, **kwargs)
		end_time = time.time()
		print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
	return wrapper_fn
    # Parameters:
	# pdf_path -> Path to the PDF that you want to convert 
	# dpi -> Image quality in DPI (default 200) 
	# output_folder -> Write the resulting images to a folder (instead of directly in memory) 
	# first_page -> First page to process 
	# last_page -> Last page to process before stopping 
	# fmt -> Output image format 
	# jpegopt -> jpeg options quality, progressive, and optimize (only for jpeg format) 
	# thread_count -> How many threads we are allowed to spawn for processing 
	# userpw -> PDF's password 
	# use_cropbox -> Use cropbox instead of mediabox 
	# strict -> When a Syntax Error is thrown, it will be raised as an Exception 
	# transparent -> Output with a transparent background instead of a white one. 
	# single_file -> Uses the -singlefile option from pdftoppm/pdftocairo 
	# output_file -> What is the output filename or generator 
	# poppler_path -> Path to look for poppler binaries 
	# grayscale -> Output grayscale image(s) 
	# size -> Size of the resulting image(s), uses the Pillow (width, height) standard 
	# paths_only -> Don't load image(s), return paths instead (requires output_folder) 
	# use_pdftocairo -> Use pdftocairo instead of pdftoppm, may help performance 
	# timeout -> Raise PDFPopplerTimeoutError after the given time
# (595, 842)
# file_name = "Bulldog.pdf"
@logging_time
def pdf2jpg(file_name, **kwargs):
	return convert_from_path(f"pdf/{file_name}.pdf", **kwargs)

if __name__=="__main__":
	target = '2022 재난대응 안전한국훈련 기본계획'
	pdf2jpg_option = {
		"fmt": "jpg",
		# "single_file": True,
		# "paths_only": True,
		"use_pdftocairo": True,
		"size": (None, 1000),
		"timeout": 1200, 
		# "thread_count": 4,
		"output_folder": ".",
		"output_file": target,
        # "last_page" : 1
	}
	convert_from_path(f"{target}.pdf", **pdf2jpg_option)
	# pdf2jpg('target', **pdf2jpg_option)