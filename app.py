import streamlit as st
import google.generativeai as genai
import time
import requests

# Page Configuration
st.set_page_config(page_title="AI Doc-Gen", page_icon="📄", layout="wide")

# Custom CSS Theme (Clean UI)
custom_theme = """
<style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stApp {margin-top: -30px;}
    .stButton>button {
        border-radius: 8px;
        transition: 0.3s;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
</style>
"""
st.markdown(custom_theme, unsafe_allow_html=True)

# Callback to handle the Custom Stop Button
def stop_generation():
    st.session_state.is_generating = False
    st.session_state.current_screen = 'input'

# --- SESSION STATE INITIALIZATION ---
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'generated_doc' not in st.session_state:
    st.session_state.generated_doc = ""
if 'detected_lang' not in st.session_state:
    st.session_state.detected_lang = ""
if 'dynamic_file_name' not in st.session_state:
    st.session_state.dynamic_file_name = "technical_documentation.md"
if 'run_code_input' not in st.session_state:
    st.session_state.run_code_input = ""
if 'run_prompt_context' not in st.session_state:
    st.session_state.run_prompt_context = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# --- SCREEN 0: WELCOME ---
if st.session_state.current_screen == 'welcome':
    st.write("")
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Welcome to AI Doc-Gen")
        st.markdown("Hello Judges! Thank you for evaluating our hackathon submission. To explore the documentation capabilities, please authenticate the AI engine below.")
        
        st.info("💡 **Instructions:** Please paste your Gemini API Key to proceed. We do not store this key, and it will be cleared once the session ends.")
        
        temp_api_key = st.text_input("Enter Gemini API Key:", type="password", placeholder="AIzaSy...")
        
        st.write("")
        if st.button("🚪 Enter Workspace", type="primary", use_container_width=True):
            if temp_api_key.strip():
                st.session_state.api_key = temp_api_key.strip()
                st.session_state.current_screen = 'input'
                st.rerun()
            else:
                st.error("⚠️ Please enter a valid API Key to continue.")

# --- SIDEBAR (App Guide) ---
if st.session_state.current_screen in ['input', 'output']:
    with st.sidebar:
        st.markdown("### 💡 App Guide")
        st.markdown("**What you can do:**")
        st.markdown("- 🔍 Auto-detect your code context")
        st.markdown("- 🌐 Summarize GitHub PRs instantly")
        st.markdown("- 📝 Auto-generate downloadable files")
        st.markdown("- ⚡ Watch live documentation streaming")
        st.markdown("---")
        if st.button("🔒 Logout / Change Key", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.current_screen = 'welcome'
            st.rerun()

# --- SCREEN 1: INPUT ---
if st.session_state.current_screen == 'input':
    st.title("📄Documentation Generator")
    st.markdown("Select an input source for analysis:")
    
    input_mode = st.radio("Mode", ["💻 Source Code", "🔗 GitHub Pull Request", " CI/CD Logs"], horizontal=True, label_visibility="collapsed")
    st.write("") 
    
    code_input = ""
    prompt_context = ""
    
    if "Source Code" in input_mode:
        col1, col2 = st.columns(2)
        with col1:
            uploaded_files = st.file_uploader("Upload Code File", accept_multiple_files=True, label_visibility="collapsed")
            if uploaded_files:
                for file in uploaded_files:
                    code_input += f"\n\n--- File: {file.name} ---\n\n"
                    code_input += file.read().decode("utf-8")
                st.success(f"{len(uploaded_files)} File(s) loaded successfully!", icon="✅")
        with col2:
            pasted_code = st.text_area("Or paste raw code:", height=150, label_visibility="collapsed", placeholder="Paste your code here...")
            if pasted_code:
                code_input += f"\n\n--- Pasted Code ---\n\n"
                code_input += pasted_code
                
        st.markdown("#### Documentation Settings")
        c1, c2 = st.columns(2)
        with c1: doc_style = st.selectbox("Audience:", ["Developer/Professional", "Beginner-Friendly"])
        with c2: doc_length = st.radio("Detail:", ["Standard README", "Deep Architectural Scan"])
        prompt_context = f"Generate standard documentation. Tone: {doc_style}. Level: {doc_length}."

    elif "Pull Request" in input_mode:
        pr_url = st.text_input("Enter GitHub PR URL", placeholder="e.g., https://github.com/owner/repo/pull/1")
        if pr_url:
            try:
                diff_url = pr_url.replace("github.com", "patch-diff.githubusercontent.com/raw") + ".diff"
                response = requests.get(diff_url)
                if response.status_code == 200:
                    code_input = response.text
                    st.success("Successfully fetched PR code changes!", icon="✅")
                else:
                    st.error("Failed to fetch PR. Ensure the repository is public or the URL is correct.")
            except Exception:
                st.error("Invalid URL format. Please check and try again.")
                
        st.markdown("#### PR Settings")
        c1, c2 = st.columns(2)
        with c1: pr_focus = st.selectbox("Focus Area:", ["Changelog & Impact", "Code Review & Tech Debt"])
        with c2: pr_format = st.radio("Format:", ["Markdown Release Notes", "Bullet Points"])
        prompt_context = f"Generate a PR report. Focus: {pr_focus}. Format: {pr_format}."

    elif "CI/CD Logs" in input_mode:
        cicd_logs = st.text_area("Paste Deployment Logs", height=200, placeholder="Paste GitHub Actions, Jenkins, or AWS logs here...")
        if cicd_logs:
            code_input = cicd_logs
            
        st.markdown("#### DevOps Settings")
        c1, c2 = st.columns(2)
        with c1: log_target = st.selectbox("Target Audience:", ["Executive Summary", "Engineering Debug Report"])
        with c2: log_detail = st.radio("Include Metrics:", ["Include Build Times/Stats", "Just Pass/Fail Status"])
        prompt_context = f"Generate a Deployment report. Audience: {log_target}. Metrics: {log_detail}."

    st.write("")
    st.write("")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("Generate Documentation", type="primary", use_container_width=True):
            if not st.session_state.api_key:
                st.error("Please enter a Gemini API Key on the welcome screen.")
            elif not code_input.strip():
                st.warning("Please provide the required input data (Code, PR Link, or Logs).")
            else:
                st.session_state.run_code_input = code_input
                st.session_state.run_prompt_context = prompt_context
                st.session_state.is_generating = True
                st.session_state.current_screen = 'output'
                st.rerun()

# --- SCREEN 2 & 3: PROCESSING & OUTPUT ---
elif st.session_state.current_screen == 'output':
    st.html("<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>")
    
    # --- IF GENERATING (LIVE STREAMING MODE) ---
    if st.session_state.is_generating:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title("⚙️ Processing Input...")
        with col2:
            st.button("🛑 Stop", on_click=stop_generation, use_container_width=True)
        
        with st.spinner("Analyzing input and streaming response..."):
            genai.configure(api_key=st.session_state.api_key)
            
            detected_lang = "General Context"
            if "def " in st.session_state.run_code_input or "class " in st.session_state.run_code_input: detected_lang = "Python Source"
            elif "function" in st.session_state.run_code_input or "=>" in st.session_state.run_code_input: detected_lang = "JavaScript/TypeScript Source"
            elif "diff --git" in st.session_state.run_code_input: detected_lang = "GitHub Pull Request (Diff)"
            elif "Build" in st.session_state.run_code_input or "Runner" in st.session_state.run_code_input: detected_lang = "CI/CD Deployment Log"
            
            st.session_state.detected_lang = detected_lang
            
            final_prompt = f"""
            You are an AI Technical Documentation Assistant.
            Detected Input Type: {detected_lang}.
            
            Task Instructions:
            {st.session_state.run_prompt_context}
            
            CRITICAL RULES:
            1. The VERY FIRST LINE of your response MUST be exactly in this format: "File Name: your_dynamic_name.md".
            2. DO NOT generate raw base64 image strings.
            3. Ensure the markdown output is clean, readable, and properly formatted starting from the second line.
            
            Raw Input Data:
            ```
            {st.session_state.run_code_input}
            ```
            """
            
            available_model = None
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_model = m.name
                        break
            except Exception:
                pass
            
            if available_model:
                try:
                    model = genai.GenerativeModel(available_model)
                    response = model.generate_content(final_prompt, stream=True)
                    
                    doc_placeholder = st.empty()
                    full_text = ""
                    
                    for chunk in response:
                        full_text += chunk.text
                        doc_placeholder.markdown(full_text + "▌") 
                    
                    doc_placeholder.markdown(full_text) 
                    
                    raw_output = full_text.strip()
                    if raw_output.startswith("File Name:"):
                        parts = raw_output.split("\n", 1)
                        st.session_state.dynamic_file_name = parts[0].replace("File Name:", "").replace("`", "").replace("**", "").strip()
                        st.session_state.generated_doc = parts[1].strip() if len(parts) > 1 else raw_output
                    else:
                        st.session_state.dynamic_file_name = "generated_docs.md"
                        st.session_state.generated_doc = raw_output
                        
                    st.session_state.is_generating = False
                    st.rerun() 
                    
                except Exception as e:
                    st.session_state.is_generating = False
                    error_msg = str(e).lower()
                    if "429" in error_msg or "quota" in error_msg:
                        st.error("⏳ API rate limit reached. Please wait 60 seconds and try again.")
                    else:
                        st.error("❌ An error occurred during generation. Please check your API key or input data.")
            else:
                st.session_state.is_generating = False
                st.error("❌ No supported models found. Please check your API key.")

    # --- IF FINISHED (FINAL STATIC UI) ---
    else:
        st.markdown("## 📄 Generated Documentation")
        st.info(f"**Context Detected:** {st.session_state.detected_lang}")
        
        tab_preview, tab_raw = st.tabs(["👁️ Preview", "📝 Raw Markdown"])
        
        with tab_preview:
            st.markdown(st.session_state.generated_doc)
            
        with tab_raw:
            st.code(st.session_state.generated_doc, language="markdown")
            
        st.write("") 
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.download_button(
                label=f"📥 Download ({st.session_state.dynamic_file_name})",
                data=st.session_state.generated_doc,
                file_name=st.session_state.dynamic_file_name,
                mime="text/markdown",
                use_container_width=True
            )
        with col_btn2:
            if st.button("⬅️ Process New Input", type="primary", use_container_width=True):
                st.session_state.current_screen = 'input'
                st.rerun()