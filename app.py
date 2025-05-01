# app.py

import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import altair as alt
import os

# Import your custom modules
from data_handler import refine_response, data_handler
from components import BigQueryManager, embeddings, initialize_components, generate_initial_response, vector_store
from prompts import SYSTEM_PROMPT, redefine
from langchain_core.messages import AIMessage, SystemMessage

# Enable Altair charts to render in browser
alt.renderers.enable('default')

# Initialize Gemini API
gemini_api_key = "AIzaSyAvPY9KmVoZMmTHEe0CpBnnXhy-IBXI7js"

# Initialize BigQuery Manager
bq_manager = initialize_components()

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define Graph
graph_builder = StateGraph(State)

# Node functions
def check_sql_generation(state: State, system_prompt=SYSTEM_PROMPT, vector_store=vector_store, embeddings=embeddings):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)
    user_input = state["messages"][-1].content
    response = generate_initial_response(user_input, llm, vector_store)
    return {"messages": [response]}

def chatbot2(state: State, system_prompt=redefine):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)
    system_message = SystemMessage(content=system_prompt)
    messages_with_system = [system_message] + state["messages"]
    llm_response = llm.invoke(messages_with_system)
    return {"messages": [llm_response.content]}

def chatbot3(state: State, bq_manager=bq_manager):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)
    last_message = state["messages"][-1].content
    query = refine_response(last_message)
    user_input = state["messages"][-2].content
    bq_manager = initialize_components()
    data = bq_manager.execute_query(query)

    if isinstance(data, pd.DataFrame) and not data.empty:
        summary_text, chart = data_handler(data, user_input, llm)
        if chart is not None:
            st.altair_chart(chart, use_container_width=True)
    else:
        summary_text = "No data available to display."

    return {"messages": [summary_text]}

def check_condition(state: State):
    if "I cannot generate a SQL query for this request based on the provided schema" in state["messages"][-1].content:
        return "chatbot2"
    else:
        return "chatbot3"

# Build the graph
graph_builder.add_node("chatbot1", check_sql_generation)
graph_builder.add_node("chatbot2", chatbot2)
graph_builder.add_node("chatbot3", chatbot3)
graph_builder.add_edge(START, "chatbot1")
graph_builder.add_conditional_edges("chatbot1", check_condition, {
    "chatbot2": "chatbot2",
    "chatbot3": "chatbot3",
})
graph_builder.add_edge("chatbot2", END)
graph_builder.add_edge("chatbot3", END)

graph = graph_builder.compile()

# Streamlit App
st.set_page_config(page_title="Data Analyst Bot", page_icon="📊", layout="wide")

st.title("📊 Intelligent Data Analysis Assistant")
st.write("Ask questions and get insights + charts directly from your database!")

user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input.strip() != "":
        with st.spinner("Generating response..."):
            for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
                for value in event.values():
                    assistant_response = value["messages"][-1]
                    if "SELECT" not in assistant_response:  # This ensures the SQL query isn't shown
                        st.write(assistant_response)

    else:
        st.warning("Please enter a query to continue.")
