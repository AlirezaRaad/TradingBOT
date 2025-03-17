import sys
import os
import subprocess


VENV_NAME = "TradingBot_Venv"

# If Venv Do not exists, make one.
if not os.path.exists(VENV_NAME):
    print(f"Did not find venv Folder name {VENV_NAME}, Attempting to create one.")
    subprocess.run([sys.executable, "-m", "venv", VENV_NAME], check=True)


# Seeing If The User Is on Windows or Linux.
if sys.platform == "win32":
    python_venv_path = os.path.join(VENV_NAME, "Scripts", "python.exe")
    with open(".env", "w") as fh:
        fh.write(f"PYTHON_VENV_PATH={python_venv_path}\n")
else:
    python_venv_path = os.path.join(VENV_NAME, "bin", "python")
    with open(".env", "w") as fh:
        fh.write(f"PYTHON_VENV_PATH={python_venv_path}\n")

# Now Upgrade Pip
subprocess.run(
    [python_venv_path, "-m", "pip", "install", "--upgrade", "pip"], check=True
)
print("Upgrading The pip...")

# Now installing dependencies.
if os.path.exists("requirements.txt"):
    subprocess.run(
        [python_venv_path, "-m", "pip", "install", "-r", "requirements.txt"], check=True
    )
    print("Installing dependencies from requirements.txt...")
else:
    print("No requirements.txt found. Skipping dependency installation.")


print("Installing virtual environment and dependencies is complete.")
