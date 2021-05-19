@echo off
set FLASK_APP=Registrar.py
set FLASK_ENV=development
cat tests\data\imports.txt tests\data\%1.txt | flask shell
rem cat tests\data\output.txt