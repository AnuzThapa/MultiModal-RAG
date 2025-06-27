import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.retrievers.multi_vector import MultiVectorRetriever
from src.chains import text_and_table_summarization_chain,image_summarization_chain
from src.preprocess import tables,texts,images
from langchain.storage import LocalFileStore
import json

# The vectorstore to use to index the child chunks

embedding_function = OllamaEmbeddings(
    model="nomic-embed-text:latest",  # or "mxbai-embed-large", etc.
    base_url="http://localhost:11434"  # Default Ollama endpoint
)
vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=embedding_function,persist_directory="./chroma_db" )

# The storage layer for the parent documents
# store = InMemoryStore()
store = LocalFileStore("./docstore")
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    # collection_name="multi_modal_rag",
    docstore=store,
    id_key=id_key,
)



# text_summaries=text_and_table_summarization_chain().batch(texts,{"max_concurrency": 3})
# doc_ids = [str(uuid.uuid4()) for _ in texts]
# summary_texts = [
#     Document(page_content=summary, metadata={id_key: doc_ids[i]}) for i, summary in enumerate(text_summaries)
# ]
# retriever.vectorstore.add_documents(summary_texts)
# serialized_texts = [str(text).encode('utf-8') for text in texts]
# retriever.docstore.mset(list(zip(doc_ids, serialized_texts)))  



#store summaries in the vectorstore
# retriever.docstore.mset(list(zip(doc_ids, texts)))    #store original texts i.e. list of chunks in the docstore


# Add tables
# tables_html = [table.metadata.text_as_html for table in tables]
# table_summaries = text_and_table_summarization_chain().batch(tables_html, {"max_concurrency": 3})
# table_ids = [str(uuid.uuid4()) for _ in tables]
# summary_tables = [
#     Document(page_content=summary, metadata={id_key: table_ids[i]}) for i, summary in enumerate(table_summaries)
# ]
# retriever.vectorstore.add_documents(summary_tables)
# retriever.docstore.mset(list(zip(table_ids, tables)))


# Add image summaries

# image_summaries = image_summarization_chain().batch(images)
# img_ids = [str(uuid.uuid4()) for _ in images]
# summary_img = [
#     Document(page_content=summary, metadata={id_key: img_ids[i]}) for i, summary in enumerate(image_summaries)
# ]
# retriever.vectorstore.add_documents(summary_img)

# img_bytes = [img.encode("utf-8") for img in images]
# retriever.docstore.mset(list(zip(img_ids, img_bytes)))   #id for the content is the vectorstore is matched with the id in the docstore for easy fetching.

# retriever.vectorstore.persist()