import os
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import whisper
from gtts import gTTS
import logging
from langdetect import detect, DetectorFactory 
import re
import librosa
import sys
import noisereduce as nr
import time


total_response_time = 0.0
response_count = 0

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Pestaway")

# Set consistent results for langdetect
DetectorFactory.seed = 0

# Constants
#MODEL_DIR = r"D:\Downloads\LATEST\out_finetuned1_Epoch_5\checkpoint-125" 
MODEL_DIR = r"D:\\Downloads\\checkpoint-13975-20250509T072357Z-1-002\\checkpoint-13975"
WHISPER_MODEL_SIZE = "large-v3"
MAX_PROMPT_LENGTH = 4096
MAX_LENGTH = 4096


# Load Tokenizer
def load_tokenizer(model_dir):
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    logger.info("Tokenizer loaded successfully.")
    return tokenizer

# Load Model
def load_model(model_dir):
    logger.info("Loading fine-tuned model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    )
    model.config.use_cache = False
    model = model.to("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Model loaded successfully.")
    return model

# Load Whisper Model
def load_whisper_model():
    logger.info("Loading Whisper model...")
    whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
    logger.info("Whisper model loaded successfully.")
    return whisper_model

# Detect Language
def detect_language(text):
    try:
        lang = detect(text)
        # Tagalog-specific keywords to improve detection
        tagalog_keywords = [
    # Original Keywords
    "sakit", "peste", "tanong", "sagot", "gamot", "puno", "ani", "kahalagahan",

    # Health and Agriculture Keywords
    "kalusugan", "karamdaman", "epidemya", "lunas", "halaman", "pananim",
    "anihan", "tanim", "bunga", "sakit ng halaman", "pataba", "panlaban",
    "lason", "sustansya", "panahon", "tagtuyot", "bagyo", "peste ng halaman",
    "katubigan", "lupa",

    # General Keywords
    "bakit", "paanong" "ano", "anong", "paano", "saan", "kailan", "sino", "alin", "kanino",
    "gaano", "ganoon", "ganito", "ito", "iyan", "iyon", "dito", "diyan",
    "doon", "ngayon", "kahapon", "bukas", "kanina", "mamaya", "madali",
    "mahirap", "mabagal", "mabilis", "malaki", "maliit",

    # Pest Management Keywords
    "insekto", "kulisap", "pananim", "pagkalanta", "pagkatuyo",
    "mga peste", "pananalasa", "proteksyon", "pag-iwas", "kontrol",
    "organic na pesticide", "kemikal na pesticide", "likas na lunas",
    "bitag", "pagsusuri", "inspeksyon", "pagsusubaybay",
    "biological control", "natural na kalaban", "pamatay-peste",
    "pananggalang", "panlaban sa peste", "resistensya", "pag-aalaga",
    "mabuting kasanayan sa pagsasaka", "paglilinis", "paggamit ng organikong pataba",
    "compost", "pagpapatubig", "wastong irigasyon"
]
        if any(word in text.lower() for word in tagalog_keywords):
            lang = 'tl'
            
        else: 
            lang = 'en'    
        
        logger.info(f"Detected Language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return "Please make an input again"
    

# Preprocess Audio
def preprocess_audio(audio_path):
    logger.info("Preprocessing audio...")
    try:
        # Load the audio file with librosa
        audio, sr = librosa.load(audio_path, sr=16000)

        # Apply noise reduction to the audio
        logger.info("Applying noise reduction...")
        reduced_noise_audio = nr.reduce_noise(y=audio, sr=sr)

        # Return the cleaned audio
        return reduced_noise_audio
    except Exception as e:
        logger.error(f"Error during audio preprocessing: {e}")
        raise
    
# Transcribe Audio
def transcribe_audio(audio_path, whisper_model):
    try:
        logger.info(f"Transcribing audio: {audio_path}")
        audio = preprocess_audio(audio_path)
        transcription = whisper_model.transcribe(audio, task="transcribe")
        text = transcription.get("text", "").strip()
        logger.info(f"Transcribed Text: {text}")
        return text
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        return "Sorry, I could not process the audio. Please try again."

# Generate Chatbot Response
def generate_response(prompt, tokenizer, model):
    try:
        lang = detect_language(prompt)
        prompt = f"Tanong: {prompt}\nSagot:" if lang == 'tl' else f"Question: {prompt}\nAnswer:"

        inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
        attention_mask = torch.ones_like(inputs)

        outputs = model.generate(
    inputs,
    attention_mask=attention_mask,
    max_new_tokens=1536,         # Extend response length to allow highly detailed answers
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.6,            # Lower for more factual and coherent responses
    top_p=0.92,                 # Slightly lower nucleus sampling for more relevant words
    top_k=40,                   # Slightly lower for better focus on important words
    repetition_penalty=1.05,    # Light penalty to avoid unnecessary loops
    num_return_sequences=1,     # Single response for clarity
    do_sample=True,             # Keeps sampling enabled for natural replies
    eos_token_id=tokenizer.eos_token_id
)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()
        if "Sagot:" in response:
            response = response.split("Sagot:")[-1].strip()

        return response
    except Exception as e:
        logger.error(f"Error during response generation: {e}")
        return "I encountered an issue generating a response. Please try again."

# Convert Text to Speech
def text_to_speech(text, lang="en"):
    try:
        # Add natural pauses after punctuation
        text = re.sub(r'([.,!?])', r'\1 ', text)
        tts = gTTS(text, lang=lang)
        audio_path = "response.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        logger.error(f"Error during text-to-speech conversion: {e}")
        return None

# Load Models
tokenizer = load_tokenizer(MODEL_DIR)
model = load_model(MODEL_DIR)
whisper_model = load_whisper_model()

# Gradio Interface
# Define Custom CSS
custom_css = """
body {
    background-color: #1e1e1e; /* Dark mode */
    font-family: 'Arial', sans-serif;
}

h1 {
    font-size: 32px;
    color: #ffffff;
    text-shadow: 2px 2px 4px #000;
}


.gradio-container {
    max-width: 1600px !important; /* Increase width to force landscape */
    width: 100% !important;
    margin: auto;
    background: #2c2c2c;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
}

.gr-button {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
    font-size: 16px;
} 

.gr-textbox, .gr-audio {
    border: 2px solid #4CAF50 !important;
    border-radius: 5px !important;
}


.gr-chatbot {
    border: 2px solid #5f8b2c !important;
    border-radius: 10px !important;
}

.gr-markdown {
    color: #ffffff !important;
    font-size: 18px;
}

.centered-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
}

/* Fix Row Layout */
.gr-row {
    display: flex !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
}

.gr-column {
    flex: 1 !important;  /* Ensure both columns take equal space */
}

.nature-bg {
    background-image: url('https://www.transparenttextures.com/patterns/asfalt-light.png');
}

.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -20px;
}

.logo-container img {
    width: 150px;
}
"""

# Gradio Interface
with gr.Blocks(css=custom_css) as demo:
    with gr.Row():
        gr.Markdown("<center><h1>🌱 Welcome to PestAway 🌱</h1></center>")

    gr.Markdown("""
        <div style="text-align: center; font-size: 18px; color: #ffffff;">
        I am your assistant for effective pest management. Ask me anything about pest control!
        </div>
    """)

    # Centered PestAway Logo
    gr.HTML("""
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmFydW9ycG42cWJ1N29qcGk2Z2dxY3R0MXRlamI1OWFvdm5iMXhpOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/ZsVN3XgMJtT52b52bk/giphy.gif" width="250px" alt="Talking Robot">
    </div>
    """)

    # Chatbot & Input Layout
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Chat with PestAway", elem_classes="gr-chatbot")
            robot_display = gr.HTML("")  # **Robot GIF placeholder**
        with gr.Column(scale=2):
            msg = gr.Textbox(
                label="💬 Ask a Question",
                placeholder="Type your question...",
                lines=1,
                interactive=True
            )
            audio_input = gr.Audio(sources= "microphone", type="filepath", label="🎙️ Or Speak Your Question")
            transcription_output = gr.Textbox(label="📝 Transcription of Audio Input", interactive=False)
            detected_language = gr.Textbox(label="🌍 Detected Language", interactive=False)
            audio_output = gr.Audio(label="🔊 Chatbot Response in Voice")

    submit = gr.Button("📤 Submit")
    clear = gr.Button("🗑️ Clear Chat")

    def respond(message, audio, chat_history):
        global total_response_time, response_count  # 👈 Allow global modification
        transcription = ""
        detected_lang = "Unknown"
        logger.info(f"Received message: {message}")
        # GIF Animation for Talking Robot
        robot_animation = """
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnUzZGZ3OHB6Y3RmOXRhaGM5aTI1aW95ZGJtejRvZnNndXdqc3o3YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/RLheOHSbMj4b0JfQ1k/giphy.gif" 
        width="250px" alt="Talking Robot">
    </div>
    """
        try:
            start_time = time.time()
            if audio:
                logger.info("Received an audio input, processing transcription...")
                transcription = transcribe_audio(audio, whisper_model)
                detected_lang = detect_language(transcription)
                if detected_lang == "Unsupported":
                    logger.warning("Unsupported language detected, returning an error message.")
                    return "", None, transcription, detected_lang, chat_history, None, ""
                bot_message = generate_response(transcription, tokenizer, model)
                logger.info(f"Generated bot response: {bot_message}")
            else:
                detected_lang = detect_language(message)
                if detected_lang == "Unsupported":
                    return "Sorry, I can only assist in English or Tagalog.", None, "", detected_lang, chat_history, None, ""
                bot_message = generate_response(message, tokenizer, model)
                logger.info(f"Generated bot response: {bot_message}")
                
                end_time = time.time()
                response_time = end_time - start_time

                # Update total time and count
                total_response_time += response_time
                response_count += 1
                average_response_time = total_response_time / response_count

                logger.info(f"⏱️ Response time: {response_time:.2f} sec | Average: {average_response_time:.2f} sec")

                
                
            chat_history.append((message or transcription, bot_message))
            audio_response = text_to_speech(bot_message, lang='tl' if detected_lang == 'tl' else 'en')
            return "", None, transcription, detected_lang, chat_history, audio_response, robot_animation
        except Exception as e:
            logger.error(f"Error in respond function: {e}")
            return "", None, "An error occurred", "Error", chat_history, None, ""
        
        
        
        
        

    # Ensure robot_display is included in the outputs
    submit.click(
        respond,
        inputs=[msg, audio_input, chatbot],
        outputs=[msg, audio_input, transcription_output, detected_language, chatbot, audio_output, robot_display]
    )

    msg.submit(
        respond,
        inputs=[msg, audio_input, chatbot],
        outputs=[msg, audio_input, transcription_output, detected_language, chatbot, audio_output, robot_display]
    )

    clear.click(lambda: ("", None, "", "", [], None, ""), outputs=[msg, audio_input, transcription_output, detected_language, chatbot, audio_output, robot_display])

    

# Launch the App
demo.launch(server_port=8008, server_name='192.168.254.109', share=True, debug=True)
