from typing import List, Tuple
import math
from copy import deepcopy

class Walker:

    class Memento:
        coordinate: Tuple[int, int]
        action_list: List[str]
        def __init__(self, coordinate: Tuple[int, int], action_list: List[str]) -> None:
            self.coordinate = coordinate
            self.action_list:List[str] = action_list
        
    def __init__(self, current_coordinate:Tuple[int, int], target_coordinate: Tuple[int, int]) -> None:
        self.__current_coordinate = current_coordinate  # 현재 좌표
        self.__target_coordinate = target_coordinate   # 목적지 좌표
        self.__action_list:List[str] = []

    def walk(self, action:str) -> float:
        self.__action_list.append(action)
        
        if action == 'UP':
            self.__current_coordinate = (self.__current_coordinate[0], self.__current_coordinate[1] + 1)
        elif action == 'DOWN':
            self.__current_coordinate = (self.__current_coordinate[0], self.__current_coordinate[1] - 1)
        elif action == 'LEFT':
            self.__current_coordinate = (self.__current_coordinate[0] - 1, self.__current_coordinate[1])
        elif action == 'RIGHT':
            self.__current_coordinate = (self.__current_coordinate[0] + 1, self.__current_coordinate[1])
        else:
            raise ValueError('Invalid action')

        return self.__calculate_distance()

    def __calculate_distance(self) -> float:
        '''현재 좌표와 목적지 좌표의 거리를 계산하여 반환한다.'''
        # math.pow(x, y) : x의 y제곱
        # math.sqrt(x) : x의 제곱근
        return math.sqrt(math.pow(self.__current_coordinate[0] - self.__target_coordinate[0], 2)\
                         + math.pow(self.__current_coordinate[1] - self.__target_coordinate[1], 2))

    def create_memento(self) -> Memento:        
        return Walker.Memento(tuple(self.__current_coordinate), self.__action_list.copy())

    def restore_memento(self, memento:Memento) -> None:
        self.__current_coordinate = tuple(memento.coordinate)
        self.__action_list = memento.action_list.copy()

    def __str__(self) -> str:
        return str(self.__action_list)


if __name__ == '__main__':
    import random
    
    walker = Walker((0, 0), (10, 10))
    actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    min_distance = 999999999.0000
    memento = None

    while True:
        action = actions[int(random.randrange(0, len(actions)))]
        distance = walker.walk(action)
        print(f'{action} : {distance}')

        if distance <= 0.0001:
            break

        if min_distance > distance:
            min_distance = distance
            memento = walker.create_memento()
        else:
            if memento != None:
                walker.restore_memento(memento)
                print(f'Restore : {action}')

    print("walker's path : ", walker)
        

        
