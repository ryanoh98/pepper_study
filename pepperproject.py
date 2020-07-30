import qi
import argparse
import sys
import time
import almath
import vision_definitions
import json
import base64
import requests
from PIL import Image

# pepper capturing photo
def capture(session, count):
    # Get the service ALVideoDevice.
    print('here is capture function')

    video_service = session.service("ALVideoDevice")

    # Register a Generic Video Module
    resolution = vision_definitions.kQQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 20
    resolution = 5
    colorSpace = 11

    nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

    print('getting images in remote')
    # for i in range(0, 1):
    print("getting image " + str(count))
    naoImage = video_service.getImageRemote(nameId)
    width = naoImage[0]
    height = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))
    print('width, height',width, height)
    im = Image.frombytes("RGB", (width, height), image_string)
    resize_image = im.resize((640,480))
    image_name = "naoImage" + str(count) + '.png'
    resize_image.save("naoImage" + str(count) + '.png', "PNG")
    time.sleep(0.05)

    video_service.unsubscribe(nameId)

    return image_name

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

def lookfrontandposture(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses(["Head", "Shoulder"], [1.0, 1.0])
    names            = ["HeadYaw", "HeadPitch", "LShoulderPitch", "RShoulderPitch"]
    angles           = [0.0*almath.TO_RAD, -25.0*almath.TO_RAD, -86.0*almath.TO_RAD, -86.0*almath.TO_RAD]
    fractionMaxSpeed = 0.1
    motion_service.setAngles(names,angles,fractionMaxSpeed)


def posture(session):
    # Get the service ALMotion.
    motion_service = session.service("ALMotion")
    motion_service.setStiffnesses("Shoulder", 1.0)

    # Example showing a single target angle for one joint
    # Interpolates the head yaw to 1.0 radian in 1.0 second
    names      = ["LShoulderPitch", "RShoulderPitch"]
    angles = [-86.0*almath.TO_RAD, -86.0*almath.TO_RAD]
    fractionMaxSpeed = 0.1
    motion_service.setAngles(names,angles,fractionMaxSpeed)

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
    f = open('./sample.png', 'rb')
    result_pose_sample = pose_detect(f)
    count = 0
    while True:
        count +=1
        # analyze the captured photo
        lookfrontandposture(session)
        image_name = capture(session,count)
        f_capture = open(image_name, 'rb')
        result_pose_capture = pose_detect(f_capture)

        # Compare two photos
        score = 0
        try:
            point1 = result_pose_sample[0]['keypoints']
            point2 = result_pose_capture[0]['keypoints']

            for i,j in zip(point1, point2):
                score += abs(i-j)
        except Exception as e:
            print(result_pose_capture)
            print(e)
            pass
        print('score', score)
        if score > 500:
            bad(session)
        else:
            good(session)
            break
    # Conclusion
    concl(session)


