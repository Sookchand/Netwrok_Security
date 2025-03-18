import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, message: Exception, sys_module: any):
        self.message = message
        _, _, self.traceback = sys_module.exc_info()
        super().__init__(self.message)

    def __str__(self):
        if self.traceback:
            return f"{self.message} at line {self.traceback.tb_lineno}"
        else:
            return f"{self.message} (traceback not available)"


# class NetworkSecurityException(Exception):
#     def __init__(self,error_message,error_details:sys):
#         self.error_message = error_message
#         _,_,exc_tb = error_details.exc_info()
        
#         self.lineno=exc_tb.tb_lineno
#         self.file_name=exc_tb.tb_frame.f_code.co_filename 
    
#     def __str__(self):
#         return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
#         self.file_name, self.lineno, str(self.error_message))
        
# if __name__=='__main__':
#     try:
#         logger.logging.info("Enter the try block")
#         a=1/0
#         print("This will not be printed",a)
#     except Exception as e:
#            raise NetworkSecurityException(e,sys)