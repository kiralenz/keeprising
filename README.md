# keeprising

Creating a local streamlit web app for sourdough monitoring. 

## Setup
I use the anaconda navigator to create an environment using the `environment-keeprising.yml`.
Before you can start, you have to create an OpenAI API key. Next you have to store the key `openai_api_key` and your organization ID `openai_organization` in a folder called `config` in a `config.json` file. 

## Usage
At the moment:
1. run the `dummy_data_creation.ipynb` notebook to (re)set the data to its original form and save it to the local file 
2. start the conda environment
3. go to the folder where everything is stored (local)
4. `streamlit run keeprising.py`
Voila. 
5. If you need to reset the data because you messed things up, I fear you will have to reset to dummy data by running the notebook `dummy_data_creation.ipynb`.

## Todo
* transform dummy_data_creation in a python script
* expand app with plots
    * find out why plot is not shown
* add feature to add latest data in streamlit (if possible) and save the latest feeding data to local files
* store path in a external notebook/file to be called
* functionalize the script
* split script into a feeding activity, a baking activity and a dashboard activity + help page
* improve the bread loaf background and store it in a gist
* store the path in the config.json
* create a utils.py and store all the tiny functions in there
