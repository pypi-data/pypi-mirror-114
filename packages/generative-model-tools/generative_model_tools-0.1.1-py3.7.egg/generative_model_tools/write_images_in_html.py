# coding:utf-8
import os
import os.path as osp
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image


class ImageLogger():
    def __init__(self, exp_name='exp', ckpt_dir='./ckpt', image_names=['input', 'output'], image_size=256, auto_fresh_seconds=30, weight2value={'权重1': '大小'}):
        self.exp_name = exp_name
        self.ckpt_dir = ckpt_dir
        self.image_names = image_names
        self.image_size = image_size
        self.auto_fresh_seconds = auto_fresh_seconds
        if not osp.exists(ckpt_dir):
            os.makedirs(ckpt_dir)
        self.weight_html = self.gather_weight_for_html(weight2value)
        self.img_lst = list()

    def update_images(self, tensor_dict, iter_idx):
        cur_images = list()
        images_dir = osp.join(self.ckpt_dir, 'images')
        if not osp.exists(images_dir):
            os.makedirs(images_dir)
        for image_name in self.image_names:
            image = tensor_dict[image_name]
            if len(image.shape) == 4:
                image = image[0, :, :, :]
            image = np.array(255*image.detach().cpu().permute(1,2,0).numpy()/2+0.5, dtype=np.uint8)
            image_path = osp.join(images_dir, str(iter_idx).zfill(7))+'.jpg'
            Image.fromarray(image).save(image_path)
            cur_images.append(osp.join('./images', str(iter_idx).zfill(7))+'.jpg')
        cur_images = [iter_idx] + [cur_images]
        self.img_lst = [cur_images] + self.img_lst
        self.write_html()

    
    def write_html(self):
        filename = os.path.join(self.ckpt_dir, "index.html")
        html_head = (
            """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Experiment name = %s</title>
          <meta http-equiv="refresh" content="%d">
        </head>
        <body>
        """
            % (self.exp_name, self.auto_fresh_seconds)
        )
        html_tail = """
        </body>
        </html>
        """
        html_weight_html = self.weight_html
        html_cell = list()
        for img_idx, image_paths in self.img_lst:
            html_cell.append("<h3>iteration [%d] </h3>\n" % (img_idx))
            html_cell.append(
                """
            <table border="1" style="table-layout: fixed;" class="cell">
            <tr>
            """
            )
            print(image_paths)
            for image_name_idx, image_path in enumerate(image_paths):
                html_cell.append(
                    """
                    <td halign="center" style="word-wrap: break-word;" valign="top">
                    <p>
                        <a href="%s">
                            <img src="%s" style="width:%s px">
                        </a><br>
                        <p align='center'>%s</p>
                        </p>
                    </td>
                            """
                    % (image_path, image_path, str(self.image_size), self.image_names[image_name_idx])
                )
            html_cell.append(
                """
                        </tr>
                        </table>
                        """
            )
        html_cell = "\n".join(html_cell)
        html = html_head + html_weight_html + html_cell + html_tail
        soup = BeautifulSoup(html, features="html.parser")
        with open(filename, "w", encoding="utf-8") as flow:
            flow.write(soup.prettify())

    def gather_weight_for_html(self, weight2value):
        html = """
        <style>
            #zxd_x {
                width: 20px;
                height: 20px;
                text-align: center;
                font-size: 16px;
                color: red;
                position: absolute;
                right: 0px;
                top: 0px;
                cursor: pointer;
            }
        </style>
        <div style="z-index:999;display: block; position: fixed; right: 0px; top: 200px;">
            <div id="zxd_x">
                <a title="点击关闭"><b></b></a></div>
            <div class="content">
                <table border="1" class="weight_for_lambda">
                    <tr>
                        <th>名称</th>
                        <th>大小</th>
                    </tr>
        """
        for key, val in weight2value.items():
            html = (
                html
                + """
            <tr>
                        <td>"""
                + str(key)
                + """</td>
                        <td>"""
                + str(val)
                + """</td>
                    </tr>
            """
            )
        html += """
        </table>
            </div>
        </div>
        """
        return html
