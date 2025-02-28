#!/bin/bash

# Supprime tous les dossiers __pycache__ dans le projet
find . -type d -name "__pycache__" -exec rm -rf {} +

rm instance/database.db

# Lance le script Python
python3 ./run.py