# from langchain_core.runnables import RunnablePassthrough, RunnableLambda
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain_ollama import ChatOllama
# from src.vectorstore import retriever
# from base64 import b64decode
# import base64
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# import os

# def parse_docs(docs):
#     b64 = []
#     text = []
#     print(f"--- Starting parse_docs with {len(docs)} docs ---")
#     for doc in docs:

#         try:
#             base64_string = doc.decode('utf-8')
#             b64decode(base64_string)
#             b64.append(base64_string)
#         except Exception as e:
#             text.append(doc)
#     return {"images": b64, "texts": text}


# def build_prompt(kwargs):

#     docs_by_type = kwargs["context"]
#     user_question = kwargs["question"]

#     context_text = ""
#     if len(docs_by_type["texts"]) > 0:
#         for text_element in docs_by_type["texts"]:
#             # context_text += text_element.text
#              if isinstance(text_element, bytes):
#                 context_text += text_element.decode('utf-8')
#              else:
#                 context_text += text_element

#     # construct prompt with context (including images)
#     prompt_template = f"""
#     Answer the question based only on the following context, which can include text, tables, and the below image.
#     Context: {context_text}
#     Question: {user_question}
#     """

#     prompt_content = [{"type": "text", "text": prompt_template}]

#     if len(docs_by_type["images"]) > 0:
#         for image in docs_by_type["images"]:
#             prompt_content.append(
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/jpeg;base64,{image}"},
#                 }
#             )

#     return ChatPromptTemplate.from_messages(
#         [
#             HumanMessage(content=prompt_content),
#         ]
#     )


# chain = (
#     {
#         "context": retriever | RunnableLambda(parse_docs),   #separates the retrieved documents into images and texts
#         "question": RunnablePassthrough(),   # forward the input question unchanged
#     }
#     | RunnableLambda(build_prompt)   #take the context and question from the first step and build the prompt using build_prompt function
#     | ChatOllama(model="gemma3:latest")
#     | StrOutputParser()
# )
# # RunnableLambda is used to plug the function into the chain.converts the function to chainable format.

# chain_with_sources = {
#     "context": retriever | RunnableLambda(parse_docs),
#     "question": RunnablePassthrough(),
# } | RunnablePassthrough().assign(
#     response=(
#         RunnableLambda(build_prompt)
#         | ChatOllama(model="llama3.2:latest")
#         | StrOutputParser()
#     )
# )
# # this returns both the separated context or sources fetched from vectorstore and the models repsonse.

# while(True):
#     print("Type 'exit' to quit the program.")
#     query=input("Enter your query here:")
#     if query.lower() == 'exit':
#         break
#     else:
#         response = chain_with_sources.invoke(query)
#         # print(response)
#         # print(type(response))
#         # response_text = response.get('response')
#         # print("Response:", response_text)

#         print("\n\nContext:")
#         for text in response['context']['texts']:
#             if isinstance(text, bytes):
#                 text = text.decode('utf-8')  # Or the correct encoding for your data
#                 print("text-code:",text)
#             else:
#                 print(text.text) 
#             # print("Page number: ", text.metadata.page_number)
#             print("\n" + "-"*50 + "\n")

#         def save_base64_image(image_base64, filename):
#             image_data = base64.b64decode(image_base64)

#             with open(filename, "wb") as f:
#                 f.write(image_data)

#         # Directory to save images
#         output_dir = "saved_images"
#         os.makedirs(output_dir, exist_ok=True)

#         # Loop over all images in response and save them
#         for idx, image_base64 in enumerate(response['context']['images']):
#             filename = os.path.join(output_dir, f"image_{idx+1}.png")  # You can change extension if needed
#             save_base64_image(image_base64, filename)
#             print(f"Saved: {filename}")



import streamlit as st
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from src.vectorstore import retriever
from base64 import b64decode
import base64
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# --------- Document Parsing ---------
def parse_docs(docs):
    b64 = []
    text = []
    for doc in docs:
        try:
            base64_string = doc.decode('utf-8')
            b64decode(base64_string)  # Check if it's valid base64
            b64.append(base64_string)
        except Exception:
            text.append(doc)
    return {"images": b64, "texts": text}

# --------- Prompt Builder ---------
def build_prompt(kwargs):
    docs_by_type = kwargs["context"]
    user_question = kwargs["question"]

    context_text = ""
    if len(docs_by_type["texts"]) > 0:
        for text_element in docs_by_type["texts"]:
            if isinstance(text_element, bytes):
                context_text += text_element.decode('utf-8')
            else:
                context_text += text_element.text if hasattr(text_element, 'text') else str(text_element)

    prompt_template = f"""
    Answer the question based only on the following context, which can include text, tables, and images below.
    Context: {context_text}
    Question: {user_question}
    """

    prompt_content = [{"type": "text", "text": prompt_template}]

    if len(docs_by_type["images"]) > 0:
        for image in docs_by_type["images"]:
            prompt_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
            })

    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

# --------- LangChain Chain ---------
chain_with_sources = {
    "context": retriever | RunnableLambda(parse_docs),
    "question": RunnablePassthrough(),
} | RunnablePassthrough().assign(
    response=(
        RunnableLambda(build_prompt)
        | ChatOllama(model="llama3.2:latest")
        | StrOutputParser()
    )
)

# --------- Streamlit UI ---------
st.set_page_config(page_title="Multimodal RAG Chatbot", layout="wide")
st.title("🧠📷 Multimodal RAG Chatbot (Text + Images)")

query = st.text_input("Enter your query:")

if query:
    with st.spinner("Fetching and generating response..."):
        response = chain_with_sources.invoke(query)

    # --------- Display Model's Final Answer ---------
    st.markdown("## 💬 Model Response")
    st.write(response["response"])

    # --------- Display Retrieved Texts ---------
    st.markdown("---")
    st.markdown("## 📄 Retrieved Text Context")
    for idx, text_doc in enumerate(response["context"]["texts"]):
        st.markdown(f"**Text {idx+1}:**")
        if isinstance(text_doc, bytes):
            st.text(text_doc.decode('utf-8'))
        else:
            st.text(text_doc.text if hasattr(text_doc, 'text') else str(text_doc))

    # --------- Display Images Inline ---------
    st.markdown("---")
    st.markdown("## 🖼️ Retrieved Images")

    for idx, image_base64 in enumerate(response["context"]["images"]):
        try:
            image_data = base64.b64decode(image_base64)
            st.image(image_data, caption=f"Image {idx+1}", width=300)
        except Exception as e:
            st.warning(f"Failed to display image {idx+1}: {e}")
