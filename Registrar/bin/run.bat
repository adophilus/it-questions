@echo off

set FLASK_APP=Registrar.py
set FLASK_ENV=development

flask run --eager-loading --reload