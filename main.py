from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from youtube_transcript_api.proxies import WebshareProxyConfig
import os
import time
import streamlit as st

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")


def extract_video_id(youtube_url):
    """
    Extracts the video ID from a valid YouTube URL.
    """
    if "v=" in youtube_url:
        return youtube_url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[-1].split("?")[0]
    else:
        st.error("Invalid YouTube URL format. Please enter a valid URL.")
        return None
    

def get_transcript(video_id, language):
    """
    Fetches the transcript of the YouTube video using YouTube Transcript API.
    """
    # ytt_api = YouTubeTranscriptApi()
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username="uiwynuio",
            proxy_password="y3tljx1ygjd0",
        )
    )
    try:
        transcript = ytt_api.fetch(video_id, languages=[language])
        time.sleep(40)
        return " ".join([entry.text for entry in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        st.error("Transcript not available for this video. Please check the language or try a different video.")
        return None
    except VideoUnavailable:
        st.error("The video is unavailable. Please check the URL.")
        return None
    except Exception as e:
        st.error(f"An error occurred while fetching the transcript: {e}")
        return None
    
# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)


def translate_transcript_to_english(transcript):
    """
    Translates the transcript to English using LangChain.
    """

    try:
        prompt = ChatPromptTemplate.from_template("""
                                         
        You are an expert translator with deep cultural and linguistic knowledge.
        I will provide you with a transcript. Your task is to translate it into English with absolute accuracy, preserving:
        - Full meaning and context (no omissions, no additions).
        - Tone and style (formal/informal, emotional/neutral as in original).
        - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
        - Speaker's voice (same perspective, no rewriting into third-person).
        Do not summarize or simplify. The translation should read naturally in the target language but stay as close as possible to the original intent.

        Transcript:
        {transcript}

        """)

        # Runable Chain
        chain = prompt|llm

        # Run Chain
        response = chain.invoke({"transcript":transcript})

        return response.content
    except Exception as e:
        st.error(f"An error occurred during translation: {e}")
        return None
    

def get_important_topics(transcript):
    """
    Extracts important topics from the transcript using LangChain.
    """

    try:
        prompt = ChatPromptTemplate.from_template("""
                                         
        You are an assistant that extracts the 5 most important topics discussed in a video transcript or summary.

        Rules:
        - Summarize into exactly 5 major points.
        - Each point should represent a key topic or concept, not small details.
        - Keep wording concise and focused on the technical content.
        - Do not phrase them as questions or opinions.
        - Output should be a numbered list.
        - show only points that are discussed in the transcript.
        
        Here is the transcript:
        {transcript}

        """)

        # Runable Chain
        chain = prompt|llm

        # Run Chain
        response = chain.invoke({"transcript":transcript})

        return response.content
    except Exception as e:
        st.error(f"An error occurred while extracting topics: {e}")
        return None
    
    
def generate_notes(transcript):
    """
    Generates detailed notes from the transcript using LangChain.
    """

    try:
        prompt = ChatPromptTemplate.from_template("""
                                         
        You are an expert note-taker. I will provide you with a transcript of a video. 
        Your task is to create detailed, structured notes that capture all key points and information.

        Rules:
        - Use clear headings and subheadings to organize content.
        - Include bullet points for important details under each heading.
        - Maintain the original meaning and context without adding personal opinions.
        - Ensure notes are concise yet comprehensive, covering all major topics discussed.
        - If the transcript includes multiple themes, organize them under subheadings.
        - Format notes for easy reading and quick reference.
        - Do not add information that is not present in the transcript.

        Transcript:
        {transcript}

        """)

        # Runable Chain
        chain = prompt|llm

        # Run Chain
        response = chain.invoke({"transcript":transcript})

        return response.content
    except Exception as e:
        st.error(f"An error occurred while generating notes: {e}")
        return None


def create_chunks(transcript):
    """
    Splits the transcript into smaller chunks for processing.
    """
    text_splitters = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    doc = text_splitters.create_documents([transcript])
    return doc


def create_vector_store(docs):
    """
    Creates a vector store from the document chunks using HuggingFace embeddings.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(docs, embeddings)
    return vector_store


def rag_answer(question, vectorstore):
    """
    Answers a question based on the context from the vector store.
    """
    results = vectorstore.similarity_search(question, k=4)
    context_text = "\n".join([i.page_content for i in results])

    prompt = ChatPromptTemplate.from_template("""
                You are a kind, polite, and precise assistant.
                - Begin with a warm and respectful greeting (avoid repeating greetings every turn).
                - Understand the user's intent even with typos or grammatical mistakes.
                - Answer ONLY using the retrieved context.
                - If answer not in context, say:
                  "I couldn't find that information in the database. Could you please rephrase or ask something else?"
                - Keep answers clear, concise, and friendly.

                Context:
                {context}

                User Question:
                {question}

                Answer:
                """)

    #chain
    chain = prompt|llm
    response= chain.invoke({"context":context_text,"question":question})

    return response.content
