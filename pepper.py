import qi
import math
import sys

# post to net : add -> commit -> push
# update to net : pull
## add comment
def main():
    session = qi.Session()
    ip = '192.168.1.45'
    port = '9559'
    try:
        session.connect("tcp://" + ip + ":" + str(port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # Get the services ALMotion and ALRobotPosture
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Pose Init
    posture_service.goToPosture("StandInit", 0.5)

    # Call Pepper


    # Say "What can I help you, sir?"


    # Coffee!


    # Say "Yes, sir."


    # Send robot to the refrigerator
    # Use several "moveTo" commands
    # Example of the command
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)

    # Open the right hand
    motion_service.openHand('RHand')

    # Raise the right arm


    # Move robot to the left a bit to grab
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)


    # Close the right hand
    motion_service.closeHand('RHand')

    # Move back to open the refrigerator
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)

    # Release the refrigerator (Open the hand and move back a bit)
    motion_service.openHand('RHand')
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)

    # Send robot to Pose Init
    posture_service.goToPosture("StandInit", 0.5)


    # Place robot in front of the refrigerator (not close enough)
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)


    # Raise the right arm


    # Open the right hand
    motion_service.openHand('RHand')

    # Move forward a bit
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)


    # Close the right hand to grab
    motion_service.closeHand('RHand')

    # Move backward
    x  = 0.2
    y  = 0.2
    theta  = math.pi/2
    motion_service.moveTo(x, y, theta)


    # Arm with 45 degrees


    # Come back to the origin


    # Drop the coffee


    # Say "Here you are, sir. Enjoy!"


    # Move backward a bit


    # Bow


    # Send robot to Pose Init
    posture_service.goToPosture("StandInit", 0.5)

    # Go to rest position
    motion_service.rest()

if __name__ == "__main__":
    main()