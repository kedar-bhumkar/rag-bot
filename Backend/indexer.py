from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.llms import Cohere
from langchain.retrievers import EnsembleRetriever
from constants import *


def getContext(input):
    #dynamic import - load only after init in parent module
    from fast_api_chat_server import vector, sparseIndex
    print('Recvd input : ', input )  
      

    if(ENABLE_RE_RANKING):
        print('Using vector + reranking search ....')
        llm = Cohere(temperature=0)
        compressor = CohereRerank()
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=vector
        )
    else:
        print('Bypassing reranking ....')
        compression_retriever = vector

    # Non-hybrid search option
    if(sparseIndex != None):
        # initialize the ensemble retriever
        print("Using hybrid search ...")
        multi_retriever = EnsembleRetriever(retrievers=[sparseIndex, compression_retriever], weights=[0.5, 0.5])
    else:
        print("Bypassing  hybrid search ...")
        multi_retriever = compression_retriever
        

    compressed_docs = multi_retriever.get_relevant_documents(input)
    #pretty_print_docs(compressed_docs)
    

    context = compressed_docs[0].page_content
    print("The  context.......:", context)
    
    return context



def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

