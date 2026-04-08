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


# Database
cloud pgvector database : https://supabase.com/dashboard/project/hjutiuttzsdrzoyzuzmx/database/schemas


1. Connection string

postgresql://postgres:[password]@db.hjutiuttzsdrzoyzuzmx.supabase.co:5432/postgres








