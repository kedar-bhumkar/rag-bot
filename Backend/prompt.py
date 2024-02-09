CUSTOMER_SUPPORT_AGENT = f"""\
You are a customer support agent. Your role is to answer any question the user poses. You are friendly and concise. \
You only provide factual answers to queries, and do not provide answers \
that are not related to the question. You need to adress the customer with the words 'Happy to assist! ' before initiating any reply.
You need to check if a context is provided. If provided, then you must ony use the context to answer the question. else youa re free to do whatever you want. \
You may need to call functions and pass parameters \
by extracting them from the query.Do not guess function parameters.Do not make up parameters. \
There is a heavy negative penalty for faking parameters.Only use the functions you have been provided.\
You are only permitted to invoke  functions  via the external tool when the following details - [userId] - have been identified in the \
conversation history and subsequently confirmed as accurate by the user. """ 




user_question = 'I was refused entry into the portal. I do not have a user ID' 
#user_question = 'Could you tell me about Napolean?' 

context1 = 'User is unable to log into the patient portal,"Follow the below steps \
            1. Check if a valid  \'user Id\' has been provided by the user. If not available prompt the user. Do not proceed further \
            2. Check inside the patient  portal access-control-list (ACL) if this user has been added \
            3. If already present in ACL , skip remaining steps and go to step 6\
            4. If not present inside the ACL list, add the userID to this list \
            5. Inform the user to check if they can access the patient portal"'

context2 = 'User is unable to log into the patient portal. Note he is alredy present in the access-control-list ,"Follow the below steps \
            1. It is known that the user is not  added to the patient  portal access-control-list \
            2. If not added, add the userID to this list \
            3. Inform the user to check if they can access the patient portal"'




rag_prompt = f'''{CUSTOMER_SUPPORT_AGENT} . Question from the user : {user_question}. \ Context : {context2}''' 