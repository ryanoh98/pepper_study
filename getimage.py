import qi
import argparse
import sys
import time
import vision_definitions
import json
import base64
import requests
from PIL import Image


def main(session):
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")

    # Register a Generic Video Module
    resolution = vision_definitions.kQQVGA
    colorSpace = vision_definitions.kYUVColorSpace 
    fps = 20
    resolution = 5
    colorSpace = 11

    nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

    print 'getting images in remote'
    for i in range(0, 1):
        print "getting image " + str(i)
        naoImage = video_service.getImageRemote(nameId)
        width = naoImage[0]
        height = naoImage[1]
        array = naoImage[6]
        print(width, height)
        image_string = str(bytearray(array))
        im = Image.frombytes("RGB", (width, height), image_string)
        im.save("naoImage"+str(i)+'.png',"PNG")
        time.sleep(0.05)

        
    video_service.unsubscribe(nameId)

    return image_string

def pose_detect(file):
    APP_KEY = '3ac17bc0e257b604d053901085eaae99'
    session = requests.Session()
    session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

    response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', file)])
    result = response.json()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.45",
            help="Robot IP address. On robot or Local Naoqi: use '192.168.1.45'.")
    parser.add_argument("--port", type=int, default=9559,
            help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n""Please check your script arguments. Run with -h option for help.")
        sys.exit(1) 

    data = main(session)
    result_pose = pose_detect(data)
    print(result_pose)





