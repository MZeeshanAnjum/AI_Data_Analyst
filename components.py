from langchain_chroma import Chroma
from big_query_manager import BigQueryManager
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SYSTEM_PROMPT

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=gemini_api_key,
    task_type="retrieval_document",
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=r"D:\DataRopes\Big_Querry_project_1\lang_graph\chroma_langchain_db",
)



def initialize_components():
    # Load environment variables
    load_dotenv()

    # BigQuery configuration
    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("DATASET_ID")
    bq_manager = BigQueryManager(project_id=project_id, dataset_id=dataset_id)
    return bq_manager
    
    
def generate_initial_response(user_input, llm, vector_store, k=3):
    """- Generates an initial response from the LLM based on the user's
    input and schema context retrieved from a Chroma vector store.
    - Retrieves relevant schema information using similarity search
    and constructs a response.
    - Returns either an SQL query or an appropriate response message."""
    try:
        results = vector_store.similarity_search(user_input, k=k)
        # print("Result from croma db ")
        flattened_context = [item.page_content for item in results]
        context = "\n".join(flattened_context)
        system_message = SystemMessage(
            content=f"{SYSTEM_PROMPT}\nSchema Context:\n{context}"
        )
        human_message = HumanMessage(content=user_input)
        # print("Sending to LLM")
        response = llm.invoke([system_message, human_message])
        # print(response)
        return response.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return (
            "An error occurred while processing your request. Please try again later."
        )
