import requests

def ask_backend(question):
    response = requests.post("http://localhost:8000/ask", data={"question": question})
    print(response.json())
    # print(response.json()["answer"])

question = "I took the wrong flour to feed my sourdough. Is that a problem?"

ask_backend(question=question)