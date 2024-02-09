import re
from langchain.agents import tool

@tool
def addUserInACL():
        "A tool to add a user inside the patient portal access-control-list"
        return "User added successfully"    
@tool
def checkUserExitsIinACL(userId:str):
        """A tool to check if  a  user exists in  the patient portal access-control-list"
           
           returns: Outcome in String format. The outcome is either User found, Exception : User ID not provided, General Exception, User not found
           
           function arguments: userId - A string in the format 'U-random 8 digits'. For E.g.  U-99988812. It represents the users Id which is used to search if the user exists in the ACL  
        """
        print(f"user id {userId}")

        if(not is_valid_string(userId.replace(" ", ""))):
            return "Exception : User ID incorrect or not provided in expected format"    

        
        return "User does not exist in ACL"
        #return "User already exists in ACL"
        #return "Exception : User ID not provided"
    
def is_valid_string(input_string):
        print(f"input_string {input_string}")
        pattern = r'^U-\d{8}$'
        return bool(re.match(pattern, input_string))