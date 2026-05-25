# 📄 Agentic Document Generator (AI Doc-Gen)

**An autonomous AI agent that evaluates inputs and independently decides how to structure, format, and generate documentation for Source Code, GitHub PRs, and CI/CD logs.** Built for the **AI Hackathon**, this tool acts as a smart developer assistant, eliminating the tedious task of manual documentation and deployment debugging.

---

## ✨ Core Features

* 🤖 **Autonomous Context Detection:** The AI agent automatically identifies the input context (e.g., Python scripts, GitHub Diffs, CI/CD Runner logs) and dynamically constructs the best prompt strategy.
* 💻 **Multi-File Source Code Analysis:** Upload multiple files or paste raw code. The agent analyzes the logic and generates either a deep architectural scan or a beginner-friendly README.
* 🔗 **Live GitHub PR Summarizer:** Paste any public GitHub PR URL. The agent fetches the patch diffs and generates concise release notes or technical debt reviews.
* 🚀 **DevOps & CI/CD Debugger:** Paste failing or successful deployment logs (Jenkins, GitHub Actions, AWS) to instantly get an Engineering Debug Report with actionable fix items.
* ⚡ **Live Streaming & Smart Downloads:** Watch the documentation generate in real-time. The agent dynamically suggests a relevant file name for a 1-click Markdown (`.md`) download.
* 🔒 **Secure & Stateless:** Built with a gatekeeper Welcome Screen. User API keys are only held in the temporary session state and are completely cleared upon logout or session end.

---

## 🛠️ Tech Stack
* **Frontend & Framework:** [Streamlit](https://streamlit.io/)
* **AI Engine:** Google Generative AI ([Gemini 1.5 Flash](https://ai.google.dev/))
* **Language:** Python 3
* **Integrations:** GitHub Patch/Diff API

---

## How to Test

1. Open the App.
2. On the **Welcome Screen**, paste your temporary **Gemini API Key**. *(Rest assured, this key is only stored in your browser's session state and is not saved anywhere).*
3. Click **Enter Workspace**.
4. Select a mode:
   * **Source Code:** Upload `.py`, `.js`, or `.dart` files to see architectural documentation.
   * **GitHub PR:** Paste a valid PR link (e.g., `https://github.com/streamlit/streamlit/pull/8500`) to see the impact report.
   * **CI/CD Logs:** Paste failing logs to get a root-cause analysis.
5. Click **Generate** and watch the agent stream the response!

---

## 💻 Running Locally

If you wish to run this agent on your local machine:

1. Clone this repository:
   ```bash
   git clone
