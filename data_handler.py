"""
# Data Processing and Visualization Module

This module provides functions for refining SQL query responses, executing BigQuery queries,
and handling data processing and visualization based on user queries.
"""

import pandas as pd
import altair as alt
import regex as re

def refine_response(response):
    """
    ### `refine_response(response: str) -> str`
    Cleans and refines SQL query responses by removing markdown artifacts such
    as code block backticks and unnecessary tags.

    **Parameters:**
    - `response (str)`: The raw SQL query response.

    **Returns:**
    - `str`: A cleaned and formatted SQL query string.
    """

    # Remove the 'sql' tag if it exists at the start of the response
    response = re.sub(r"^sql\s*", "", response)
    response = re.sub(r"^```sql(.*)```$", r"\1", response, flags=re.DOTALL)


    # Remove triple backticks or single backticks at both ends
    response = re.sub(r"^```(.*)```$", r"\1", response, flags=re.DOTALL)
    response = re.sub(r"^`(.*)`$", r"\1", response, flags=re.DOTALL)

    # Strip any leading or trailing whitespace
    return response.strip()


def get_data(bq_manager, reg):
    """
    ### `get_data(bq_manager, reg: str) -> pd.DataFrame`
    Executes a SQL query using a BigQuery manager instance and returns
    the results as a Pandas DataFrame.

    **Parameters:**
    - `bq_manager`: An instance of `BigQueryManager` to execute queries.
    - `reg (str)`: The SQL query string to be executed.

    **Returns:**
    - `pd.DataFrame`: Query results in a Pandas DataFrame.
    """

    # Execute the BigQuery query
    data = bq_manager.execute_query(reg)
    return data


def data_handler(data: pd.DataFrame, user_input, llm):
    """
    ### `data_handler(data: pd.DataFrame, user_input: str, llm) -> tuple`
    Processes data and generates a summary or visualization based on the
    user's query using an LLM (Large Language Model).

    **Parameters:**
    - `data (pd.DataFrame)`: The dataset retrieved from BigQuery.
    - `user_input (str)`: The user's query regarding the data.
    - `llm`: The language model instance to analyze and summarize the data.

    **Returns:**
    - `tuple (str, Optional[alt.Chart])`: A tuple containing:
    - A text summary of the data.
    - An Altair chart visualization (or `None` if no visualization is generated).
    """

    data_json = data.to_json(orient="records", lines=False)

    improved_prompt = f"""
    You are an expert data analysis assistant tasked with analyzing the dataset provided in JSON format and summarizing it based on the user's query. Your primary goal is to extract actionable insights and answer data-related questions clearly and concisely. When responding, ensure that you focus on the most relevant details and avoid unnecessary context about the dataset unless directly requested. You should strive to uncover trends, patterns, or interesting observations from the dataset that may be helpful to the user.

### Instructions:
1. **Understand the Context**: The dataset you receive has already been preprocessed to directly align with the user's query, so it contains only the relevant information.
2. **Your Primary Responsibilities**:
   - **Directly address the user's query**: If the query requires a simple answer (e.g., a count or list), provide that answer directly.
   - **Provide Insights and Trends**: Try to give any insignts about the data,but do give a summary of the data with key trends and insights. Look for any interesting patterns, such as averages, maximum or minimum values, and relationships between different variables.
   - **Create Visualizations**: If the user requests a graph or visualization, choose the most appropriate type (e.g., bar chart, line graph, pie chart) to represent the data clearly. Provide the code for generating the visualization.
   - **Acknowledge Limitations**: If the dataset doesn't contain enough information to fully answer the user's query, mention this limitation and suggest possible modifications to the query for more complete results.
3. **Response Structure**:
   - For **simple queries**: Directly provide the answer (e.g., the list of students, the total count, etc.).
   - For **insight-based queries**: Offer a summary of the data with key trends and insights. Look for any interesting patterns, such as averages, maximum or minimum values, and relationships between different variables.
   - For **graphical queries**: Generate a graph to illustrate the data and provide the corresponding code.

4. **Important Guidelines**:
   - Focus on **clarity** and **conciseness** in your responses.
   - Avoid **technical jargon** or explanations of dataset preprocessing unless the user explicitly asks.
   - Ensure that visualizations are informative, clean, and easy to understand.
The dataset is in JSON format:
{data_json} Please summarize the data accordingly. and the user query is: {user_input}.

### Python Code for Visualization:
```python
import pandas as pd
import altair as alt

# Create a DataFrame with the provided data
data = {{
    'Department': ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering'],
    'Average CGPA': [3.44, 3.32, 3.68]
}}
df = pd.DataFrame(data)

# Create a bar chart
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Department', axis=alt.Axis(title='Department')),
    y=alt.Y('Average CGPA', axis=alt.Axis(title='Average CGPA')),
    tooltip=['Department', 'Average CGPA']
).properties(
    title='Average CGPA by Department'
)
"""
    
    
    # print(f"Improved Prompt:{improved_prompt}")
    result = llm.invoke(improved_prompt)
    response_text = result.content.strip()

    # Extract Python code if present
    code_pattern = r"```python(.*?)```"
    png_pattern = r"\b\w+\.png\b"
    html_pattern = r"\b\w+\.html\b"
    code_match = re.search(code_pattern, response_text, re.DOTALL)

    chart = None
    if code_match:
        try:
            # Get the code and execute it
            code = code_match.group(1).strip()
            local_vars = {"pd": pd, "alt": alt, "data": data}
            exec(code, local_vars)

            if "chart" in local_vars:
                chart = local_vars["chart"]

            response_text = re.sub(
                code_pattern, "", response_text, flags=re.DOTALL
            ).strip()
            response_text = re.sub(png_pattern, "", response_text).strip()
            response_text = re.sub(html_pattern, "", response_text).strip()

        except Exception as e:
            response_text += f"\nError generating visualization: {str(e)}"

    return response_text, chart
