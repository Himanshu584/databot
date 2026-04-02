import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def configure_gemini():
    """
    Configures the Gemini API with the API key from .env file
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def ask_gemini(model, question, dataframe_info):
    """
    Sends the user's question + dataset summary to Gemini
    and returns the response.
    """
    prompt = f"""
You are an expert data analyst. A user has uploaded a dataset and wants to analyze it.

Here is the dataset information:
{dataframe_info}

The user asked: {question}

Your job is to:
1. Answer the question clearly in simple English
2. If the question requires a chart or visualization, write Python code using Plotly to create it
3. If you write code, wrap it inside ```python and ``` tags so it can be extracted and executed
4. If you write code, make sure it uses a variable called 'df' for the dataframe
5. Only write code if a visualization genuinely helps answer the question
6. Keep your explanation concise and easy to understand

Important: Do not import pandas in your code, df is already available.
"""
    response = model.generate_content(prompt)
    return response.text


def extract_code(response_text):
    """
    Extracts Python code from Gemini's response if it exists.
    """
    import re
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, response_text, re.DOTALL)
    if matches:
        return matches[0].strip()
    return None