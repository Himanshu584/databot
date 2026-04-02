import streamlit as st
import pandas as pd
import plotly.express as px
from utils import read_file, get_dataframe_info
from llm import configure_gemini, ask_gemini, extract_code

# ---- Page Configuration ----
st.set_page_config(
    page_title="DataBot",
    page_icon="🤖",
    layout="wide"
)

# ---- Initialize Gemini ----
@st.cache_resource
def load_model():
    return configure_gemini()

try:
    model = load_model()
except Exception as e:
    st.error(f"⚠️ Gemini API Error: {str(e)}")
    st.stop()

# ---- App Title ----
st.title("🤖 Data Analysis ChatBot")
st.subheader("Upload your dataset and ask anything about it!")

# ---- File Upload ----
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    # Read the file
    df, error = read_file(uploaded_file)
    
    if error:
        st.error(error)
        st.stop()
    
    # Show success message and dataset preview
    st.success(f"✅ File uploaded successfully! {df.shape[0]} rows and {df.shape[1]} columns")
    
    with st.expander("👀 Preview your dataset"):
        st.dataframe(df)
    
    with st.expander("📊 Dataset Statistics"):
        st.write(df.describe())
    
    # ---- Chat Section ----
    st.divider()
    st.subheader("💬 Ask anything about your data")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "chart" in message and message["chart"] is not None:
                st.plotly_chart(message["chart"], use_container_width=True)
    
    # User input
    question = st.chat_input("Ask a question about your data...")
    
    if question:
        # Show user message
        with st.chat_message("user"):
            st.write(question)
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Get Gemini response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                dataframe_info = get_dataframe_info(df)
                response = ask_gemini(model, question, dataframe_info)
                code = extract_code(response)
                
                # Clean response text - remove code block from display
                display_text = response
                if code:
                    import re
                    display_text = re.sub(r"```python.*?```", "", response, flags=re.DOTALL).strip()
                
                st.write(display_text)
                
                # Execute chart code if present
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
    st.info("👆 Please upload a CSV or Excel file to get started!")