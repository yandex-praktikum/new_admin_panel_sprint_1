docker run -d \
  --name postgres-yandex \
  -p 5434:5434 \
  -v $HOME/postgresql/data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=123qwe \
  -e POSTGRES_USER=app \
  -e POSTGRES_DB=movies_database  \
  postgres:13