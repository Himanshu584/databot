import streamlit as st
import pandas as pd
import plotly.express as px
import re
from utils import read_file, get_dataframe_info
from llm import configure_gemini, ask_gemini, extract_code

# ---- Page Configuration ----
st.set_page_config(
    page_title="DataBot",
    page_icon="🤖",
    layout="wide"
)

# ---- Custom CSS ----
st.markdown("""
    <style>
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        color: #4F8BF9;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #1E1E2E;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Initialize Gemini ----
@st.cache_resource
def load_model():
    return configure_gemini()

try:
    model = load_model()
except Exception as e:
    st.error(f"⚠️ Gemini API Error: {str(e)}")
    st.stop()

# ---- Main Title ----
st.markdown('<H2 class="main-title">🤖 LLM Powered Data Analysis ChatBot</H2>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your dataset and ask anything about it in plain English!</p>', unsafe_allow_html=True)

# ---- File Upload ----
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    df, error = read_file(uploaded_file)

    if error:
        st.error(error)
        st.stop()

    # ---- Sidebar ----
    with st.sidebar:
        st.header("📊 Dataset Info")
        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])
        st.metric("Missing Values", df.isnull().sum().sum())
        
        st.divider()
        st.subheader("🧮 Column Types")
        for col, dtype in df.dtypes.items():
            st.write(f"**{col}** — {dtype}")
        
        st.divider()
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # ---- Dataset Preview ----
    st.success(f"✅ File uploaded! {df.shape[0]} rows × {df.shape[1]} columns")

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("👀 Preview Data"):
            st.dataframe(df, use_container_width=True)
    with col2:
        with st.expander("📈 Statistics"):
            st.dataframe(df.describe(), use_container_width=True)

    # ---- Suggested Questions ----
    st.divider()
    st.subheader("💡 Suggested Questions")
    
    col1, col2, col3 = st.columns(3)
    suggestions = [
        "Show me a summary of this dataset",
        "Which column has the most missing values?",
        "Show me a bar chart of the first column",
    ]
    
    if col1.button(suggestions[0]):
        st.session_state.suggested = suggestions[0]
    if col2.button(suggestions[1]):
        st.session_state.suggested = suggestions[1]
    if col3.button(suggestions[2]):
        st.session_state.suggested = suggestions[2]

    # ---- Chat Section ----
    st.divider()
    st.subheader("💬 Chat with your Data")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "suggested" not in st.session_state:
        st.session_state.suggested = None

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "chart" in message and message["chart"] is not None:
                st.plotly_chart(message["chart"], use_container_width=True)

    # Handle input - either from suggestion or chat input
    question = st.chat_input("Ask a question about your data...")
    
    if st.session_state.suggested:
        question = st.session_state.suggested
        st.session_state.suggested = None

    if question:
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                dataframe_info = get_dataframe_info(df)
                response = ask_gemini(model, question, dataframe_info)
                code = extract_code(response)

                display_text = response
                if code:
                    display_text = re.sub(r"```python.*?```", "", response, flags=re.DOTALL).strip()

                st.write(display_text)

                chart = None
                if code:
                    try:
                        local_vars = {"df": df, "px": px, "pd": pd}
                        exec(code, local_vars)
                        if "fig" in local_vars:
                            chart = local_vars["fig"]
                            st.plotly_chart(chart, use_container_width=True)
                    except Exception as e:
                        st.warning(f"⚠️ Could not generate chart: {str(e)}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": display_text,
                    "chart": chart
                })

else:
    # ---- Landing Page when no file uploaded ----
    st.info("👆 Upload a CSV or Excel file to get started!")
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📁 Upload")
        st.write("Upload any CSV or Excel file — sales data, survey results, financial data, anything!")
    
    with col2:
        st.markdown("### 💬 Ask")
        st.write("Ask questions in plain English — no SQL or coding knowledge needed!")
    
    with col3:
        st.markdown("### 📊 Visualize")
        st.write("Get instant charts, summaries and insights powered by Google Gemini AI!")