from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import re
from functools import lru_cache

from fast_api_chat_server import vector1

pattern = re.compile(r'Notes:(.*)', re.DOTALL)

def getContext(input):

    print('Recvd input : ', input )

    #vector = buildIndex("idx")
    #retriever = vector.as_retriever(search_kwargs={"score_threshold": 0.9})
    
    
    ret_context = vector1.similarity_search_with_score(input)
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

@lru_cache(maxsize=2)
def buildIndex(idx):
    print("If here then cache was missed ... ")

    loader = CSVLoader(file_path='./data/support-bot.csv')
    docs = loader.load()

    #print("\n",docs)

    documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)

    #documents = CharacterTextSplitter(separator="\n",chunk_size=1000, chunk_overlap=0,length_function=len,is_separator_regex=False).create_documents(docs)


   # print("\n\n\n",documents)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings())

    return vector    
#print(getContext(""))