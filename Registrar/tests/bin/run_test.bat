@echo off
set FLASK_APP=Registrar.py
cat tests\data\imports.txt tests\data\%1.txt %2 | flask shell