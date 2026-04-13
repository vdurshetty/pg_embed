# pg_embed
Postgres embed images, audio and vedios data 


# file-upload
Python API to upload files

# ai_samples
AI Samples 


# PIP upgrade 
python3.10 -m pip install --upgrade pip

# Project Setup 
1. git clone https://api_token@github.com/vdurshetty/pg_embed.git
2. python3.10 -m venv pg_embed   (will pick the latest python version) [for specific version use # python3.10 -m venv file-upload]
3. source pg_embed/bin/activate
4. cd pg_embed
5. create requirements.txt 

# Run Ollama server local 
% ollama serve (ther server starts and listerns on the port 11434)
% ollama run gemma4:e4b  (Run gemma4 chat )

run through
curl http://localhost:11434/api/generate -d '{
  "model": "gemma4:e4b",
  "prompt": "Summarize the key ideas behind transformer architecture in three bullet points.",
  "stream": false
}'




## Install python libraries 
% pip install -r requirements.txt 
% pip uninstall -r requirements.txt -y 
## New with pyproject.toml
% pip install build
% pip install -e .  (Install packages mentioned in the pyproject.toml)
% pip install -d '.[dev]'  (install dev dependencies )
% python -m build 
% pip freeze    (List all installed packages)

## Run the REST API server 
% gunicorn main:app
% uvicorn myapi:app --reload


# Database
cloud pgvector database : https://supabase.com/dashboard/project/hjutiuttzsdrzoyzuzmx/database/schemas


1. Connection string

postgresql://postgres:[password]@db.hjutiuttzsdrzoyzuzmx.supabase.co:5432/postgres








