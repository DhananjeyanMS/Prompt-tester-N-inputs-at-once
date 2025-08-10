# Gemini Prompt Tester (Flask App)

A lightweight **Flask web application** for testing prompts with multiple Google Gemini models.  
It allows you to upload system prompts, multiple input prompts, tweak generation settings, and get outputs in a structured table.

---

## 🚀 Features

- **Multiple Model Support** – Choose from available Gemini models (`gemini-1.5-flash-latest`, `gemini-2.0-flash-001`, `gemini-2.5-flash`, etc.).
- **Batch Prompt Testing** – Upload multiple `.txt` files as prompts to run requests in one go.
- **System Prompt Upload** – Optionally upload a `.txt` file to act as the system message.
- **Configurable Parameters** – Set temperature, top_p, and top_k values for output control.
- **Results Table** – View input-output pairs in a clean HTML table.
- **File Upload Restrictions** – Only `.txt` files are allowed.
- **Basic UI** – HTML template and CSS styling included in `templates/` and `static/`.

---

## 📂 Project Structure

```
.
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # UI for uploading files and viewing results
├── static/
│   └── style.css         # Styles for the interface
├── uploads/              # Temporary file storage (auto-created)
├── .env                  # Store your Gemini API key here
└── README.md             # Documentation
```

---

## 🔑 Prerequisites

- Python 3.8+
- A valid **Google Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Basic understanding of prompt engineering

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/gemini-prompt-tester.git
   cd gemini-prompt-tester
   ```

2. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**
   ```bash
    flask
    python-dotenv
    google-generativeai
    werkzeug
   ```

4. **Set Environment Variables**
   - Create a `.env` file in the root directory:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

---

## ▶️ Running the App

```bash
python app.py
```

The app will run on **http://127.0.0.1:5002** by default.

---

## 🖥 Usage

1. Go to `http://127.0.0.1:5002` in your browser.
2. Select a Gemini model from the dropdown.
3. Enter your Gemini API key (or set it in `.env`).
4. Optionally upload a **System Prompt** (`.txt` file).
5. Upload **one or more Input Prompt Files** (`.txt` only).
6. Adjust `temperature`, `top_p`, and `top_k` settings if needed.
7. Click **Submit** to run multiple requests and view results.

---

## ⚙️ Configuration

- **UPLOAD_FOLDER**: Defaults to `uploads/`
- **MAX_CONTENT_LENGTH**: 16 MB limit
- **Allowed File Types**: `.txt` only
- **Generation Config**:
  - `temperature`: Controls creativity (default: `1.0`)
  - `top_p`: Nucleus sampling (default: `0.95`)
  - `top_k`: Limits token sampling to top_k tokens (default: `40`)

---


- [Flask](https://flask.palletsprojects.com/)
- [Google Generative AI Python SDK](https://pypi.org/project/google-generativeai/)
