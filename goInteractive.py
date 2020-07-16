import argparse
from robotProxy.robotProxy import baseProxy as RobotProxy

if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--toControlled", type=bool, nargs='?', const=False, default=True,
                        help="Make Peppa interactive with True or non-interactive with False")
    args = parser.parse_args()
    myRobot = RobotProxy(10, 10, 1000)
    myRobot.makeInteractive(args.toControlled)
    