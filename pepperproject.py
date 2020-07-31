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
import numpy as np
import math

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
    tts = session.service("ALTextToSpeech")
    tts.say("Hi! Let's prevent round shoulder. Follow my stretch.")


def good(session):
    tts = session.service("ALTextToSpeech")
    tts.say("Great job!")

def bad(session):
    tts = session.service("ALTextToSpeech")
    tts.say("It's wrong. Do it again in 3 seconds.")
    time.sleep(5)

def tryagain(session):
    tts = session.service("ALTextToSpeech")
    tts.say("I cannot find you.")
    time.sleep(5)

def next(session):
    tts = session.service("ALTextToSpeech")
    tts.say("Let's begin the next stretch.")
    time.sleep(4)

def concl(session):
    tts = session.service("ALTextToSpeech")
    tts.say("Well done! Now, you deserve to be a normal one.")

def posture1(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses(["Head", "Shoulder"], [1.0, 1.0])
    names            = ["HeadYaw", "HeadPitch", "LShoulderPitch", "RShoulderPitch"]
    angles           = [0.0*almath.TO_RAD, -35.0*almath.TO_RAD, -86.0*almath.TO_RAD, -86.0*almath.TO_RAD]
    fractionMaxSpeed = 0.4
    motion_service.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(5)

def posture2(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses(["Head", "Shoulder", "Elbow"], [1.0, 1.0, 1.0])
    names            = ["HeadYaw", "HeadPitch", "LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll", "LElbowYaw", "RElbowYaw"]
    angles           = [0.0*almath.TO_RAD, -20.0*almath.TO_RAD, 45.0*almath.TO_RAD, -45.0*almath.TO_RAD,
                        -89.0*almath.TO_RAD, 89.0*almath.TO_RAD, 5.0*almath.TO_RAD, -5.0*almath.TO_RAD]
    fractionMaxSpeed = 0.4
    motion_service.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(5)


def cal_angle(x,y,z):
    return (180/math.pi)*abs(math.atan((x[1]-y[1])/(x[0])-(y[0]))
                                   -math.atan((z[1]-y[1])/(z[0]-y[0])))
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

    # analyze the first sample
    f1 = open('./sample.png', 'rb')
    result_pose_sample1 = pose_detect(f1)
    count1 = 0
    while True:
        count1 +=1
        # analyze the captured photo
        posture1(session)
        image_name1 = capture(session,count1)
        f_capture1 = open(image_name1, 'rb')
        result_pose_capture1 = pose_detect(f_capture1)

        try:
            # Compare two photos with angle
            point1 = result_pose_sample1[0]['keypoints']
            point2 = result_pose_capture1[0]['keypoints']

            point1_RShoulder = np.array([point1[18],point1[19]])
            point1_REar = np.array([point1[12],point1[13]])
            point1_RElbow = np.array([point1[24],point1[25]])
            point1_RWrist = np.array([point1[30],point1[31]])
            point1_LShoulder = np.array([point1[15],point1[16]])
            point1_LEar = np.array([point1[9],point1[10]])
            point1_LElbow = np.array([point1[21],point1[22]])
            point1_LWrist = np.array([point1[27],point1[28]])
            point2_RShoulder = np.array([point2[18],point2[19]])
            point2_REar = np.array([point2[12],point2[13]])
            point2_RElbow = np.array([point2[24],point2[25]])
            point2_RWrist = np.array([point2[30],point2[31]])
            point2_LShoulder = np.array([point2[15],point2[16]])
            point2_LEar = np.array([point2[9],point2[10]])
            point2_LElbow = np.array([point2[21],point2[22]])
            point2_LWrist = np.array([point2[27],point2[28]])

            right_fromEar_angle1 = cal_angle(point1_REar, point1_RShoulder, point1_RElbow)
            left_fromEar_angle1 = cal_angle(point1_LEar, point1_LShoulder, point1_LElbow)
            right_fromEar_angle2 = cal_angle(point2_REar, point2_RShoulder, point2_RElbow)
            left_fromEar_angle2 = cal_angle(point2_LEar, point2_LShoulder, point2_LElbow)
            right_fromShoulder_angle1 = cal_angle(point1_RShoulder, point1_RElbow, point1_RWrist)
            left_fromShoulder_angle1 = cal_angle(point1_LShoulder, point1_LElbow, point1_LWrist)
            right_fromShoulder_angle2 = cal_angle(point2_RShoulder, point2_RElbow, point2_RWrist)
            left_fromShoulder_angle2 = cal_angle(point2_LShoulder, point2_LElbow, point2_LWrist)

            CompareFromREar = abs(right_fromEar_angle1-right_fromEar_angle2)
            CompareFromLEar = abs(left_fromEar_angle1-left_fromEar_angle2)
            CompareFromRShoulder = abs(left_fromEar_angle1-left_fromEar_angle2)
            CompareFromLShoulder = abs(left_fromShoulder_angle1-left_fromShoulder_angle2)

            print(CompareFromREar)
            print(CompareFromLEar)
            print(CompareFromRShoulder)
            print(CompareFromLShoulder)


            if ((CompareFromREar <= 30) and (CompareFromLEar <= 30) and (CompareFromRShoulder <= 30)
                    and (CompareFromLShoulder <= 30)):
                good(session)
                break
            else:
                bad(session)
        except IndexError as e:
            print(e)
            tryagain(session)

    # move on to the second posture
    next(session)
    f2 = open('./posture222.jpg', 'rb')
    result_pose_sample2 = pose_detect(f2)
    count2 = 0
    while True:
        count2 +=1
        # analyze the captured photo
        posture2(session)
        image_name2 = capture(session,count2)
        f_capture2 = open(image_name2, 'rb')
        result_pose_capture2 = pose_detect(f_capture2)

        try:
            # Compare two photos with angle
            point11 = result_pose_sample2[0]['keypoints']
            point22 = result_pose_capture2[0]['keypoints']

            point11_RShoulder = np.array([point11[18],point11[19]])
            point11_REar = np.array([point11[12],point11[13]])
            point11_RElbow = np.array([point11[24],point11[25]])
            point11_RWrist = np.array([point11[30],point11[31]])
            point11_LShoulder = np.array([point11[15],point11[16]])
            point11_LEar = np.array([point11[9],point11[10]])
            point11_LElbow = np.array([point11[21],point11[22]])
            point11_LWrist = np.array([point11[27],point11[28]])
            point22_RShoulder = np.array([point22[18],point22[19]])
            point22_REar = np.array([point22[12],point22[13]])
            point22_RElbow = np.array([point22[24],point22[25]])
            point22_RWrist = np.array([point22[30],point22[31]])
            point22_LShoulder = np.array([point22[15],point22[16]])
            point22_LEar = np.array([point22[9],point22[10]])
            point22_LElbow = np.array([point22[21],point22[22]])
            point22_LWrist = np.array([point22[27],point22[28]])

            right_fromEar_angle11 = cal_angle(point11_REar, point11_RShoulder, point11_RElbow)
            left_fromEar_angle11 = cal_angle(point11_LEar, point11_LShoulder, point11_LElbow)
            right_fromEar_angle22 = cal_angle(point22_REar, point22_RShoulder, point22_RElbow)
            left_fromEar_angle22 = cal_angle(point22_LEar, point22_LShoulder, point22_LElbow)
            right_fromShoulder_angle11 = cal_angle(point11_RShoulder, point11_RElbow, point11_RWrist)
            left_fromShoulder_angle11 = cal_angle(point11_LShoulder, point11_LElbow, point11_LWrist)
            right_fromShoulder_angle22 = cal_angle(point22_RShoulder, point22_RElbow, point22_RWrist)
            left_fromShoulder_angle22 = cal_angle(point22_LShoulder, point22_LElbow, point22_LWrist)

            CompareFromREar2 = abs(right_fromEar_angle11-right_fromEar_angle22)
            CompareFromLEar2 = abs(left_fromEar_angle11-left_fromEar_angle22)
            CompareFromRShoulder2 = abs(left_fromEar_angle11-left_fromEar_angle22)
            CompareFromLShoulder2 = abs(left_fromShoulder_angle11-left_fromShoulder_angle22)

            print(CompareFromREar2)
            print(CompareFromLEar2)
            print(CompareFromRShoulder2)
            print(CompareFromLShoulder2)


            if ((CompareFromREar2 <= 30) and (CompareFromLEar2 <= 30) and (CompareFromRShoulder2 <= 30)
                    and (CompareFromLShoulder2 <= 30)):
                good(session)
                break
            else:
                bad(session)
        except IndexError as e:
            print(e)
            tryagain(session)

    # Conclusion
    concl(session)


