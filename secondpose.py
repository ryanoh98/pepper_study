import json
import base64
import requests
from PIL import Image

def pose_detect(file):
    APP_KEY = '3ac17bc0e257b604d053901085eaae99'
    session = requests.Session()
    session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

    response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', file)])
    result = response.json()
    return result

if __name__ == "__main__":
    im = Image.open('C:/Users/오윤제/Pictures/aaa.jpg')
    print('image_size', im.size)

    f = open('C:/Users/오윤제/Pictures/.jpg', 'rb')
    print(f)
    result_pose = pose_detect(f)
    print(result_pose)