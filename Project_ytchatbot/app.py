import os
from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from urllib.parse import urlparse, parse_qs
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

os.environ["GOOGLE_API_KEY"] = ""

app = Flask(__name__, template_folder='templates', static_folder='static')

CACHED_RETRIEVER = None
CACHED_VIDEO_INFO = None

try:
    if "GOOGLE_API_KEY" not in os.environ:
        raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")
    
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
except Exception as e:
    print(f"Error initializing Google Generative AI: {e}")
    exit()

ytt_api = YouTubeTranscriptApi()
splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=200)

prompt = PromptTemplate(
    template="""
      You are a strict, factual assistant. Your task is to answer questions based *exclusively* on the provided video transcript context.
      Do not use any external knowledge. Do not make assumptions.
      If the answer is not present in the context, you MUST respond with *only* the text: "I don't know based on the video transcript."
      Do not add any conversational phrases, greetings, or explanations *about* your task.

      Context:
      {context}
      
      Question:
      {question}
    """,
    input_variables=['context', 'question']
)

def convert_transcript_format(ts: list) -> list:
    converted = []
    for snippet in ts:
        converted.append({
            'text': snippet.text,
            'start': snippet.start,
            'duration': snippet.duration
        })
    return converted

def format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def get_video_id(url: str) -> str | None:
    try:
        video_id_regex = r"^[a-zA-Z0-9_-]{11}$"
        
        if re.match(video_id_regex, url):
            return url
            
        parsed_url = urlparse(url)
        
        if parsed_url.hostname and "youtube.com" in parsed_url.hostname:
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get("v", [None])[0]
            if video_id:
                return video_id
            
        elif parsed_url.hostname and "youtu.be" in parsed_url.hostname:
            return parsed_url.path[1:].split("?")[0]
            
        elif parsed_url.path and "/embed/" in parsed_url.path:
            return parsed_url.path.split("/embed/")[1].split("?")[0]

        elif parsed_url.path and "/shorts/" in parsed_url.path:
            return parsed_url.path.split("/shorts/")[1].split("?")[0]
            
    except Exception as e:
        print(f"Error parsing URL: {e}")
    return None

def load_video_data(video_id: str):
    global CACHED_RETRIEVER, CACHED_VIDEO_INFO
    
    print(f"Fetching transcript for video: {video_id}...")
    try:
        ts = ytt_api.fetch(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None, f"Error fetching transcript. Is it a valid video with transcripts enabled? Error: {e}"

    video_info = {
        "title": "Unknown Title",
        "channel": "Unknown Channel",
        "publish_date": "Unknown Date",
        "thumbnail_url": "https://placehold.co/120x90/e2e8f0/64748b?text=No+Preview"
    }
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'forceid': True,
            'forcetitle': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
        
        video_info.update({
            "title": info_dict.get('title', 'Unknown Title'),
            "channel": info_dict.get('uploader', 'Unknown Channel'),
            "publish_date": info_dict.get('upload_date', 'Unknown Date'), 
            "thumbnail_url": info_dict.get('thumbnail', video_info["thumbnail_url"])
        })
        
        if video_info["publish_date"] != "Unknown Date" and len(video_info["publish_date"]) == 8:
            d = video_info["publish_date"]
            video_info["publish_date"] = f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
    except Exception as e:
        print(f"Warning: yt-dlp failed to get video metadata: {e}. Proceeding with transcript only.")

    converted_transcript = convert_transcript_format(ts)
    texts = [item['text'] for item in converted_transcript]
    full_text = " ".join(texts)

    if not full_text:
        return None, "Error: Could not extract any text from the video transcript."

    chunks = splitter.split_text(full_text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"Transcript chunked into {len(documents)} documents.")

    print("Creating in-memory vector store...")
    vector_store = FAISS.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": 5, "fetch_k": 20}
    )

    CACHED_RETRIEVER = retriever
    CACHED_VIDEO_INFO = video_info
    
    print("Video data loaded and cached successfully.")
    return video_info, None

def get_rag_answer(question: str) -> str:
    global CACHED_RETRIEVER
    
    if CACHED_RETRIEVER is None:
        return "Error: No video is loaded. Please provide a YouTube URL first."

    print("Running SIMPLE RAG chain...")
    
    rag_chain = (
        {"context": CACHED_RETRIEVER | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)
    return answer



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_video', methods=['POST'])
def handle_load_video():
    global CACHED_RETRIEVER, CACHED_VIDEO_INFO
    
    data = request.json
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "No video URL provided."}), 400
        
    video_id = get_video_id(video_url)
    
    if not video_id:
        return jsonify({"status": "error", "message": "Invalid YouTube URL."}), 400

    CACHED_RETRIEVER = None
    CACHED_VIDEO_INFO = None
    

    video_info, error = load_video_data(video_id)
    
    if error:
        return jsonify({"status": "error", "message": error}), 500
        
    return jsonify({"status": "success", "video_info": video_info})

@app.route('/ask', methods=['POST'])
def handle_ask_question():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"status": "error", "message": "No question provided."}), 400
        
    if CACHED_RETRIEVER is None:
        return jsonify({"status": "error", "message": "No video loaded."}), 400

    answer = get_rag_answer(question)
    
    return jsonify({"status": "success", "answer": answer})

@app.route('/clear', methods=['POST'])
def handle_clear_video():
    global CACHED_RETRIEVER, CACHED_VIDEO_INFO
    CACHED_RETRIEVER = None
    CACHED_VIDEO_INFO = None
    
    print("Cache cleared.")
    return jsonify({"status": "success", "message": "Video context cleared."})

if __name__ == '__main__':
    app.run(debug=True)