from vectorBuilder import *
from sparseIndexBuilder import *
from constants import *
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.llms import Cohere
from langchain.retrievers import EnsembleRetriever

def getRetreiver():
    sparseIndex = None    

    vector = buildVectorIndex()
    print("vector", vector)

    if(ENABLE_HYBRID_SEARCH):
        sparseIndex = buildSparseIndex()
    
    print("sparseIndex ", sparseIndex)


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
    if(ENABLE_HYBRID_SEARCH):
        # initialize the ensemble retriever
        print("Using hybrid search ...")
        multi_retriever = EnsembleRetriever(retrievers=[sparseIndex, compression_retriever], weights=[0.5, 0.5])
    else:
        print("Bypassing  hybrid search ...")
        multi_retriever = compression_retriever


    return multi_retriever