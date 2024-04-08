import gradio as gr
import requests
from gradio_calendar import Calendar
import datetime
import gradio as gr
from common.calendar import update_feedings
from common.config import data_path
from pathlib import Path
import pandas as pd

def ask_backend(question):
    response = requests.post("http://localhost:8000/ask", json={"question": question})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return f"Error: {response.status_code}, {response.text}"
    
feedings_data = pd.read_csv(Path(data_path,"feedings.csv"))

with gr.Blocks() as demo:
    gr.Markdown("# Welcome to keeprising!")
    with gr.Tab("Help"):
        gr.Markdown("## Looking for help?")
        with gr.Column():
            inp = gr.Textbox(placeholder="Ask your question here")
            out = gr.Textbox()
        btn = gr.Button("Run")
        btn.click(fn=ask_backend, inputs=inp, outputs=out)
        with gr.Row():
            thumbs_down = gr.Button(value="👎")
            thumbs_up = gr.Button(value="👍")
    with gr.Tab("Feedings"):
        gr.Markdown("## Feedings")        
        with gr.Row():
            feedings_overview = gr.DataFrame(value=feedings_data, interactive=False)
            # Create the Calendar component for date input
            feeding_date = Calendar(type="datetime", label="Select a date", info="Click the calendar icon to bring up the calendar.")
            feeding_date.change(fn=update_feedings, inputs=feeding_date, outputs=feedings_overview)




demo.launch()

# interface = gr.Interface(fn=ask_backend, inputs="text", outputs="text")


