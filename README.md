# flask-tests

Repo de pruebas de flask

Correr con "docker-compose up -d --build"
Para verificar servicio: "curl localhost:5000" deberia devolver un json con hello:world

Para verificar migraciones: "curl localhost:5000/users_cols" devuelve las columnas de la tabla de usuarios
