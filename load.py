%pip install llama-index llama-index-vector-stores-pinecone

import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from pinecone import Pinecone, ServerlessSpec


os.environ["PINECONE_API_KEY"] =
os.environ["OPENAI_API_KEY"] =

api_key = os.environ["PINECONE_API_KEY"]

pc = Pinecone(api_key=api_key)


# delete if needed
# pc.delete_index("quickstart")


# dimensions are for text-embedding-ada-002

pc.create_index(
    name="zhoop",
    dimension=1536,
    metric="euclidean",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

# If you need to create a PodBased Pinecone index, you could alternatively do this:
#
# from pinecone import Pinecone, PodSpec
#
# pc = Pinecone(api_key='xxx')
#
# pc.create_index(
# 	 name='my-index',
# 	 dimension=1536,
# 	 metric='cosine',
# 	 spec=PodSpec(
# 		 environment='us-east1-gcp',
# 		 pod_type='p1.x1',
# 		 pods=1
# 	 )
# )
#


pinecone_index = pc.Index("zhoop")



from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from IPython.display import Markdown, display



!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'




# load documents
documents = SimpleDirectoryReader("./data/paul_graham").load_data()



# initialize without metadata filter
from llama_index.core import StorageContext

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError(f"Environment variable OPENAI_API_KEY is not set")

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)



# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("what are the fir checklist for murder?")


display(Markdown(f"<b>{response}</b>"))