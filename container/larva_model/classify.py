import numpy as np
from keras.models import load_model
import math

class classify:
    def __init__(self):
        self.main_class = ['밥상','서랍장','소파','안마의자','의자','장롱','책상','침대','화장대',
         '가스레인지','냉장고','전기밥솥','선풍기','세탁기','에어프라이어','전자레인지','텔레비전']
        self.chair_subclass = ['일반 의자', '컴퓨터 의자']
        self.bed_subclass= ['돌침대', '2층 침대', '일반 침대']
    
    def main_classify(self, img, model):  
        predict = model.predict(img)
        argsort = np.argsort(predict[0])
        category1 = [self.main_class[argsort[-1]], math.trunc(predict[0][argsort[-1]] * 100)]
        category2 = [self.main_class[argsort[-2]], math.trunc(predict[0][argsort[-2]] * 100)]
        category3 = [self.main_class[argsort[-3]], math.trunc(predict[0][argsort[-3]] * 100)]
        category4 = [self.main_class[argsort[-4]], math.trunc(predict[0][argsort[-4]] * 100)]
        return category1, category2, category3, category4

    def sub_classify(self, img, label, model):
        predict = np.argmax(model.predict(img), axis=-1)
        category = label[int(predict)]
        return category
        
    def get_model(self, model_path):
        model = load_model(model_path)
        return model