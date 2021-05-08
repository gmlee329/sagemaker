from tensorflow.python.keras.models import load_model
from PIL import Image
import numpy as np
import io

class classify:
    def __init__(self):
        self.category = ['밥상', '서랍장', '소파', '안마의자', '의자', '장롱', '책상', '침대', '화장대']

    def classfy(self, model, img):

        # image_byte = img.read()
        # img = Image.open(io.BytesIO(image_byte))
        # img = img.resize(size=(80,80))
        img = np.array(img)
        predict = model.predict(img)
        index = np.argmax(predict)
        
        return self.category[index]
    
    def get_model(self, model_path):
        model = load_model(model_path)
        return model

if __name__ == '__main__':
    model_path = './model/first_model.h5'
    img = Image.open('./model/의자.jpg')
    CF = classify()
    pretrained_model = CF.get_model(model_path)
    category = CF.classfy(pretrained_model, img)
    result = {
        "category" : category
    }
    print(result)