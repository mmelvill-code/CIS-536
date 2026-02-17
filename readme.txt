To build and execute this program:

1) Create a new folder for this project. Have a command line terminal opened at that folder location.

2) Add the following files to the folder created in step 1
CheckPoint1.py
tiny_wikipedia.txt

3) Create a python virtual environment for the project.

At the terminal type:

> python -m venv .venv
> source .venv/bin/activate

4) Install nltk 

At the terminal type:

> pip install nltk 

5) Install the required nltk data

At the terminal, type:

> python
>>> import nltk
>>> nltk.download('wordnet', download_dir='./nltk_data')
>>> exit()

6) Execute the python script.

At the terminal, type:

> python CheckPoint1.py