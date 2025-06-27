from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
def text_and_table_summarization_chain():
        # Prompt
        prompt_text = """
        You are an assistant tasked with summarizing tables and text.
        Give a concise summary of the table or text.

        Respond only with the summary, no additionnal comment.
        Do not start your message by saying "Here is a summary" or anything like that.
        Just give the summary as it is.

        Table or text chunk: {element}

        """
        prompt = ChatPromptTemplate.from_template(prompt_text)

        # Summary chain
        model = ChatOllama(temperature=0.5, model="gemma3:latest")
        summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

        return summarize_chain



def image_summarization_chain():

        prompt_template = """Describe the image in detail. For context,
                        the image is part of a research paper explaining the transformers
                        architecture. Be specific about graphs, such as bar plots."""
        messages = [
            (
                "user",
                [
                    {"type": "text", "text": prompt_template},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64,{image}"},
                    },
                ],
            )
        ]

        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | ChatOllama(model="gemma3:latest") | StrOutputParser()
        # image_summaries = chain.batch(images)

        return chain