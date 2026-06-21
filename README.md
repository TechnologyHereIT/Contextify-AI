# 🧠 Contextify AI - Agentic Research Workspace

**Contextify AI** is an advanced, next-generation Multi-Document Context Engine and Interactive Mindmap Assistant built during the **Build with AI Saudi Arabia 2026** workshop (#Googleantigravity). 

The platform transforms dense academic research papers, markdown notes, and text files into structured visual knowledge graphs while providing a strict, context-enforced RAG (Retrieval-Augmented Generation) chat interface powered by **Google Gemini 2.5 Flash**.

## ✨ Key Features

- **Three-Panel Professional Layout**: Streamlined workspace separating control, visual analysis, and interactive chat.
- **Native PDF Viewport**: Direct inline base64 PDF rendering for seamless paper reading.
- **Neural Concept Mapping**: Instantly structures raw text semantics into a fluid, interactive mindmap using **Mermaid.js** via secure HTML injection.
- **Strict Agentic RAG Gate**: An AI assistant strictly bounded to your document context to prevent hallucinations.
- **Dynamic API Status Gate**: Live visual indicators (`Ready` / `Missing`) verifying Google AI Studio connection.

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit (Python)
- **AI Engine**: Google Gemini 2.5 Flash API
- **Visuals & Graphs**: Mermaid.js via HTML Injection
- **Document Parsing**: PyPDF Reader
- **Deployment**: Vercel

## ⚙️ Local Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/TechnologyHereIT/arxivllm.git](https://github.com/TechnologyHereIT/arxivllm.git)
   cd arxivllm