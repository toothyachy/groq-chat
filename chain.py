from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import streamlit as st
import os

os.environ["TAVILY_API_KEY"] = st.secrets["tavily_api_key"]
os.environ["GROQ_API_KEY"] = st.secrets["groq_api_key"]

llm = ChatGroq(temperature=0.8, model_name="mixtral-8x7b-32768")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are Slartibartfast from the Hitchhiker's Guide to the Galaxy. Many beings have travelled far and wide to seek your wisdom. Only answer the question based on the provided context: '{context}'. Your reply to the user should start a funny opening line, and end with a 'Sources' list of the website links given in the context.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

retriever = TavilySearchAPIRetriever(k=5)
# print(retriever.invoke("Where is Magrathea"))

chain = (
    RunnablePassthrough.assign(context=(lambda x: x["question"]) | retriever)
    | prompt
    | llm
)

store = st.session_state


def get_message_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_message_history,
    input_messages_key="question",
    history_messages_key="history",
)
