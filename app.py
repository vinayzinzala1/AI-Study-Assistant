import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Study Assistant")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    question = st.text_input("Ask a question from the PDF")

    if question:
        prompt = f"""
        Use this PDF content to answer the question:

        {text[:4000]}

        Question:
        {question}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)
