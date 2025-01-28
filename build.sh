#!/bin/bash

# Installation des dépendances
pip install -r requirements.txt

# Mise à jour de l'administrateur
python create_admin.py
