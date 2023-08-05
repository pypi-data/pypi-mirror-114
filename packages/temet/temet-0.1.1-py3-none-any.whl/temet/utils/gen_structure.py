import os

def gen_fastapi():
    os.mkdir('app')
    os.mkdir('app/models')
    os.mkdir('app/routers')
    os.mkdir('app/.temet')
    os.mkdir('app/templates')
    os.system('git clone https://github.com/cgmark101/temet-files.git files')
    os.system('cp files/main.py app')
    os.system('cp files/ping.py app/routers')
    os.system('cp files/index.html app/templates')
    os.system('cp files/hellow.py app/models')
    os.system('cp files/requirements.txt app')
    os.system('cp files/python.gitignore app/.gitignore')
    os.system('virtualenv .venv')
    os.system('.venv/bin/python -m pip install --upgrade pip')
    os.system('.venv/bin/pip install -r app/requirements.txt')
    os.system('rm -rf files')