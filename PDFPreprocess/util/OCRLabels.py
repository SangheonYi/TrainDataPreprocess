from typing import Type

class OCRLabels:
    def __init__(self):
        self.rec_label_list = []
        self.det_label_list = []
        self.det_section_label_list = []

    def append_det_label(self, det_label, det_section_label):
        self.det_label_list.append(det_label)
        self.det_section_label_list.append(det_section_label)

    def merge_ocr_labels(self, sub_labels:Type['OCRLabels']):
        self.rec_label_list += sub_labels.rec_label_list
        self.det_label_list += sub_labels.det_label_list
        self.det_section_label_list += sub_labels.det_section_label_list