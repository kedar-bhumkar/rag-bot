from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

documents = None

def buildVectorIndex():
    global documents
    print("Building index on server startup ... ")
    loader = CSVLoader(file_path='./data/support-bot.csv')
    #loader = CSVLoader(file_path='./data/FinalPrep2.txt', encoding="utf8")
    
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)
    vector = FAISS.from_documents(documents, OpenAIEmbeddings()).as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 5} )
    
    return vector    