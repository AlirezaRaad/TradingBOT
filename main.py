import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Finding Streamlit.exe
python_path = os.path.dirname(os.path.abspath(os.environ["PYTHON_VENV_PATH"]))
streamlit_path = os.path.join(python_path, "streamlit.exe")


subprocess.run([streamlit_path, "run", "WebApp\main.py"])
