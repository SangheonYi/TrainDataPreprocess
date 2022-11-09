cat administrative_documents/done/admi_train.txt > admi_font_banila_train.txt
cat font_data/rec_font_train.txt >> admi_font_banila_train.txt
cat PDFPreprocess/labels/rec_banila_train.txt >> admi_font_banila_train.txt
scp admi_font_banila_train.txt administrative_documents/done/admi_val.txt spey3125@192.168.20.159:/data/spey3125/sayi/ONR/train_data
# scp -r -P 16022 admi_font_banila_train.txt administrative_documents/done/admi_val.txt ubuntu@211.253.164.229:/home/ubuntu/sayi/ONR/train_data/
