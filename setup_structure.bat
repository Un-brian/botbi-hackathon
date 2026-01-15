@echo off
echo Creando estructura del proyecto...

mkdir backend frontend automation templates data docs
mkdir backend\routes backend\services backend\utils
mkdir frontend\css frontend\js frontend\assets
mkdir automation\tasks

type nul > backend\__init__.py
type nul > backend\routes\__init__.py
type nul > backend\services\__init__.py
type nul > backend\utils\__init__.py
type nul > automation\__init__.py'
type nul > automation\tasks\__init__.py
type nul > frontend\assets\.gitkeep
type nul > data\.gitkeep
type nul > .env.example
type nul > docs\API.md
type nul > docs\SETUP.md

echo  Estructura creada exitosamente!
pause