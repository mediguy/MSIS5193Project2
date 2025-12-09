
# %pip install streamlit langchain-ollama pymupdf pdfminer.six python-docx docx2txt beautifulsoup4
import streamlit as st
import fitz  # PyMuPDF
import docx2txt
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma3:latest",
    temperature=0.1
    )


def extract_text(file):
    # TXT
    if file.name.endswith('.txt'):
        content = file.read().decode('utf-8')
        return content

    # PDF
    elif file.name.endswith('.pdf'):
        with open('tempfile.pdf', 'wb') as f:
            f.write(file.read())
        doc = fitz.open('tempfile.pdf')
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    # Word DOCX
    elif file.name.endswith('.docx'):
        with open('tempfile.docx', 'wb') as f:
            f.write(file.read())
        return docx2txt.process('tempfile.docx')

    # HTML
    elif file.name.endswith(('.htm', '.html')):
        content = file.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    else:
        return None

st.title('Document-Q&A with Ollama LLM')

question = st.text_input('Enter your question:')
uploaded_file = st.file_uploader('Upload a document (plain text, PDF, Word, or HTML, optional):',
                                 type=['txt', 'pdf', 'docx', 'doc', 'htm', 'html'])

context_text = ''
if uploaded_file is not None:
    context_text = extract_text(uploaded_file)
    if not context_text:
        st.error('Unable to extract text from the uploaded file!')

if st.button("Get Answer"):
    prompt = f"Context:\n{context_text}\n\nQuestion: {question}" if context_text else question
    answer = llm.invoke(prompt)
    st.write("Answer:", answer.content)

