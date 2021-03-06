# post to net : add -> commit -> push
# update to net : pull
import qi
import argparse
import sys
import math
import almath
import time

def main(session):
    motion_service  = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    motion_service.setStiffnesses("Head", 1.0)

    names      = "RShoulderPitch"
    angleLists = 0*almath.TO_RAD
    timeLists  = 2.0
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    motion_service.openHand('RHand')
    motion_service.closeHand('RHand')

    names      = "RShoulderPitch"
    angleLists = 90.0*almath.TO_RAD
    timeLists  = 2.0
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    names      = "RWristYaw"
    angleLists = 75.0*almath.TO_RAD
    timeLists  = 2.0
    isAbsolute = True
    motion_service.angleInterpolation(names, angleLists, timeLists, isAbsolute)

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
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)