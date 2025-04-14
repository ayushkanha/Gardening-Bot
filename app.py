import streamlit as st
import re
import requests
import data
import os
import pandas as pd
import io
import glob

from langchain.agents import Tool
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from websraper import ws
from mailsender import send_email,create_event
from voice import text_to_speech,transcribe
from graphs import graph_generator 
# venv\Scripts\activate
# ---------------------------------------------------------------------------------------------------------------------------------
groq_key = st.secrets["Groq_API_KEY"]
WETHER_API_KEY = st.secrets["WETHER_API_KEY"]
# LLM
llama = ChatGroq(
        temperature=0.2,
        model_name="mistral-saba-24b",
        groq_api_key="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"
    )

# ---------------------------------------------------------------------------------------------------------------------------------

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
            You are a helpful gardening assistant. 
            Use ONLY the relevant information from the following context to answer the user's question.
            If the answer is not in the context, say "I don't know".

            Context:
            {context}

            Question: {question}
            Answer:
            """
)

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = RetrievalQA.from_chain_type(
        llm=llama,  # your Llama 3.2 model instance
        retriever=data.vector_store,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )
# ---------------------------------------------------------------------------------------------------------------------------------

# ✅ Define your query function
def rag_tool_func(query: str) -> str:
    output = st.session_state.rag_chain({"query": query})
    return output["result"]
# Define tools
def summarize_text(text):
    return llama.predict(f"summerise this:{text}")

def answer_question(question):
    search = DuckDuckGoSearchRun()
    return search.invoke(question)
    

def get_weather(city: str):
    # Use your preferred weather API
    url = f"https://api.weatherapi.com/v1/current.json?key={WETHER_API_KEY}&q={city}"
    response = requests.get(url)
    data = response.json()
    return f"The current temperature in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}. and editional information are:{data}"
def graph_gen(query: str) -> str:
    return "i will genetarate your Graphs for you enter your data in left side uploading option."
# def graph_gen1():
#     st.sidebar.subheader("📊 Upload Data for Visualization")
#     uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel", type=["csv", "xlsx"])

#     if uploaded_file and st.sidebar.button("Generate Charts", key="generate_button"):
#         if uploaded_file.name.endswith(".csv"):
#             df = pd.read_csv(uploaded_file)
#         else:
#             df = pd.read_excel(uploaded_file)

#         st.session_state["uploaded_data"] = df
#         st.session_state["generate_charts"] = True
#     else:
#         st.session_state["generate_charts"] = False

#     if st.session_state.get("generate_charts"):
#         if "uploaded_data" in st.session_state:
#             chart_paths = graph_generator(st.session_state["uploaded_data"])
#             if not chart_paths:
#                 st.write("No charts were generated.")
#             else:
#                 for path in chart_paths:
#                     st.image(path, caption=path)
#                     st.session_state.chat_history.append({"role": "assistant", "content": st.image(path, caption=path)})
#             # Optionally reset the state after generation
#             # st.session_state["generate_charts"] = False
#             # del st.session_state["uploaded_data"]
#         else:
#             st.warning("Please upload data first.")
  
def send_email_input_string(input_string: str):
    try:
        # Regex for each part with non-greedy matching
        to_match = re.search(r"to:\s*(.*?)(?=, subject:|$)", input_string, re.IGNORECASE)
        subject_match = re.search(r"subject:\s*(.*?)(?=, message:|$)", input_string, re.IGNORECASE)
        message_match = re.search(r"message:\s*(.*)", input_string, re.IGNORECASE | re.DOTALL)

        to = to_match.group(1).strip() if to_match else None
        subject = subject_match.group(1).strip() if subject_match else None
        message = message_match.group(1).strip() if message_match else None

        if to and subject and message:
            return send_email(to, subject, message)
        else:
            return "Error: Missing to, subject, or message."
    except Exception as e:
        return f"Error parsing input: {str(e)}"
def schedule_meeting_input_string(input_string: str):
    """
    Example input_string:
    'title: Gardening Talk, description: Discuss soil health, start_time: 2025-04-10T15:30:00, duration: 45'
    """
    try:
        parts = input_string.split(",")
        title = parts[0].split("title:")[1].strip()
        description = parts[1].split("description:")[1].strip()
        start_time = parts[2].split("start_time:")[1].strip()
        duration = int(parts[3].split("duration:")[1].strip())
        return create_event(title, description, start_time, duration)
    except Exception as e:
        return f"Error parsing meeting input: {str(e)}"


# ---------------------------------------------------------------------------------------------------------------------------------
WebScraper_tool = Tool(
    name="WebScraperTool",
    func=ws,
    description="Use this tool when the user wants to buy or know the price of a product. It scrapes Google Shopping and returns a list of product names, prices, and buy links that can be shared with the user."
)

weather_tool = Tool(
    name="WeatherFetcher",
    func=get_weather,
    description="Fetches current weather information for a given city."
)
summarization_tool = Tool(
    name="SummarizationTool",
    func=summarize_text,
    description="Summarizes long texts into concise points."
)

rag_tool = Tool(
    name="RAGTool",
    func=rag_tool_func,
    description="Use this tool to answer gardening questions using expert documents."
)
question_tool = Tool(
    name="QA_Tool",
    func=answer_question,
    description="Answers gardening questions if not present in rag_tool."
)
graph_gen_tool = Tool(
    name="GraphGenerator",
    func=graph_gen,
    description="If user want to generate Graphs or visulization from them there files.And return output asitis to user"
)

email_tool = Tool(
    name="EmailSender",
    func=send_email_input_string,
    description="Send an email. Format: 'to: <email>, subject: <subject>, message: <message>'."
)


meeting_tool = Tool(
    name="MeetingScheduler",
    func=schedule_meeting_input_string,
    description=(
        "Schedules a gardening meeting. Input format: "
        "'title: Gardening Talk, description: Discuss soil health, start_time: 2025-04-10T15:30:00, duration: 45'"
    )
)

tools = [summarization_tool,WebScraper_tool, question_tool,rag_tool,weather_tool ,email_tool,meeting_tool,graph_gen_tool]

# ---------------------------------------------------------------------------------------------------------------------------------

# UI
st.set_page_config(page_title="Gardening Assistant")
st.title("☘ Gardening Assistant")



if "agent" not in st.session_state:
    def build_system_message(user_name, user_city):
        return f"""
        You are a personal Gardening Assistant for {user_name} from {user_city}.
        Help {user_name} with gardening advice, plant care, pest control, composting, and related queries tailored to {user_city}'s climate.
        Be friendly, concise, and informative.

        If RAGTool says "I don't know", use QA_Tool.

        When using EmailSender:
        - Extract and pass parameters as:
            {{
                "to": "recipient@example.com",
                "subject": "Short subject here",
                "message": "Full message here"
            }}

        For example, if user says: "Send an email to rohan.grow@gmail.com reminding him about pest control this weekend", 
        you should call the tool like:
            {{
                "to": "rohan.grow@gmail.com",
                "subject": "Reminder about pest control",
                "message": "Just a reminder about pest control this weekend. Let me know if you have questions."
            }}
        """

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(
        tools=tools,
        llm=llama,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        agent_kwargs={"system_message":build_system_message(user_name="Ayush", user_city="Bhilai")}
    )

    st.session_state.agent = agent
    st.session_state.chat_history = []

users = ["ayushkanha", "kanha"]
passwords = ["ayush", "1234"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.subheader("Login Page")
    user = st.text_input("Enter Username:")
    password = st.text_input("Enter your Password:", type="password")

    if st.button("Login"):
        if user in users:
            if password == passwords[users.index(user)]:
                st.success("Login successful")
                st.session_state.logged_in = True
            else:
                st.error("Incorrect password")
        else:
            st.error("Incorrect username")

if not st.session_state.logged_in:
    login()
else:
    # --- Display chat history ---
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "image":
                st.image(msg["content"], caption=msg["content"])
            else:
                st.markdown(msg["content"])


    user_select= st.sidebar.selectbox(
        "How would you like to Communticate?",
        ("Text", "Voice")
    )
    st.sidebar.subheader("📊 Upload Data for Visualization")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file and st.sidebar.button("Generate Charts", key="generate_button"):
        [os.remove(f) for f in glob.glob("charts/*")]
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state["uploaded_data"] = df.head(30)
        st.session_state["generate_charts"] = True
    else:
        st.session_state["generate_charts"] = False

    if st.session_state.get("generate_charts"):
        if "uploaded_data" in st.session_state:
            chart_paths = graph_generator(st.session_state["uploaded_data"])
            if not chart_paths:
                st.write("No charts were generated.")
            else:
                for path in chart_paths:
                    st.image(path, caption=path)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": path})
            
        else:
            st.warning("Please upload data first.")
    
    if user_select == "Text":
        # --- User input handling ---
        user_input = st.chat_input("Ask something to the agent...")

        if user_input:
            # Show user message
            st.chat_message("user").markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Run agent
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.agent.run(user_input)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    if response.strip():
                            audio_file = text_to_speech(response)
                            st.sidebar.audio(audio_file, format='audio/mp3', autoplay=True)
                    if re.search(r"generate", response, re.IGNORECASE) and re.search(r"graph(s)?", response, re.IGNORECASE):
                       pass
    else: 
        uploaded_file = st.sidebar.audio_input("Record a Voice Message")
        if uploaded_file and st.sidebar.button('Enter'):
            user_input = transcribe(uploaded_file)
            if user_input:
                # Show user message
                st.chat_message("user").markdown(user_input)
                st.session_state.chat_history.append({"role": "user", "content": user_input})

                # Run agent
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.session_state.agent.run(user_input)
                        if response.strip():
                            audio_file = text_to_speech(response)
                            st.sidebar.audio(audio_file, format='audio/mp3', autoplay=True)
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
