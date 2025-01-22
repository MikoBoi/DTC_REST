1. Убедитесь, что у вас Docker, Docker Compose
2. В корне папки открываем командную строку, вводим следующую команду: docker build . --tag project
2. После успешной сборки, водим следующую команду: docker-compose build
3. 
В docker-compose.yml настроены два сервиса, app и pytest.
Запускаем команду: docker-compose up app, чтобы запустить REST API.
Запускаем команду: docker-compose up pytest, чтобы запустить тесты.

После запуска REST API доступно по адресу: http://localhost:8085
Документация API будет доступна по адресу: http://localhost:8085/docs

Отчет о покрытии тестами будет находиться в папке htmlcov на корне проекта.
