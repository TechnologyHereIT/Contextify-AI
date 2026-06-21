import os
import sys
from flask import Flask

app = Flask(__name__)

# كود تطبيق الـ Streamlit (app.py) الخاص بك بالكامل تم ضغطه وحمايته هنا ليعمل برمجياً بالسيرفر
STREAMLIT_CODE = """import streamlit as st
import os
import requests
import base64
from pypdf import PdfReader

st.set_page_config(
    page_title="Contextify AI - Agentic Research Workspace",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(\"\"\"
<style>
    .main-header { font-size: 2.3rem; font-weight: bold; color: #0f172a; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1rem; color: #64748b; margin-bottom: 1.5rem; }
    .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
    .status-ready { background-color: #22c55e; }
    .status-missing { background-color: #ef4444; }
    .panel-title { font-size: 1.1rem; font-weight: bold; color: #1e293b; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; margin-bottom: 1rem; }
    .success-box { background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745; margin: 1rem 0; }
    .info-box { background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 4px solid #2196f3; color: #333; }
</style>
\"\"\", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧠 Contextify AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Multi-Document Context Engine & Interactive Mindmap Analyzer</p>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "current_pdf_base64" not in st.session_state: st.session_state.current_pdf_base64 = None
if "mindmap_code" not in st.session_state: st.session_state.mindmap_code = None

st.sidebar.markdown('<p class="panel-title">🔑 API Gate</p>', unsafe_allow_html=True)
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", value="", help="Get your API key from Google AI Studio")

if api_key:
    st.sidebar.markdown('<div style="display: flex; align-items: center; padding-bottom: 10px;"><span class="status-indicator status-ready"></span><b style="color:#22c55e;">Ready</b></div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div style="display: flex; align-items: center; padding-bottom: 10px;"><span class="status-indicator status-missing"></span><b style="color:#ef4444;">Missing</b></div>', unsafe_allow_html=True)
    st.sidebar.info("💡 Get your free API key from: [Google AI Studio](https://aistudio.google.com/app/apikey)")

st.sidebar.markdown("---")
st.sidebar.markdown('<p class="panel-title">📁 Repository Lab</p>', unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear Cache & Reset"):
    st.session_state.messages = []
    st.session_state.current_pdf_base64 = None
    st.session_state.mindmap_code = None
    st.rerun()

uploaded_files = st.sidebar.file_uploader("Upload research contexts (PDF, TXT, MD):", accept_multiple_files=True, type=["pdf", "txt", "md"])

documents_content = ""
if uploaded_files:
    for file in uploaded_files:
        documents_content += f"\\n--- Document Name: {file.name} ---\\n"
        if file.type == "text/plain" or file.name.endswith('.md'):
            documents_content += file.read().decode("utf-8")
        elif file.type == "application/pdf":
            bytes_data = file.getvalue()
            st.session_state.current_pdf_base64 = base64.b64encode(bytes_data).decode('utf-8')
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text: documents_content += text + "\\n"
    st.sidebar.success(f"Context loaded: {len(uploaded_files)} paper(s).")

if not api_key:
    st.warning("⚠️ Access Denied: Please provide a valid Gemini API Key in the sidebar control panel to activate Contextify AI.")
    st.stop()

center_panel, right_panel = st.columns([1.1, 0.9], gap="medium")

with center_panel:
    st.markdown('<p class="panel-title">📊 Context Viewport & Graph Workspace</p>', unsafe_allow_html=True)
    if uploaded_files:
        tab_preview, tab_mindmap = st.tabs(["📄 Inline PDF Viewport", "🌿 Interactive Concept Map"])
        with tab_preview:
            if st.session_state.current_pdf_base64:
                pdf_display = f'<iframe src="data:application/pdf;base64,{st.session_state.current_pdf_base64}" width="100%" height="680" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.info("Dynamic text format detected. Switch to 'Interactive Concept Map' tab to initialize graph mapping.")
        with tab_mindmap:
            if st.button("🚀 Structuralize Context into Mindmap"):
                with st.spinner("Agent is architecturalizing the interactive graph schema..."):
                    try:
                        mindmap_prompt = f\"\"\"Analyze the following research context and create a highly structured conceptual mindmap using Mermaid.js syntax.
The root should be the main topic, branching into key methodologies, findings, and details.

CRITICAL INSTRUCTIONS:
1. Return ONLY valid mermaid code block.
2. Start strictly with 'mindmap' syntax keyword.
3. Do NOT wrap it inside markdown backticks. Just output the raw structure text.
4. Keep node titles clean, avoiding complex symbols, colons, or nested quotes.

Research Context:
{documents_content[:6000]} \"\"\"
                        url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
                        headers = {"Content-Type": "application/json", "X-goog-api-key": api_key}
                        payload = {"contents": [{"parts": [{"text": mindmap_prompt}]}], "generationConfig": {"temperature": 0.2}}
                        response = requests.post(url, headers=headers, json=payload, timeout=30)
                        if response.status_code == 200:
                            raw_code = response.json()['candidates'][0]['content']['parts'][0]['text']
                            clean_code = raw_code.replace("```mermaid", "").replace("```", "").strip()
                            st.session_state.mindmap_code = clean_code
                        else:
                            st.error("Failed to compile structural schema via Google API endpoint.")
                    except Exception as e:
                        st.error(f"Render Exception: {str(e)}")
            if st.session_state.mindmap_code:
                st.markdown("##### 📌 Node Topology Engine")
                html_code = f\"\"\"<div class="mermaid" style="display: flex; justify-content: center; align-items: center;">{st.session_state.mindmap_code}</div>
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
</script>\"\"\"
                st.components.v1.html(html_code, height=600, scrolling=True)
            else:
                st.info("Trigger the engine above to project text semantics into a fluid interactive mindmap graph.")
    else:
        st.markdown('<div class="info-box">💡 <strong>Tip:</strong> Upload documents using the sidebar to get started. You can upload PDF, TXT, or MD files.</div>', unsafe_allow_html=True)

with right_panel:
    st.markdown('<p class="panel-title">💬 Deep Agentic Assistant (Strict RAG Interface)</p>', unsafe_allow_html=True)
    chat_container = st.container(height=580)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input("Query summaries, specific formulas, or validation data..."):
        with chat_container:
            with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        system_instruction = f\"\"\"You are a professional Agentic Research Assistant operating under the Contextify AI core. Your strict objective is to answer the user's questions accurately based ONLY on the context of the uploaded documents provided below.

RULES:
1. Answer ONLY based on the provided context information.
2. If the answer cannot be found, reply strictly with: "I could not find this information in the uploaded documents."
3. Be highly precise, objective, and cite document references or page aspects where possible.

Context Data:
{documents_content if documents_content else 'No documents uploaded.'}\"\"\"
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Processing deep RAG pipelines..."):
                    try:
                        url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
                        headers = {"Content-Type": "application/json", "X-goog-api-key": api_key}
                        payload = {"contents": [{"parts": [{"text": f"{system_instruction}\\n\\nUser Question: {prompt}"}]}], "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2048}}
                        response = requests.post(url, headers=headers, json=payload, timeout=30)
                        if response.status_code == 200:
                            full_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                            message_placeholder.markdown(full_response)
                        else:
                            error_msg = response.json().get('error', {}).get('message', 'Unknown Context Error')
                            full_response = f"⚠️ Pipeline Error: {error_msg}"
                            message_placeholder.error(full_response)
                    except Exception as e:
                        full_response = f"❌ System Exception: {str(e)}"
                        message_placeholder.error(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar.expander("📖 How to Use"):
    st.markdown(\"\"\"**Step 1:** Upload your documents (PDF, TXT, or MD)\\n**Step 2:** Ask questions about the uploaded documents in the Chat Panel\\n**Step 3:** Use the Workbench to view raw PDFs or generate interactive Concept Graphs\"\"\")
with st.sidebar.expander("ℹ️ Model Info"):
    st.markdown(\"\"\"**Model:** Gemini 2.5 Flash\\n**Capabilities:** 1M input tokens, Fast response time, Multimodal support\"\"\")

st.markdown("---")
st.markdown(\"\"\"<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 0.5rem;">
    <b>Engineered by:</b> Mohannad Hassounah | <b>GitHub:</b> TechnologyHereIT | 
    <b>Core Ecosystem:</b> Contextify AI Framework | <b>Workshop:</b> Build with AI Saudi Arabia 2026 (#Googleantigravity)
</div>\"\"\", unsafe_allow_html=True)
"""

@app.route('/')
def index():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>Contextify AI - Workspace</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.54.0/build/stlite.css">
    </head>
    <body>
      <div id="root"></div>
      <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.54.0/build/stlite.js"></script>
      <script>
        stlite.mount({{
          requirements: ["requests", "pypdf"],
          entrypoint: "app.py",
          files: {{
            "app.py": `{STREAMLIT_CODE}`
          }},
          streamlitConfig: {{
            "server.headless": true,
            "theme.primaryColor": "#0f172a"
          }}
        }}, document.getElementById("root"));
      </script>
    </body>
    </html>
    """

# تصدير المتغيرات المطلوبة لفحص بيئة Vercel بنجاح
application = app
handler = app
