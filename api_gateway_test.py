import requests
import json
from PIL import Image
import io
import numpy as np
import time
import os
import im_utils

def img_to_npy(img):
    img = im_utils.check_angle(img)
    img = im_utils.make_square(img)
    img = img.convert('RGB')
    img = im_utils.resize_img(img, shape=(100,100))
    img = np.array(img).reshape(1,100,100,3) / 255.
    return img

def test_api_gateway(path):
    img = Image.open(path)
    img = img_to_npy(img)

    img = img.tolist()
    test_data = {
        'img' : img
    }
    payload = json.dumps(test_data)

    s = time.time()

    url = 'https://4rqor8vh30.execute-api.us-west-2.amazonaws.com/default/resnet-lambda'
    response = requests.post(url, data=payload)
    result = response.json()
    result = result['body']
    print(result, '>', time.time()-s)

root_path = os.getcwd()
dir_path = os.path.join(root_path, 'sample_img')
for file_name in os.listdir(dir_path):
    path = os.path.join(dir_path, file_name)
    test_api_gateway(path)
    break
    # time.sleep(1)