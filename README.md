# keeprising

Creating a local streamlit web app for sourdough monitoring. 

## Setup
I use the anaconda navigator to create an environment using the `environment-keeprising.yml`

## Usage
At the moment:
1. run the `dummy_data_creation.ipynb` notebook to (re)set the data to its original form and save it to the local file 
2. start the conda environment
3. go to the folder where everything is stored (local)
4. `streamlit run keeprising.py`
Voila. 

## Todo
* expand app with plots
    * find out why plot is not shown
* add feature to add latest data in streamlit (if possible) and save the latest feeding data to local files
* store path in a external notebook/file to be called
