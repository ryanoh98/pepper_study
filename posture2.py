def posture2(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses(["Head", "Shoulder"], [1.0, 1.0])
    names            = ["HeadYaw", "HeadPitch", "LShoulderRoll", "RShoulderRoll"]
    angles           = [0.0*almath.TO_RAD, -35.0*almath.TO_RAD, 48.0*almath.TO_RAD, 48.0*almath.TO_RAD]
    fractionMaxSpeed = 0.4
    motion_service.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(5)

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

    posture2(session)