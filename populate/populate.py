import os
from time import sleep
import subprocess  # Importando o módulo subprocess

scripts_python = [
    "populate_subject.py",
    "populate_student.py",
    "populate_teacher.py",
    "populate_rating.py",
    "populate_favorite_teacher.py",
    "populate_classroom.py",
]

for script in scripts_python:
    result = subprocess.run(["python", script], capture_output=True, text=True)
    print(f"Executando {script}...")
    print(result.stdout)  
    if result.returncode != 0:
        print(f"Erro ao executar {script}: {result.stderr}")
    sleep(1)
