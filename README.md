# keeprising

Creating a local streamlit web app for sourdough monitoring. 

## Setup
I use the anaconda navigator to create an environment using the `environment-keeprising.yml`.
Before you can start, you have to provide an OpenAI API key and the local path to the project folder.
1. Create an OpenAI API key (https://platform.openai.com/account/api-keys). 
2. Create a 
Next you have to store the key `openai_api_key` and your **organization ID** `openai_organization` in a folder called `config` in a `config.json` file. 

## Usage
At the moment:
1. run the `dummy_data_creation.ipynb` notebook to (re)set the data to its original form and save it to the local file 
2. start the conda environment
3. go to the folder where everything is stored (local)
4. `streamlit run Hello.py`
Voila. 
5. If you need to reset the data because you messed things up, I fear you will have to reset to dummy data by running the notebook `dummy_data_creation.ipynb`.

## Todo
* modify process so that row is only added if a feeding or a baking has been done
* expand app with plots
* update environment.yml
* transform dummy_data_creation in a python script
* add flour types to baking notebook (multiselect)
* giving suggestions on breads based on bread rating and desired bread type
* eventually install sketch to condaenv
* create a utils.py and store all the tiny functions in there -> find a way to use a module
* in the beginning no config/config.json  was created -> maybe include a way to have a start page which asks the user to put in some credentials and store them automaticall
* blackcellmagic was not installed via .yml file
* PATH is not dynamic, so I had to change it, I created a data  folder