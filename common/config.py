# PyPI:
from dotenv import dotenv_values
import os
import pathlib

chatgpt_35_turbo = {"name": "gpt-3.5-turbo"}
chatgpt_4_turbo = {"name": "gpt-4-turbo-preview"}



# Local:


### Paths ###

# Path to this file:
# (Use pathlib as os.getcwd() changes when using jupyter notebooks)
config_path = pathlib.Path(__file__).parent.resolve()
root_path = os.path.join(config_path, "..")

# Define the path to the data directory within the backend directory:
# data_path = pathlib.Path(backend_path, "data/").resolve()


### Environment Variables ###

# Path to .env file defined in Taskfile
# (Default to .env.dev needed for jupyter notebooks):
dotenv_path = os.path.join(root_path, os.getenv("DOT_ENV_FILE", ".env"))
env_vars = dotenv_values(dotenv_path)