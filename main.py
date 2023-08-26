#!/usr/bin/env python3
from mikusweeper_solver.robot import Robot
import time

def main():
   url = 'http://mikusweeper.chals.sekai.team/'
   robot = Robot(url=url)
   print("Beginning game")
   print('==Using Robot==')
   robot.describe()
   robot.startGame()
   time.sleep(1)
   robot.start_moving()


if __name__ == "__main__":
    main()
