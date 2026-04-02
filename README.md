# 🎨 Figma → Code MCP (Ollama + DeepSeek)

> Turn Figma designs into clean, responsive HTML/CSS using AI — powered by MCP, DeepSeek, and Ollama.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![MCP](https://img.shields.io/badge/Protocol-MCP-green)
![Figma](https://img.shields.io/badge/Integration-Figma-purple)
![LLM](https://img.shields.io/badge/LLM-DeepSeek-orange)
![Status](https://img.shields.io/badge/Status-Working-success)

---

## 📌 Overview

This project is a **Model Context Protocol (MCP) server** that connects:

* 🎨 **Figma Designs**
* 🤖 **AI Assistants (Claude, Cursor)**
* ☁️ **Cloud LLMs (DeepSeek via Ollama)**

It allows AI to:

* Read Figma files
* Understand UI structure
* Generate **production-ready HTML/CSS**

---

## ⚡ Features

### 🛠️ Available Tools

| Tool                       | Description                                |
| -------------------------- | ------------------------------------------ |
| `get_figma_design_info`    | Fetch full Figma file structure & metadata |
| `generate_code_from_figma` | Convert Figma nodes → HTML + CSS           |
| `describe_and_generate`    | Generate UI from text prompts              |

---

## 🧠 Architecture

```
Claude / Cursor
      ↓
   MCP Client
      ↓
 FastMCP Server (Python)
      ↓
 ┌───────────────┬────────────────────┐
 │ Figma API     │ DeepSeek (Ollama)  │
 │ (Design Data) │ (Code Generation)  │
 └───────────────┴────────────────────┘
```

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **fastmcp**
* **Figma REST API**
* **Ollama Cloud API**
* **DeepSeek LLM**
* **python-dotenv**

---

## 📦 Installation

### 1. Clone the repository

```powershell
git clone https://github.com/MusW02/figma-ollama-mcp.git
cd figma-ollama-mcp
```

### 2. Create virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 🔑 Create `.env` file

```env
FIGMA_ACCESS_TOKEN=your_figma_token_here
OLLAMA_API_KEY=your_ollama_key_here
OLLAMA_MODEL=deepseek-v3.1:671b-cloud
FIGMA_FILE_ID=your_default_figma_file_id
OLLAMA_ENDPOINT=https://ollama.com/api/generate
```

⚠️ **Important:**
Make sure `.env` is added to `.gitignore` to protect your keys.

---

## 🤖 Connect with Claude Desktop

### 📍 Config File

* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
* **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

### 🧩 Add this:

```json
{
  "mcpServers": {
    "figma-ollama-mcp": {
      "command": "C:\\Path\\To\\figma-ollama-mcp\\venv\\Scripts\\python.exe",
      "args": ["C:\\Path\\To\\figma-ollama-mcp\\figma_ollama_server.py"]
    }
  }
}
```

✅ No need to add API keys here — `.env` handles it securely.

---

## 💡 Usage Example

Just ask your AI assistant:

> "Generate HTML and CSS for node 12:34 from my Figma file"

Behind the scenes:

1. MCP calls `generate_code_from_figma`
2. Fetches design data from Figma
3. Sends it to DeepSeek
4. Returns clean, responsive code

---

## 🎯 Use Cases

* Convert **Figma → Frontend instantly**
* Build **AI-powered UI generators**
* Speed up **frontend development workflows**
* Learn **MCP + LLM integrations**

---

## 🚀 Future Improvements

* [ ] Tailwind CSS support
* [ ] React component generation
* [ ] Multi-node layout support
* [ ] Live preview UI
* [ ] Docker deployment

---

## 📂 Project Structure

```
figma-ollama-mcp/
│
├── figma_ollama_server.py  # MCP server
├── requirements.txt        # Dependencies
├── .env                    # Secrets (ignored)
├── .gitignore              # Ignore rules
└── README.md               # Documentation
```

---

## 🔄 Transport Layer

Default:

```python
mcp.run(transport="stdio")
```

For browser testing:

```python
mcp.run(transport="sse")
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Submit a PR

---

## 📜 License

MIT License

---

## ⭐ Support

If this helped you:

* ⭐ Star the repo
* 🍴 Fork it
* 📢 Share it

---

## 👨‍💻 Author

**Mustafa Waqar**
Aspiring ML Engineer | AI & Data Science

---

## 🚀 Push to GitHub

```powershell
git add README.md
git commit -m "docs: add professional README for figma MCP project"
git push origin main
```
