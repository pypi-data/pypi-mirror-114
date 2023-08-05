# coding:utf-8
import os
import os.path as osp
# import torch


class ImageLogger():
    def __init__(self, ckpt_dir='.', image_names=['input', 'output'], image_size=256):
        self.ckpt_dir = ckpt_dir
        self.image_names = image_names
        self.image_size = image_size

    def update_images(self, tensor_dict):
        print(tensor_dict)
