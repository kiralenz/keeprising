# keeprising
## Use Cases
* ask question about your sourdough
* submit images to find out, what's wrong with your sourdough
* create your own recipe book
* track how often you fed

## Get started
* `poetry install`
* copy .env.example to .env and fill the api key

## Concept
* backend
* frontend

## Use (or rather test at the moment)
* backend
    * `cd backend`
    * `uvicorn main:app --reload`
    * e.g. `curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"I took the wrong flour to feed my sourdough. Is that a problem?\"}"`
* frontend
    * `cd frontend`
    * `poetry run python gradio_frontend.py`
    * open [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser