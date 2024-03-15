import gradio as gr
import requests

def ask_backend(question):
    response = requests.post("http://localhost:8000/ask", json={"question": question})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def update(name):
    return f"Welcome to Gradio, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("# Welcome to keeprising!")
    gr.Markdown("## Looking for help?")
    with gr.Row():
        inp = gr.Textbox(placeholder="Ask your question here")
        out = gr.Textbox()
    btn = gr.Button("Run")
    btn.click(fn=ask_backend, inputs=inp, outputs=out)

demo.launch()

# interface = gr.Interface(fn=ask_backend, inputs="text", outputs="text")


