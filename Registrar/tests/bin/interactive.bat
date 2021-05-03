@echo off
set FLASK_APP=Registrar.py
flask shell < tests\data\imports.txt