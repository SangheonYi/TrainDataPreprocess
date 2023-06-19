import os
from util.util import create_directories, create_directory, get_file_list

# pdf_names = [corpus_pdf_path ]
max_number = 0
# for pdf_name in pdf_names:
# pdf_name  = pdf_names[0]
for corpus_pdf_path in get_file_list('corpus_pdf'):
    print(corpus_pdf_path)
    if not corpus_pdf_path.startswith('wind'):
        corpus_number = corpus_pdf_path.split('.')[0].split('_')[-1]
        max_number = max(max_number, corpus_number)
    break
print(max_number)
