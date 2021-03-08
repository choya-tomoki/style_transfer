from django.db import models
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import io, base64
from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import requests

import sys
sys.path.append('../')
from inference.Inferencer import Inferencer
from models.PasticheModel import PasticheModel


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    style = models.CharField(max_length=50)
    scraping_word = models.CharField(max_length=100)
    IMAGE_SIZE = 1024 # 画像サイズ
    MODEL_FILE_PATH = './carbike/ml_models/pastichemodel_99-FINAL.pth' # モデルファイル
    NUM_STYLES = 24

    def inference(self, style):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        pastichemodel = PasticheModel(self.NUM_STYLES)

        inference = Inferencer(pastichemodel,device,self.IMAGE_SIZE)
        inference.load_model_weights(self.MODEL_FILE_PATH)

        img_data = self.image.read()
        img_bin = io.BytesIO(img_data)
        im = Image.open(img_bin).convert('RGB')
        
        style_choice = style
        style_choice_2 = None
        style_factor = None
        
        if style_choice_2 == None or style_factor == None:
            result_img = inference.eval_image(im, style_choice)
        
        if style_choice_2 != None and style_factor != None:
            result_img = inference.eval_image(im, style_choice, style_choice_2, style_factor)
            
        buffer = io.BytesIO()
        result_img.save(buffer, format="PNG") 
        base64_img = base64.b64encode(buffer.getvalue()).decode()#.replace("'", "")
        return 'data:result_image/png;base64,' + base64_img


    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img
    
    def style_image_src(self, num):
        style_option = [5,3,20,22,7,1,14,11,17,10,21,18,4,12,6,16,8,23,15,2,9,13,24,19]
        img = Image.open("./carbike/static/carbike/image/{0:02d}.jpg".format(style_option[num-1]))
        print(".static/carbike/image/{0:02d}.jpg".format(num))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG") 
        base64_img = base64.b64encode(buffer.getvalue()).decode()#.replace("'", "")
        return 'data:result_image/png;base64,' + base64_img

    def scraping(self):
        keyword = self.scraping_word
        url = 'https://search.yahoo.co.jp/image/search?p={}'.format(keyword)
        headers = {'User-Agent':'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        print(soup.title.string)
        print(soup)
        top_img = soup.find(id="contentsInner").find("img").get("src")

        # req = urllib.request.Request(url=url)
        # res = urllib.request.urlopen(req)
        # soup = BeautifulSoup(res)
        # top_img = soup.find("div", id="gridlist").find("img").get("src")
        tmp = urllib.request.urlopen(top_img)
        data = tmp.read()
        base64_img = base64.b64encode(data).decode()#
        return 'data:result_image/png;base64,' + base64_img

