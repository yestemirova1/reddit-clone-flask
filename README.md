# reddit-clone-flask
Аналог reddit.com написанный на python 3 с использованием фреймворка Flask

### Создания образа Docker
Создайте образ Docker, клонировав репозиторий Git.
```
$ git clone https://github.com/gazizayestemirova/reddit-clone-flask.git
$ docker build -t yestemirova/reddit-clone-flask .
```

### Скачать предварительно подготовленное изображение
Вы также можете загрузить существующее изображение с [DockerHub](https://hub.docker.com/r/yestemirova/reddit-clone-flask).
```
docker pull yestemirova/reddit-clone-flask
```

### Запуск контейнера
Создайте контейнер из изображения.
```
$ docker run -d -p 8080:8080 yestemirova/reddit-clone-flask
```

Теперь вы можете перейти по ссылке http://localhost:8080 в браузере

Если вы используете docker machine (на Mac OS X или Windows) используйте команду docker inspect чтобы узнать IP-адрес
```
$ docker inspect [CONTAINER ID]
```
