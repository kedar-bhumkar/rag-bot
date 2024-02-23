from constants import *

def getContext(input):
    #dynamic import - load only after init in parent module
    from fast_api_chat_server import multi_retriever
    print('Recvd input : ', input )  

    compressed_docs = multi_retriever.get_relevant_documents(input)
    pretty_print_docs(compressed_docs)
    
    if(ENABLE_MULTI_CHUNK_CONTEXT):
        print("Multi chunking context enabled ....")
        context = ''.join(d.page_content  for i, d in enumerate(compressed_docs))
    else:
        print("Single chunking context enabled ....")
        context = compressed_docs[0].page_content
    
    print("The  context.......:", context)    
    return context



def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

