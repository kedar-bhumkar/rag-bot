import re


pattern = re.compile(r'Notes:(.*)', re.DOTALL)

def getContext(vector, input):
    print('Recvd input : ', input )  
    ret_context = vector.similarity_search_with_score(input)
    #context = retriever.get_relevant_documents(input)[0].page_content
    context = ret_context[0][0].page_content
    print("The  context.......:",ret_context[0][0].page_content)
    score =  ret_context[0][1]
    print("The score .......", score)
    
    match = pattern.search(context)
    print("match", match)
    #print("context:", context)

    if match and score < 0.49:
        # Extract the text after 'Notes'
        notes_text = match.group(1).strip()
        print("Context found")
    else:
        print("Notes not found in the context.")
        notes_text = "No context found"


    return notes_text

#from fast_api_chat_server import vector