from abc import ABC, abstractmethod
from typing import List

'''
<어쩔코딩 디자인패턴 스터디>

인터프리터 패턴

스터디 프레젠테이션 자료 : https://docs.google.com/presentation/d/1aC1PYHgHrgNv6p7IHYgw6Wbo8dbQE7R_jagYUf_SoZE/edit?usp=sharing
'''


class Context:
    '''
    스크립트에 대한 문자열을 받아 단어 단위로 분할하는 역할
    '''
    def __init__(self, script: str):
        self.script = script
        self.keywords = script.split(' ') # 공백문자(' ')를 기준으로 문자열 분할
        self.__current_keyword:str = None
        self.__read_index = -1
        self.read_next_keyword()

    def read_next_keyword(self) -> str:
        '''
        단어 단위로 분할된 문자열을 읽어서 반환
        '''
        if self.__read_index + 1 >= len(self.keywords):
            self.__current_keyword = None
        else:
            self.__read_index += 1
            self.__current_keyword = self.keywords[self.__read_index]
        return self.__current_keyword

    def get_current_keyword(self) -> str:
        return self.__current_keyword


class Expression(ABC):
    '''
    스크립트를 해석하고 실행하는 기능을 제공하는 인터페이스
    '''
    @abstractmethod
    def interpret(self, context: Context) -> bool:
        pass

    @abstractmethod
    def run(self) -> bool:
        pass


class BeginExpression(Expression):
    '''스크립트의 시작을 해석하는 클래스'''
    def __init__(self) -> None:
        self.__expression:CommandListExpression = None

    def interpret(self, context: Context) -> bool:
        if self.check_valid_keyword(context.get_current_keyword()):
            context.read_next_keyword()
            self.__expression = CommandListExpression()
            return self.__expression.interpret(context)
        else:
            return False

    def run(self) -> bool:
        return self.__expression.run()

    @staticmethod
    def check_valid_keyword(keyword:str)-> bool:
        return keyword == 'BEGIN'

    def __str__(self):
        return 'BEGIN ' + str(self.__expression)


class CommandListExpression(Expression):
    '''명령어 목록을 저장하는 클래스'''
    def __init__(self):
        self.__commands = []

    def interpret(self, context: Context) -> bool:
        while True:
            current_keyword = context.get_current_keyword()            
            if current_keyword is None:
                return False
            elif current_keyword == 'END':
                context.read_next_keyword()
                break
            else:
                command:CommandExpression = None

                if LoopCommandExpression.check_valid_keyword(current_keyword):
                    command = LoopCommandExpression(current_keyword)
                elif ActionCommandExpression.check_valid_keyword(current_keyword):
                    command = ActionCommandExpression(current_keyword)
                # 이후 명령어 추가

                if command is not None:
                    if command.interpret(context):
                        self.__commands.append(command)
                    else:
                        return False
                else:
                    return False
        
        return True

    def __str__(self) -> str:
        return str(self.__commands)

    def run(self) -> bool:
        '''해석된 모든 커맨드 실행'''
        for command in self.__commands:
            if not command.run():
                return False
        return True


class CommandExpression(Expression):
    '''명령어를 담을 수 있는 클래스'''
    def __init__(self, keyword:str) -> None:
        self._keyword = keyword

    def __str__(self):
        return self._keyword


class LoopCommandExpression(CommandExpression):
    @staticmethod
    def check_valid_keyword(keyword:str)-> bool:
        return keyword == 'LOOP'

    def __init__(self, keyword:str) -> None:
        super().__init__(keyword)
        self.__count = None
        self.__expression = None
        
    def interpret(self, context: Context) -> bool:
        if not self.check_valid_keyword(context.get_current_keyword()):
            return False
        
        # 반복 횟수 읽기
        count_keyword = context.read_next_keyword()
        if count_keyword is None:
            return False
        
        try:
            self.__count = int(count_keyword)
            self.__expression = CommandListExpression()

            if context.read_next_keyword() is None:
                return False
            
            return self.__expression.interpret(context)
        except ValueError:
            return False

    def __str__(self) -> str:
        return 'LOOP (' + str(self.__count) + ') ' + str(self.__expression)

    def __repr__(self) -> str:
        return 'LOOP (' + str(self.__count) + ') ' + str(self.__expression)

    def run(self) -> bool:
        '''반복문 내 명령어 실행'''
        for _ in range(self.__count):
            if not self.__expression.run():
                return False
        return True


class ActionCommandExpression(CommandExpression):
    @staticmethod
    def check_valid_keyword(keyword:str)-> bool:
        action_keywords = ['FRONT', 'BACK', 'LEFT', 'RIGHT']
        return keyword in action_keywords

    def __init__(self, keyword:str) -> None:
        super().__init__(keyword)

    def interpret(self, context: Context) -> bool:
        if not self.check_valid_keyword(context.get_current_keyword()):
            return False
        if context.read_next_keyword() is None:
            return False
        return True        

    def run(self) -> bool:
        '''명령어 실행'''
        print("CMD : ", self._keyword)
        return True

    def __str__(self) -> str:
        return self._keyword

    def __repr__(self) -> str:
        return self._keyword


if __name__ == '__main__':
    script = 'BEGIN FRONT LOOP 3 LOOP 2 RIGHT FRONT END LOOP 3 LEFT END BACK RIGHT END BACK END'
    context = Context(script)        
    expression = BeginExpression()
    
    print("script : ", script)

    if expression.interpret(context):
        print("interpreted : ", expression)
        expression.run()
    else:
        print("interpret failed")