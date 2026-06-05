import os
from huggingface_hub import HfApi

# Ensure you have your HF_TOKEN exported in your terminal: export HF_TOKEN="your_token"
token = os.environ.get("HF_TOKEN")
api = HfApi(token=token)

user_info = api.whoami()
username = user_info['name']

repo_id = f"{username}/QEC-Automation"

print(f"Uploading files to {repo_id}...")
api.upload_folder(
    folder_path="/home/mehran/Downloads/Air-University-QEC-Python-Script-main",
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=["venv/**/*", "venv", ".git/**/*", ".git", "__pycache__/**/*", "*.pyc", "app.log", "deploy.py"]
)
print("Uploaded successfully! Your app is now live at:")
print(f"https://huggingface.co/spaces/{repo_id}")
