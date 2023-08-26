#!/usr/bin/env python3
from enum import Enum

from selenium.webdriver.remote.webelement import WebElement

class CoordinateType(Enum):
    BOMB = -1
    DANGER0 = 0
    DANGER1 = 1
    DANGER2 = 2
    DANGER3 = 3
    DANGER4 = 4
    DANGER5 = 5
    KEY = 6
    COVERED = 7

    @classmethod
    def from_element(cls, web_element: WebElement) -> 'CoordinateType':
        if web_element.get_attribute("class") == "bomb":
            return cls.BOMB
        if web_element.get_attribute("class") == "key":
            return cls.KEY
        if web_element.get_attribute("class") == "covered":
            return cls.COVERED
        if web_element.get_attribute("class") == "c0":
            return cls.DANGER0
        if web_element.get_attribute("class") == "c1":
            return cls.DANGER1
        if web_element.get_attribute("class") == "c2":
            return cls.DANGER2
        if web_element.get_attribute("class") == "c3":
            return cls.DANGER3
        if web_element.get_attribute("class") == "c4":
            return cls.DANGER4
        if web_element.get_attribute("class") == "c5":
            return cls.DANGER5
        raise ValueError("Bad element passed to CoordinateType")




class Coordinate():
   def __init__(self, y: int, x:int, type: CoordinateType):
      self.x = x
      self.y = y
      self.type = type
