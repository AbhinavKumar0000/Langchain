# Langchain Learning & RAGTube Project

This repository documents my journey learning LangChain and its core concepts, culminating in a full-stack web application called **RAGTube**.

The primary application, **RAGTube**, allows you to have a conversation with any YouTube video. You provide a URL, the app fetches and processes its transcript, and you can ask questions to be answered *only* from the video's content.

The other directories (`Chains`, `Data_loader`, `Parsers`, etc.) are my hands-on learning modules based on the reference material.

---

## Featured Project: RAGTube

RAGTube is a sophisticated, full-stack web application that implements a complete Retrieval-Augmented Generation (RAG) pipeline.

* **Purpose**: To let a user have a conversation with a YouTube video.
* **Core Concept**: A user provides a YouTube URL, the application fetches the video's transcript, "learns" it, and then answers the user's questions based exclusively on the information in that video.

### 🛠️ Core Technology Stack

* **Backend**: Python, Flask
* **AI & RAG**: LangChain, Google Gemini (`langchain-google-genai`)
* **Vector Database**: FAISS (in-memory vector store)
* **Data Scraping**: `youtube_transcript_api`, `yt-dlp`
* **Frontend**: HTML, JavaScript, and custom CSS (dark mode, glassmorphism)

### How It Works: The Full Pipeline

The project is split into a frontend (what the user sees) and a backend (how it "thinks").

#### 1. The Frontend (Client-Side)

* **UI**: A minimal, dark-mode chat interface built with HTML, CSS, and JavaScript.
* **State Management**: The frontend `script.js` manages the application's state, tracking if a video is loaded or if it's on the "welcome screen."
* **Event Handling**:
    * **On URL Submit**: Sends the YouTube URL to the `/load_video` backend endpoint.
    * **On Question Submit**: Sends the user's question to the `/ask` backend endpoint.
    * **On Clear**: Calls the `/clear` endpoint and resets the UI.

#### 2. The Backend (Server-Side: `app.py`)

This is the "brain" of the operation, orchestrated by LangChain.

**Part A: Video Loading (Ingestion via `/load_video`)**
1.  **Get URL**: Flask receives the YouTube URL from the frontend.
2.  **Fetch Metadata**: `yt-dlp` is used to extract the video's Title, Channel, and Thumbnail.
3.  **Fetch Transcript**: `youtube_transcript_api` scrapes the full text transcript.
4.  **Chunk Text**: The transcript is split into small, overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`.
5.  **Create Embeddings**: Each text chunk is converted into a vector (a list of numbers) using the Gemini embedding model.
6.  **Index Vectors**: All vectors are loaded into a FAISS vector store, creating a searchable, in-memory database of the video's content.
7.  **Cache**: The FAISS retriever and video metadata are cached in a global variable for quick access.

**Part B: Answering Questions (RAG via `/ask`)**
1.  **Get Question**: Flask receives the user's question (e.g., "What did the speaker say about RAG?").
2.  **Retrieve Context**: The app performs a "semantic search" on the FAISS vector store to find the most relevant chunks from the transcript related to the question.
3.  **Build Prompt**: A special prompt is constructed with strict rules, the retrieved context, and the user's question.
    * **Rule**: "You are a strict assistant... you MUST only use the context... if the answer is not here, say 'I don't know'."
    * **Context**: (The most relevant chunks are pasted here).
    * **Question**: (The user's question is pasted here).
4.  **Generate Answer**: This complete prompt is sent to the Gemini chat model, which generates an answer following the strict rules.
5.  **Send Response**: The AI's answer is sent back to the frontend to be displayed in the chat.

###  Extra Features

* **Glassmorphism UI**: A "Developed by Abhinav Kumar" watermark with a frosted-glass effect.
* **Pop-up Modal**: Clicking the watermark triggers a pop-up window.
* **Animated RAG Diagram**: Inside the modal is a custom, animated, horizontal-scrolling diagram (built with pure HTML/CSS) that visualizes the entire RAG pipeline for this project.

---

## Repository File Contents

This repository is organized into the main project and the individual learning modules.
