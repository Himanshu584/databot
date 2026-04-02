# 🤖 DataBot — AI-Powered Data Analysis Chatbot

DataBot is an AI-powered web application that lets you upload any CSV or Excel dataset and analyze it using plain English questions. No SQL or coding knowledge required!

Built with **Streamlit**, **Google Gemini AI**, **Pandas**, and **Plotly**.

---

## 🚀 Features

- 📁 Upload CSV or Excel files
- 💬 Ask questions about your data in plain English
- 📊 Get instant interactive charts powered by Plotly
- 🧠 AI-powered analysis using Google Gemini
- 📈 Dataset statistics and column info in the sidebar
- 💡 Suggested questions to get started quickly

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Streamlit | Web app framework |
| Google Gemini AI | LLM for natural language understanding |
| Pandas | Data manipulation |
| Plotly | Interactive charts |
| Docker | Containerization |

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Himanshu584/databot.git
cd databot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free API key from: https://aistudio.google.com/apikey

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🐳 How to Run with Docker

### Pull from DockerHub
```bash
docker pull hsharma2002/databot
```

### Run the container
```bash
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key_here hsharma2002/databot
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure
```
databot/
├── app.py              # Main Streamlit application
├── llm.py              # Google Gemini AI integration
├── utils.py            # File reading and data utilities
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .env                # API key (not pushed to GitHub)
└── .gitignore          # Git ignore rules
```

---

## 💡 Example Questions to Ask

- "Show me a summary of this dataset"
- "Which column has the most missing values?"
- "Show me a bar chart of sales by region"
- "What is the average value of each numeric column?"
- "Show me the correlation between columns"

---

## 👨‍💻 Author

**Himanshu Sharma**
- GitHub: [github.com/Himanshu584](https://github.com/Himanshu584)
- LinkedIn: [linkedin.com/in/hsharma98765](https://linkedin.com/in/hsharma98765)
- Medium: [medium.com/@hsharma98765](https://medium.com/@hsharma98765)

---

## ⭐ If you found this useful, give it a star on GitHub!