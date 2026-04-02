import pandas as pd

def read_file(uploaded_file):
    """
    Reads uploaded CSV or Excel file and returns a pandas DataFrame.
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file type. Please upload a CSV or Excel file."
        
        return df, None
    
    except Exception as e:
        return None, f"Error reading file: {str(e)}"


def get_dataframe_info(df):
    """
    Returns a summary of the dataframe to send to Gemini
    so it understands what data it's working with.
    """
    info = f"""
Dataset Shape: {df.shape[0]} rows and {df.shape[1]} columns

Column Names and Data Types:
{df.dtypes.to_string()}

First 5 rows of data:
{df.head().to_string()}

Basic Statistics:
{df.describe().to_string()}
    """
    return info