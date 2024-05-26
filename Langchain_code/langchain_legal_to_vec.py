import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import PyPDF2
from langchain.docstore.document import Document
import re


os.environ["OPENAI_API_KEY"] = "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"


# 加载PDF文件
def load_pdf(pdf_file):
    pdf_file = open('../data/组合文件.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[num]
        text += page.extract_text()
    return text


# 自定义句子分段的方式，保证句子不被截断
def split_paragraph(text, pdf_name, max_length=300):
    text = text.replace('\n', '')
    text = text.replace('\n\n', '')
    text = re.sub(r'\s+', ' ', text)
    """
    将文章分段
    """
    # 首先按照句子分割文章
    sentences = re.split('(；|。|！|\!|\.|？|\?)', text)

    new_sents = []
    for i in range(int(len(sentences) / 2)):
        sent = sentences[2 * i] + sentences[2 * i + 1]
        new_sents.append(sent)
    if len(sentences) % 2 == 1:
        new_sents.append(sentences[len(sentences) - 1])

    # 按照要求分段
    paragraphs = []
    current_length = 0
    current_paragraph = ""
    for sentence in new_sents:
        sentence_length = len(sentence)
        if current_length + sentence_length <= max_length:
            current_paragraph += sentence
            current_length += sentence_length
        else:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence
            current_length = sentence_length
    paragraphs.append(current_paragraph.strip())
    documents = []
    metadata = {"source": pdf_name}
    for paragraph in paragraphs:
        new_doc = Document(page_content=paragraph, metadata=metadata)
        documents.append(new_doc)
    return documents


# 持久化向量数据
def persist_embedding(documents):
    # 将embedding数据持久化到本地磁盘
    persist_directory = 'db'
    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory)
    vectordb.persist()
    vectordb = None


if __name__ == "__main__":
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    # embdding 并且持久化
    pdf_name = "../data/组合文件.pdf"
    content = load_pdf(pdf_name)
    documents = split_paragraph(content, pdf_name)
    persist_embedding(documents)