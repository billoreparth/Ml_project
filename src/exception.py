import sys 
import logging 



def error_message(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    exc_message="Error occured in python script name [{0}] and line number is [{1}] , error message is [{2}] ".format(
        file_name,exc_tb.tb_lineno,str(error))
    
    return exc_message
    
class CustomException(Exception):
    def __init__(self,exc_message,error_detail:sys):
        super().__init__(exc_message)
        self.exc_message=error_message(exc_message,error_detail=error_detail)

    def __str__(self):
        return self.exc_message

