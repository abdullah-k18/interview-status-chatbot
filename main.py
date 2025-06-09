import os
import pandas as pd
from groq import Groq
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

# Setup environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
sheet_url = os.getenv("SHEET_URL") or "https://docs.google.com/spreadsheets/d/1-NcmknFNSDg2S7o6Pn4-oMw3EWL6gZGbShcb1QDNEeM/export?format=csv"

# Load embeddings and Pinecone
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
pc = Pinecone(api_key=pinecone_api_key)

# Define index_name and namespace for pinecone
index_name = "interview-updates"
namespace = "embeds"

# Create new index if not created already
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

pinecone_index = pc.Index(index_name)

try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    print(f"⚠️ Failed to load from URL: {e}")

documents = []
for _, row in df.iterrows():
    content = (
        f"Name: {row['Name']}\n"
        f"Position: {row['Position']}\n"
        f"Application Date: {row['Application Date']}\n"
        f"Application Status: {row['Application Status']}\n"
        f"Interview Status: {row['Interview Status']}\n"
        f"Interview Date: {row['Interview Date']}\n"
        f"Interview Time: {row['Interview Time']}\n"
        f"Interview Mode: {row['Interview Mode']}\n"
        f"Interview Address: {row['Address']}"
    )
    documents.append(
        Document(
            page_content=content,
            metadata={
                "name": row["Name"],
                "position": row["Position"],
                "text": content
            }
        )
    )

vectorstore = PineconeVectorStore.from_documents(
    documents,
    embedding=hf_embeddings,
    index_name=index_name,
    namespace=namespace
)

# System prompt
system_prompt = """
You are a professional HR assistant responsible for communicating interview updates to job applicants. 

Your goal is to generate a clear, polite, and professional message based only on the applicant's data provided in the prompt.

⚠️ Important:
- Never mention or reveal details about any other applicant.
- If the applicant's name or role is not found, reply with a professional message like: 
  "We could not find any information related to your application at this time. If you believe this is a mistake, please contact our HR department for assistance."


Avoid email headers like "Re:" and do not include placeholder names like [Your HR Representative].

Include only the following if available:
- Applicant Name
- Position Applied For
- Application Date
- Application Status
- Interview Status
- Interview Date
- Interview Time
- Interview Mode (Online or On-site)
- Interview Address (Zoom/Google Meet link if online, full address if on-site)

Instructions:
1. If the interview status is "*not selected*", write a respectful rejection message mentioning the applicant’s name and position, and wish them good luck.
2. If the interview is *scheduled*, write a formal, polite message confirming the interview and include all available interview details (mode, time, date, address/link).
3. Do not fabricate or assume missing data.
4. Do not include email headers like "Re:" or sign off with generic placeholders like "[Your HR Representative]".
5. End the message with a polite and professional sign-off such as:
    - Best regards.
    - Wishing you the best of luck.
    - Looking forward to meeting you.

Maintain a warm, respectful tone throughout.
"""

groq = Groq(api_key=groq_api_key)

def perform_rag(query):
    query_embedding = hf_embeddings.embed_query(query)
    top_matches = pinecone_index.query(
        vector=query_embedding,
        top_k=10,
        include_metadata=True,
        namespace=namespace
    )
    contexts = [match["metadata"].get("text", "") for match in top_matches["matches"]]
    augmented_query = (
        "\n" + "\n\n-------\n\n".join(contexts[:10]) + "\n-------\n\n\n\n\nMY QUESTION:\n" + query
    )

    res = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": augmented_query}
        ]
    )
    return res.choices[0].message.content


# Chainlit handler
@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content="Processing your query...").send()
    try:
        result = perform_rag(message.content)
        await cl.Message(content=result).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {e}").send()

@cl.on_chat_start
async def startup():
    welcome_msg = (
        "Welcome! 👋\n"
        "Get your job application status and interview details by entering your name and the job role you applied for."
    )
    await cl.Message(content=welcome_msg).send()