# Users Service

[![Build Status](https://travis-ci.com/BookBnB/users-service.svg?branch=master)](https://travis-ci.com/BookBnB/users-service)
[![codecov](https://codecov.io/gh/BookBnB/core/branch/master/graph/badge.svg?token=3HYQW6VBPY)](https://codecov.io/gh/BookBnB/users-service)
[![Heroku](https://img.shields.io/badge/heroku-master-success.svg?l?style=flat&logo=heroku&logoColor=white&labelColor=494998)](https://users-service-master.herokuapp.com/)
[![Heroku](https://img.shields.io/badge/heroku-develop-success.svg?l?style=flat&logo=heroku&logoColor=white&labelColor=494998)](https://users-service-develop.herokuapp.com/)

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
