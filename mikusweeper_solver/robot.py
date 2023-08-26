#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time

from mikusweeper_solver.coordinate import Coordinate, CoordinateType

class Robot():
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def start_game(self):
        time.sleep(2)
        startButton = self.driver.find_element(By.ID, "start")
        startButton.click()

    def start_moving(self):
        while(True):
            self.calculate_next_move()


    def calculate_next_move(self):
        keys = self._find_keys()
        if len(keys) != 0:
            self._move(keys[0].y, keys[0].x)
            return

        explore_tile = self._choose_tile_to_explore()
        if explore_tile is not None:
            self._move(explore_tile.y, explore_tile.x)
            return
        bombs = self._find_all_bombs()
        if len(bombs) != 0:
            self._move(bombs[0].y, bombs[0].x)
            return


    def _move(self, y: int, x: int):
       try:
        self.driver.find_element(By.ID, f"cell-{y}-{x}").click()
       except Exception:
           pass


    def _find_keys(self):
        keys = self.driver.find_elements(By.CLASS_NAME, "key")
        return self._parseCellLocations(list(keys))

    def _find_all_edge_tiles(self) -> list[Coordinate]:
        moves = []
        for number in range(1, 5):
            class_pattern = f"c{number}"
            unfiltered = self.driver.find_elements(By.CLASS_NAME, class_pattern)
            moves.extend(unfiltered)
        return self._parseCellLocations(moves)

    def _choose_tile_to_explore(self) -> Coordinate|None:
        all_explorable_tiles = self._find_all_explorable_tiles()
        if len(all_explorable_tiles) == 0:
            return None
        return min(all_explorable_tiles, key=lambda x: all_explorable_tiles[x])


    def _find_all_explorable_tiles(self) -> dict[Coordinate, int]:
        all_edge_tiles = self._find_all_edge_tiles()

        tiles = {}
        for tile in all_edge_tiles:
            for y in range(-1,2):
                for x in range(-1,2):
                    if x == 0 and y == 0:
                        continue
                    if (tile.y + y <= 0) or (tile.x + x <= 0):
                        continue
                    explorable_tile =  self._get_explorable_tile(tile.y + y, tile.x + x)
                    if explorable_tile is not None:
                        if explorable_tile not in tiles:
                            tiles[explorable_tile] = tile.type.value
                        else:
                            tiles[explorable_tile] += tile.type.value
            # tiles.add(self._get_tile(tile.y + 1, tile.x))
            # tiles.add(self._get_tile(tile.y - 1, tile.x))
            # tiles.add(self._get_tile(tile.y + 1, tile.x + 1))
            # tiles.add(self._get_tile(tile.y - 1, tile.x - 1))
            # tiles.add(self._get_tile(tile.y - 1, tile.x + 1))
            # tiles.add(self._get_tile(tile.y + 1, tile.x - 1))
            # tiles.add(self._get_tile(tile.y, tile.x + 1))
            # tiles.add(self._get_tile(tile.y, tile.x - 1))
        return tiles


    def _get_explorable_tile(self, y, x) -> Coordinate|None:
        try:
            element = self.driver.find_element(By.ID, f"cell-{y}-{x}")
        except Exception:
            return None
        coordinate_type = CoordinateType.from_element(element)
        if coordinate_type is not CoordinateType.COVERED:
            return None
        return Coordinate(y, x, coordinate_type)


    def _find_all_bombs(self):
        bombs = self.driver.find_elements(By.CLASS_NAME, "bomb")
        return self._parseCellLocations(bombs)

    def _parseCellLocations(self, cell_elements) -> list[Coordinate]:
        return [i for i in map(lambda x: self._parseCellLocation(x), cell_elements) if i is not None]

    def _parseCellLocation(self, cell_element: WebElement) -> Coordinate|None:
        id = cell_element.get_attribute("id")
        if id is None:
            return None
        y, x = id.strip("cell-").split("-")
        return Coordinate(int(y), int(x), CoordinateType.from_element(cell_element))


    def describe(self):
        print(vars(self))
