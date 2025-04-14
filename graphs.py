import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent
from langchain_experimental.tools import PythonREPLTool
from langchain.agents.agent_types import AgentType
import tempfile
import os
import re
import glob

def graph_generator(df):
    # Save DataFrame to CSV to load via PythonREPLTool
  

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        csv_path = tmp.name
        df.to_csv(csv_path, index=False)

    # Init Groq LLM
    llm = ChatGroq(
        temperature=0.2,
        model_name="mistral-saba-24b",
        groq_api_key="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"
    )

    
    tools = [PythonREPLTool()]
    custom_prompt = """
    You are a smart AI agent. If you encounter Python code, you must execute it using the Python tool provided.
    Only use tools if required to solve the user's request. 
    """
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True,
        agent_kwargs={
        "system_message": custom_prompt
         }
    )
    column_info = "\n".join([f"{col} ({dtype})" for col, dtype in df.dtypes.items()])
    prompt = f"""
You are a data visualization assistant.

The dataset is stored in a file named '{csv_path}'.
Here are the column names and data types:
{column_info}

1. Load it using pandas.
2. Generate 2 or 3 meaningful and relevant plots using matplotlib or seaborn.
3. Save each plot using `plt.savefig()` as 'chart1.png', 'chart2.png', etc.
4. Do not show the plots or add explanations. Just save them.

Only return valid Python code.
"""

    output = agent.run(prompt)

    images = []
    for i in range(1, 4):
        path = f"chart{i}.png"
        if os.path.exists(path):
            images.append(path)

    return images

    # class CustomPythonREPLTool(PythonREPLTool):
    #     def __init__(self, df, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self._df = df

    #     def _clean_code(self, code: str) -> str:
    #         # Remove ```python or ``` from start/end
    #         code = re.sub(r"^```(?:python)?\s*", "", code.strip())
    #         code = re.sub(r"\s*```$", "", code)
    #         return code

    #     def _run(self, command: str) -> str:
    #         command = self._clean_code(command)  # Clean LLM-generated markdown
    #         local_env = {"df": self._df}
    #         try:
    #             exec(command, {}, local_env)
    #             return "Chart generated successfully."
    #         except Exception as e:
    #             return f"Error running the code: {e}"


#     # Initialize the custom tool with your dataset
#     tools = CustomPythonREPLTool(df=df)
#     agent = initialize_agent(
#         tools=[tools],
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         handle_parsing_errors=True,
#         verbose=True,
#     )

#     prompt = f"""
# You are a data visualization assistant.

# The DataFrame 'df' is already loaded.

# 1. Load it using pandas.
# 2. Generate 2 or 3 meaningful and relevant plots using matplotlib or seaborn.
# 3. Save each plot using `plt.savefig()` as 'chart1.png', 'chart2.png', etc.
# 4. Do not show the plots or add explanations. Just save them.
# Only return valid Python code.

# """

#     output = agent.run(prompt)

#     images = []
#     for i in range(1, 4):
#         path = f"chart{i}.png"
#         if os.path.exists(path):
#             images.append(path)

#     return images
