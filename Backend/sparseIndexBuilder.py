from langchain.retrievers import BM25Retriever




# BM25 aims to find the best matching documents for a given search query by considering the frequency of terms, their rarity across documents, and adjusting for document length. It strikes a balance between precision and recall in information retrieval systems.
def buildSparseIndex():
    #dynamic import - load only after init in parent module
    from vectorBuilder import documents
    print("Building sparse index on server startup ... ")
    bm25_retriever = BM25Retriever.from_documents(documents) 
    bm25_retriever.k = 2

    return bm25_retriever