
import requests

import cv2
import numpy as np
from matplotlib import pyplot as plt
from pycocotools.coco import COCO
from requests import Session

def pose_detect(file):
    APP_KEY = '3ac17bc0e257b604d053901085eaae99'
    session = requests.Session()
    session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

    response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', file)])
    result = response.json()
    return result

def visualize(filename, annotations, threshold=0.2):
    # 낮은 신뢰도를 가진 keypoint들은 무시
    for annotation in annotations:
        keypoints = np.asarray(annotation['keypoints']).reshape(-1, 3)
        low_confidence = keypoints[:, -1] < threshold
        keypoints[low_confidence, :] = [0, 0, 0]
        annotation['keypoints'] = keypoints.reshape(-1).tolist()

    # COCO API를 활용한 시각화
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.axis('off')
    coco = COCO()
    coco.dataset = {
        "categories": [
            {
                "supercategory": "person",
                "id": 1,
                "name": "person",
                "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder",
                              "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip",
                              "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"],
                "skeleton": [[1, 2], [1, 3], [2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 7], [6, 8], [6, 12], [7, 9],
                             [7, 13], [8, 10], [9, 11], [12, 13], [14, 12], [15, 13], [16, 14], [17, 15]]
            }
        ]
    }
    coco.createIndex()
    coco.showAnns(annotations)
    plt.show()

if __name__ == "__main__":
    # im = Image.open('C:/Users/오윤제/Pictures/1.jpg')
    # print('image_size', im.size)
    IMAGE_FILE_PATH ='./sample3.png'
    f = open(IMAGE_FILE_PATH, 'rb')
    result = pose_detect(f)
    visualize(IMAGE_FILE_PATH, result)
