@echo off
cat tests\data\imports.txt tests\data\%1.txt %2 | flask shell