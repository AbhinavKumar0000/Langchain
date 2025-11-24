# RAGTube - Chat with YouTube Videos

RAGTube is a sophisticated, full-stack web application that implements a complete Retrieval-Augmented Generation (RAG) pipeline, allowing you to have conversations with YouTube videos.

##  Purpose

Have a conversation with any YouTube video. Provide a URL, the app fetches and processes its transcript, and you can ask questions to be answered *only* from the video's content.

##  Technology Stack

* **Backend**: Python, Flask
* **AI & RAG**: LangChain, Google Gemini (`langchain-google-genai`)
* **Vector Database**: FAISS (in-memory vector store)
* **Data Scraping**: `youtube_transcript_api`, `yt-dlp`
* **Frontend**: HTML, JavaScript, and custom CSS (dark mode, glassmorphism)

##  How It Works: The Full Pipeline

### Frontend (Client-Side)

* **UI**: Minimal, dark-mode chat interface built with HTML, CSS, and JavaScript
* **State Management**: Tracks video loading status and application state
* **Event Handling**:
  * **URL Submit**: Sends YouTube URL to `/load_video` endpoint
  * **Question Submit**: Sends user questions to `/ask` endpoint
  * **Clear**: Calls `/clear` endpoint and resets UI

### Backend (Server-Side: `app.py`)

#### Part A: Video Loading (Ingestion via `/load_video`)
1. **Get URL**: Receives YouTube URL from frontend
2. **Fetch Metadata**: Uses `yt-dlp` to extract video Title, Channel, and Thumbnail
3. **Fetch Transcript**: Scrapes full text transcript using `youtube_transcript_api`
4. **Chunk Text**: Splits transcript into overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`
5. **Create Embeddings**: Converts text chunks into vectors using Gemini embedding model
6. **Index Vectors**: Loads vectors into FAISS vector store for semantic search
7. **Cache**: Stores FAISS retriever and video metadata for quick access

#### Part B: Answering Questions (RAG via `/ask`)
1. **Get Question**: Receives user's question
2. **Retrieve Context**: Performs semantic search on FAISS to find relevant transcript chunks
3. **Build Prompt**: Constructs prompt with strict rules, retrieved context, and user question
4. **Generate Answer**: Sends complete prompt to Gemini chat model for answer generation
5. **Send Response**: Returns AI's answer to frontend for display

##  Features

* **Glassmorphism UI**: Frosted-glass effect watermark
* **Pop-up Modal**: Interactive information window
* **Animated RAG Diagram**: Custom, animated horizontal-scrolling visualization of the RAG pipeline
* **Strict Context Enforcement**: AI only answers from video content, refuses external knowledge

##  UI/UX Highlights

* Dark mode interface
* Responsive design
* Real-time chat experience
* Visual feedback for loading states
* Clean, modern aesthetic with glassmorphism effects

---

*Developed by Abhinav Kumar*
