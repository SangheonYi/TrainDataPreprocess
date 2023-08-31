from typing import Type
from util import to_train_path
import json

class OCRLabels:
    def __init__(self):
        self.rec_label_list = []
        self.det_label_list = []
        self.det_section_label_list = []

    def to_det_label(self, image_path, gts):
        return f"{to_train_path(image_path)}\t{json.dumps(gts, ensure_ascii=False)}\n"
    
    def append_det_label(self, image_path, det_gt, det_section_gt):
        det_label = self.to_det_label(image_path, det_gt)
        det_section_label = self.to_det_label(image_path, det_section_gt)
        self.det_label_list.append(det_label)
        self.det_section_label_list.append(det_section_label)

    def merge_ocr_labels(self, sub_labels:Type['OCRLabels']):
        self.rec_label_list += sub_labels.rec_label_list
        self.det_label_list += sub_labels.det_label_list
        self.det_section_label_list += sub_labels.det_section_label_list