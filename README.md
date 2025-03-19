# **How to Navigate**

Hello, I made this project to see the challenges while making a trading. Without further talk let's see how to install and use the project.</br>

## Making the virtual environment
If you already have a venv and know how to install from requirements.txt, you can first <b>add python path to .env file</b> and just skip this part.</br></br>
If you don't know how make a venv or you are not in a mood to first make a venv and the installing the packages, just simply run setup.py; This file will automatically make a virtual environment and then install all the requirement packages and add python path to the .env file.</br></br>

## Run and *ENJOY*
After making the venv, you can just go ahead and run `main.py` and it automatically activate the venv and run the program.</br></br>

# A more detailed explanation
Now I will explain how the program works in detail for my fellow eager programmers. If you are not interested, you can just ignore this part

## *Files in the ***main*** directory*

### setup.py
1. This program first check if you have venv file in your directory not, and if you don't have it, it will make one and then executes:
```
python -m venv VENV_NAME
```

2. Then it will check that if you are a windows user or a mac/linux user in order to save you python path into .env file.
For WIndows users:
```
os.path.join(VENV_NAME, "Scripts", "python.exe")
```
For mac/linux users:
```
os.path.join(VENV_NAME, "bin", "python")
```

3. Then it will upgrade pip via:
 ```
PYTHON_VENV_PATH -m pip install --upgrade pip
 ```
4. Now in the last step it will install all the packages in requirements.txt file:
```
PYTHON_VENV_PATH -m pip install -r requirements.txt
```

### main.py
This script first loads the PYTHON_VENV_PATH path in the .env file, Then it will locate `streamlit.exe` file, then it will run the WebApp/main.py file via:
```
streamlit_path run WebApp\\main.py
```

## *Files in the ***WebApp*** Directory*