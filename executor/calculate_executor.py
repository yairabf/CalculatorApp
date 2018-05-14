from executor.abstract_executor import *
import json

class CalculateExecutor(AbstractExecutor):

    def __operation(self,x,y,operation):
        if operation == '+':
            return str(int(x)+int(y))
        if operation == '-':
            return str(int(x)-int(y))
        if operation == '*':
            return str(int(x)*int(y))
        if operation == '/' and not y == '0' :
            return str(int(x)/int(y))
        if operation == '/' and  y == '0':
            return "BAD OPERATION"



    def __is_operator(self, input):
        return input in ['+', '-', '/', '*']

    def __is_equal_sign(self, input):
        return input == '='

    def __handle_first_interaction(self,input):
        # first interaction with user
        first_number = '0'
        operator = None
        if self.__is_operator(input) or self.__is_equal_sign(input):
            display = '0'
            if self.__is_operator(input):
                operator = input
        else:
            display = input
            first_number = input
        return {'status':'success','display': display, 'operator': operator, 'first_number': first_number, 'second_number': ''}

    def __handle_interaction(self,input,state):
        # not in a middle of operation & got an operation (it's not first interaction so we assume first_number!=None)
        # 55 and got + => 55+
        #1
        if state['operator'] is None and self.__is_operator(input):
            print(">> 1\n")
            return {'status':'success','display': state['first_number'], 'operator': input, 'first_number': state['first_number'],
                    'second_number': ''}
        # not in a middle of operation & got a number, concat to previous number
        # 55 and got 6 => 556
        # 2
        if state['operator'] is None and not (self.__is_operator(input) or self.__is_equal_sign(input)):
            print(">> 2\n")
            first_number = state['first_number'] + input
            return {'status':'success','display': first_number, 'operator': None, 'first_number': first_number, 'second_number': ''}
        # not in a middle of operation & got =
        # 55 and got = => 55
        # 3
        if state['operator'] is None and self.__is_equal_sign(input):
            print(">> 3\n")
            return {'status':'success','display': state['first_number'], 'operator': None,
                    'first_number': state['first_number'],'second_number': ''}
        # in a middle of operation & got a number
        # 55+ and got 6 => 55+6
        # 4
        if (not state['operator'] is None) and not (self.__is_equal_sign(input) or self.__is_operator(input)):
            print(">> 4\n")
            second_number = state['second_number'] + input
            return {'status':'success','display':second_number, 'operator': state['operator'],
                    'first_number': state['first_number'], 'second_number': input}
        # in a middle of operation & got an operation & second number is ''
        # 55+ and got - => 55-
        # 5
        if (not (state['operator'] is None)) and self.__is_operator(input) and state['second_number']=='':
            print(">> 5\n")
            return {'status':'success','display': state['second_number'], 'operator': state['operator'],
                    'first_number': state['first_number'], 'second_number': state['second_number']}
        # in a middle of operation & got an operation & second number exist
        #55+6 and got - => 61-
        # 6
        if (not (state['operator'] is None)) and self.__is_operator(input) and not state['second_number'] == '':
            print(">> 6\n")
            first_number=self.__operation(state['first_number'],state['second_number'],state['operation'])
            #possible dividing by zero
            if first_number is "BAD OPERATION":
                return "BAD OPERATION"
            return {'status':'success','display': first_number, 'operator': state['operator'],
                    'first_number': state['first_number'], 'second_number': ''}
        # in a middle of operation & got equal sign & second number exist
        #55+6 and got = => 61
        # 7
        if (not (state['operator'] is None)) and self.__is_equal_sign(input) and not state['second_number'] == '':
            print(">> 7\n")
            first_number = self.__operation(state['first_number'], state['second_number'], state['operator'])
            # possible dividing by zero
            if first_number is "BAD OPERATION":
                return "BAD OPERATION"
            return {'status':'success','display': first_number, 'operator': None,
                    'first_number':first_number, 'second_number': ''}
        # in a middle of operation & got equal sign & second number is ''
        #55+ and got = => 55
        # 8
        if (not (state['operator'] is None)) and self.__is_equal_sign(input) and not state['second_number'] == '':
            print(">> 8\n")
            return {'status':'success','display': state['first_number'], 'operator': None,
                    'first_number': state['first_number'], 'second_number': ''}


    def execute(self, args):
        input=args['input']


        if not 'calculatorState' in args.keys():
            return self.__handle_first_interaction(input)
        else:
            state = args['calculatorState']
            return self.__handle_interaction(input,state)

        return