# 📚 Multimodal RAG (Retrieval-Augmented Generation) Project
## 📺 Demo Video

[![Watch the demo](https://img.youtube.com/vi/L4EQ5tHuWvY/0.jpg)](https://www.youtube.com/watch?v=L4EQ5tHuWvY)

This project implements a **Multimodal RAG system** using **Ollama local open-source models** (free and runs locally without cloud dependencies). The system can process and summarize:

- ✅ **Text documents**
- ✅ **Images** (OCR + Vision models)
- ✅ **Tables**
- ✅ **Videos** (for frame extraction, image analysis, or playback)

---

## 🚀 Features:

- Runs **entirely offline** with **local LLMs (Ollama)**
- Supports **image understanding**, **table summarization**, and **text retrieval**
- Accepts **multimodal input** (text, images, videos, tables)
- **Video playback and frame extraction support**

---

## 🛠️ Requirements:

- Python 3.8+
- **Ollama installed and running locally** → [https://ollama.com/](https://ollama.com/)
- **uv (Ultra fast Python package manager)** → [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

## 📦 Installation using uv:

> **uv** handles both **dependency management** and **virtual environments** in one step.

### ✅ Install `uv` (if not already installed):

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
