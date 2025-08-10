import os
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey_for_flash_messages'  # Replace with a strong secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

GEMINI_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash-001", 
    "gemini-2.5-flash", 

]

@app.route('/', methods=['GET', 'POST'])
def index():
    # This will store a list of {"input": "...", "output": "..."} dictionaries
    results_table_data = [] 
    
    # Get previously selected model if available for sticky dropdown
    selected_model = request.form.get('gemini_model', "gemini-pro") 

    if request.method == 'POST':
        api_key = request.form.get('api_key')
        selected_model = request.form.get('gemini_model') 

        if not api_key:
            flash('Please set your Gemini API Key.', 'error')
            return redirect(request.url)

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            flash(f"Error configuring Gemini API: {e}", 'error')
            return redirect(request.url)

        system_message = None
        if 'system_message_file' in request.files:
            system_file = request.files['system_message_file']
            if system_file and allowed_file(system_file.filename):
                filename = secure_filename(system_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                system_file.save(filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    system_message = f.read()
            elif system_file.filename != '':
                flash('Invalid file type for system message. Only .txt allowed.', 'error')
                return redirect(request.url)

        # Store input messages as a list of strings
        raw_input_messages = [] 
        input_files = request.files.getlist('input_message_files')
        for input_file in input_files:
            if input_file and allowed_file(input_file.filename):
                filename = secure_filename(input_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                input_file.save(filepath)
                with open(filepath, 'r', encoding='utf-8') as f:
                    raw_input_messages.append(f.read())
            elif input_file.filename != '':
                flash(f'Invalid file type for input message: {input_file.filename}. Only .txt allowed.', 'error')
                return redirect(request.url)

        if not raw_input_messages:
            flash('Please upload at least one input message file.', 'error')
            return redirect(request.url)

        try:
            temperature = float(request.form.get('temperature', 1.0))
            top_p = float(request.form.get('top_p', 0.95))
            top_k = int(request.form.get('top_k', 40))
        except ValueError:
            flash('Invalid value for temperature, top_p, or top_k. Please enter numbers.', 'error')
            return redirect(request.url)

        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": 8192,
        }

        try:
            model = genai.GenerativeModel(model_name=selected_model)
        except Exception as e:
            flash(f"Error initializing Gemini model '{selected_model}': {e}", 'error')
            return redirect(request.url)

        try:
            # Start a chat session (if system message is present, it sets up initial history)
            # Otherwise, it's a fresh chat for each message, but if you want continuous, keep one chat object
            # For displaying input-output pairs, we'll iterate and send each input separately.
            
            for input_text in raw_input_messages:
                current_chat_history = []
                if system_message:
                    current_chat_history.append({"role": "user", "parts": [system_message]})
                    current_chat_history.append({"role": "model", "parts": ["Understood."]}) 
                
                # Each input gets its own chat session to ensure isolated input-output pairs
                # If you want a continuous conversation, you would start one chat and keep sending messages
                # For a table of distinct input-output pairs, this approach is better.
                chat = model.start_chat(history=current_chat_history)
                
                response = chat.send_message(input_text, generation_config=generation_config)
                
                results_table_data.append({
                    "input": input_text,
                    "output": response.text
                })

        except Exception as e:
            flash(f"Error generating content with Gemini: {e}", 'error')

    return render_template('index.html', 
                           results_table_data=results_table_data, # Pass the list of dictionaries
                           gemini_models=GEMINI_MODELS, 
                           selected_model=selected_model)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
