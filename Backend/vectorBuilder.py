from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

documents = None

def buildVectorIndex():
    global documents
    print("Building index on server startup ... ")
    embeddings = OpenAIEmbeddings()
    db=None
    db = FAISS.load_local("faiss_index", embeddings)
    print('db', db)
    if(db == None):
        print('Inside db is NONE')
        db = FAISS.from_documents(documents, OpenAIEmbeddings())
        db.save_local("faiss_index")
        
    documents = load_docs()
    vector = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 5} )        
    
    return vector    

def load_docs():
        loader = CSVLoader(file_path='./data/support-bot.csv')
        #loader = CSVLoader(file_path='./data/FinalPrep2.txt', encoding="utf8")        
        docs = loader.load()
        return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)


buildVectorIndex()