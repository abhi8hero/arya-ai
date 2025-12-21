import os
from dotenv import load_dotenv
import gradio as gr
from google import genai

# ----------------------------
# Load API key
# ----------------------------
load_dotenv()
api_key = os.getenv("GEN_API_KEY")
if not api_key:
    raise ValueError("GEN_API_KEY not found in .env!")

client = genai.Client(api_key=api_key)

# ----------------------------
# Chat function
# ----------------------------
def chat_with_arya(message, history):
    if not message.strip():
        return history, ""
    prompt = "You are Arya AI, a helpful assistant.\n"
    for msg in history:
        prompt += f"User: {msg['role'] == 'user' and msg['content'] or ''}\n"
        prompt += f"Arya AI: {msg['role'] == 'assistant' and msg['content'] or ''}\n"
    prompt += f"User: {message}\nArya AI:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response.text.strip()}
        ]
        return new_history, ""
    except Exception as e:
        return history + [{"role": "assistant", "content": f"Error: {e}"}], ""

# ----------------------------
# Gradio UI
# ----------------------------
with gr.Blocks(css="""
    #chatbot {
        background-color: #1e1e2f;
        color: #e0e0e0;
        border-radius: 10px;
        padding: 10px;
    }
    .gr-textbox {
        display: flex;
        align-items: center;
    }
    .gr-textbox input {
        flex: 1;
        border-radius: 20px 0 0 20px;
        padding: 10px;
        border: 1px solid #555;
        background-color: #2c2c3c;
        color: #e0e0e0;
    }
    .send-btn {
        border-radius: 0 20px 20px 0;
        padding: 10px 15px;
        margin: 0;
        background-color: #6c63ff;
        color: white;
        border: none;
        cursor: pointer;
    }
    .send-btn:hover {
        background-color: #5750d4;
    }
    h1 {
        text-align: center;
        color: #6c63ff;
        font-family: Arial, sans-serif;
    }
    /* Custom footer */
    #custom-footer {
        text-align: center;
        font-size: 14px;
        padding: 8px;
        color: #aaa;
        background-color: #1b1b28;
        border-top: 1px solid #333;
        margin-top: 10px;
    }
    #custom-footer a {
        color: #6c63ff;
        text-decoration: none;
        margin: 0 5px;
    }
    #custom-footer a:hover {
        text-decoration: underline;
    }
""") as demo:

    gr.Markdown("<h1> Arya AI</h1>\nPowered by Google Gemini. A powerful artificial intelligence chatbot for all your curiosity.", elem_id="header")

    chatbot = gr.Chatbot(elem_id="chatbot", height=450)

    with gr.Row():
        msg = gr.Textbox(placeholder="Type a message...", elem_id="user_input")
        send_btn = gr.Button("➤", elem_classes="send-btn")

    clear_btn = gr.Button("Clear")

    # Connect send button and Enter key
    send_btn.click(chat_with_arya, [msg, chatbot], [chatbot, msg])
    msg.submit(chat_with_arya, [msg, chatbot], [chatbot, msg])
    clear_btn.click(lambda: [], None, chatbot)

    # Custom footer
    gr.HTML("""
    <div id="custom-footer">
        Developed by <a href="#">Abhi The Great</a> 
        
    </div>
    """)

# ----------------------------
# Launch
# ----------------------------
demo.launch()
