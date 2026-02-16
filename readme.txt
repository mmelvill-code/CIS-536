To build and execute this program:

1) Create a new folder for this project. Have a command line terminal opened at that folder location.

2) Add the file CheckPoint1.py to the folder created in step 1.

3) Create a python virutal environment for the project.

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
>>> nltk.download('punkt_tab', download_dir='./nltk_data')
>>> nltk.download('wordnet', download_dir='./nltk_data')
>>> exit()

6) Create a folder called "tiny_wikipedia". Put your copy of tiny_wikipedia.txt in it.

7) Execute the python script.

At the terminal, type:

> python CheckPoint1.py