# 📘 Streamlit App: Chatbot for Data Analytics using LangGraph, Gemini API, BigQuery, and Altair

## ✨ Overview

The app allows users to interact with a data analysis bot that generates SQL queries based on user input, executes them on a database, and provides insights in the form of text summaries and visual charts.

The system allows a user to input a natural query (e.g., "Show a bar chart of students with GPA > 3"), automatically generates and runs SQL, fetches data from BigQuery, and visualizes the result with charts — along with descriptive insights.

The app utilizes Google Generative AI (Gemini) to generate SQL queries, processes the data using BigQuery, and visualizes the results using Altair charts.

## Prerequisites
- **Python 3.11.7** or above
- **pip** (Python package manager)
- **Gemini 2.0 Flash** API Key for generating SQL queries and natural responses.
- **BigQuery** as the database to fetch data.
- **Google Generative AI** For creating vector embeddings
## ✨Technology
- **LangGraph** for designing the conversation and logic flow.
- **LangChain** Framework for building AI-powered applications.
- **Altair** for dynamic data visualization.
- **Streamlit** for creating the front-end app.

## LangGraph

- LangGraph — is a low-level orchestration framework for building controllable agents. While langchain provides integrations and composable components to streamline LLM application development, the LangGraph library enables agent orchestration — offering customizable architectures, long-term memory, and human-in-the-loop to reliably handle complex tasks. To learn more about langgraph, visit the [GitHub repository](https://github.com/langchain-ai/langgraph).

![Alt text](URL or path to the image)

## Streamlit
- Streamlit is an open-source app framework that allows you to create interactive and data-driven web applications in Python quickly. In this project, Streamlit was used to build a user-friendly interface that allows for easy interaction with the Cooking Assistant Agent [documentation](https://docs.streamlit.io/).

![Alt text](https://github.com/MZeeshanAnjum/AI_Data_Analyst/blob/main/front_page.PNG)


---

## 🚀 Features

- ✏️ Auto-generates SQL queries based on user input.
- 🔄 Intelligent fallback mechanism when SQL generation fails.
- 🛢️ Executes live queries on BigQuery.
- 📊 Generates Altair charts dynamically.
- 🖥️ Streamlit web app for user interaction.
- 🤖 Summarizes data and provides textual insights along with plots.

## 🛠️ Installation Guide



## 🏗️ Use Cases
-  User can querry about the data in its database and can get valuable insights
![Alt text](URL or path to the image)

- If the prompt is not according to the schema of database it can also acknowledge that
![Alt text](URL or path to the image)

---


## ⚙️ How It Works

1. **User Input**: User types a query (example: "Total number of students in each department with GPA > 3").
2. **LangGraph Flow**:
   - **Node 1 (chatbot1)**: Attempts SQL generation using Gemini LLM.
   - **Conditional Check**:
     - If SQL generation fails → fallback to a conversational response (Node: chatbot2).
     - If SQL generation succeeds → execute the SQL (Node: chatbot3).
3. **Data Handling**:
   - Fetches data from BigQuery.
   - Summarizes key findings.
   - Creates an Altair chart.
4. **Display**:
   - Streamlit shows both the chart and the insights to the user.

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/lang_graph.git
   cd your-project
2. **Create and activate virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use venv\Scripts\activate`
3. **Install requirements.txt**
    ```bash
    pip install -r requirements.txt
4. **Set up environment variables**
Create a .env file and configure the following:
- GCP_SERVICE_ACCOUNT_JSON_KEY_PATH=
- DATASET_ID=
- PROJECT_ID=
- GOOGLE_GEMINI_API_KEY=
5. Run the Application
    ```bash
    streamlit run app.py


## 🏗️ Project Structure

| File/Folder | Purpose |
|:---|:---|
| `app.py` | Main LangGraph and Streamlit app logic |
| `components.py` | Helper functions for BigQuery connection and vector store |
| `data_handler.py` | Handles DataFrame summarization and chart generation |
| `prompts.py` | System prompts and templates for LLM |
| `embeddings.py` | To create embeddings of your database schema  |
| `requirements.txt` | Python dependencies |

---
 
## 📊 Usage Guide

- Enter a natural language query, e.g., "Show me the total sales for Q1 2024."

- Submit the query to generate an SQL statement.

- View results as an interactive table and chart.

![Alt text](https://github.com/MZeeshanAnjum/AI_Data_Analyst/blob/main/usecase1.PNG)

** fallback**
- When user enters a prompt that can't be used to create and SQL according to the database schema.
![Alt text](https://github.com/MZeeshanAnjum/AI_Data_Analyst/blob/main/Usecase2.PNG)
