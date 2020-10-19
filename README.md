# Users Service

[![Build Status](https://travis-ci.com/BookBnB/users-service.svg?branch=master)](https://travis-ci.com/BookBnB/users-service)

## Entorno

Crear un entorno virtual de python:

```
python3 -m venv venv
```

Activación del entorno:

```
. venv/bin/activate
```

Asegurarse de activarlo cada vez que se necesite trabajar con el proyecto.

## Install dependencies

Instalar dependencias:

```
pip install -r requirements.txt
```

## Ejecutar pruebas

Sin cobertura:

```
python -m pytest tests
```

Con cobertura:

```
coverage run -m pytest
coverage report
```

## Migraciones

Ejecutar migraciones:

```
flask db upgrade
```

Crear nuevo script de migración (generado en el directorio `migrations/versions`):

```
flask db migrate -m <name>
```

## Ejecutar aplicación

Configurar archivo `.env` con los valores apropiados y ejecutar `run.sh`
