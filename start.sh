#!/bin/bash

# Supprime tous les dossiers __pycache__ dans le projet
find . -type d -name "__pycache__" -exec rm -rf {} +

# Lance le script Python
python3 ./run.py