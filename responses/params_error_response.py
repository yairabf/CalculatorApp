from responses.abstract_response import AbstractResponse


class ParamsErrorResponse(AbstractResponse):

    def __init__(self, parameters):
        self.parameters = parameters
        """
        todo: add initialize
        """
