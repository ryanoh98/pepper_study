import qi
import argparse
import sys
import time
import vision_definitions
import json
import base64
import requests
from PIL import Image

# pepper capturing photo
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

    print
    'getting images in remote'
    for i in range(0, 1):
        print
        "getting image " + str(i)
        naoImage = video_service.getImageRemote(nameId)
        width = naoImage[0]
        height = naoImage[1]
        array = naoImage[6]
        image_string = str(bytearray(array))
        im = Image.frombytes("RGB", (width, height), image_string)
        im.save("naoImage" + str(i) + '.png', "PNG")
        time.sleep(0.05)

    video_service.unsubscribe(nameId)

    return image_string

# pose analyze
def pose_detect(file):
    APP_KEY = '3ac17bc0e257b604d053901085eaae99'
    session = requests.Session()
    session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

    response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', file)])
    result = response.json()
    return result

def intro(session):
    # Speaking
    tts = session.service("ALTextToSpeech")
    tts.say("Hi! I think you need to prevent round shoulder. Follow my stretch.")

def good(session):
    # Speaking
    tts = session.service("ALTextToSpeech")
    tts.say("Great job!")

def bad(session):
    # Speaking
    tts = session.service("ALTextToSpeech")
    tts.say("It's wrong. Do it again in 3 seconds.")
    time.sleep(3)

def concl(session):
    # Speaking
    tts = session.service("ALTextToSpeech")
    tts.say("Well done! Now, you deserve to be a normal one.")

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
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(
            args.port) + ".\n""Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # Introduction
    intro(session)

    # analyze the sample
    f = open('./1.jpg', 'rb')
    result_pose_sample = pose_detect(f)

    while True:
        # analyze the captured photo
        data = main(session)
        result_pose_capture = pose_detect(data)

        # Compare two photos
        point1 = result_pose_sample[0]['keypoints']
        point2 = result_pose_capture[0]['keypoints']
        score = 0
        for i,j in zip(point1, point2):
            score += abs(i-j)
        if score > 500:
            bad(session)
        else:
            good(session)
            break
    # Conclusion
    concl(session)

