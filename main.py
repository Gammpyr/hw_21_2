# Импорт встроенной библиотеки для работы веб-сервера
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        with open('contacts.html', 'r', encoding='utf-8') as file:
            data = file.read()
        self.wfile.write(bytes(data, "utf-8"))  # Тело ответа

    # def do_POST(self):
    #     """Обработка POST-запросов с JSON-данными"""
    #     try:
    #         # Получаем длину тела запроса
    #         content_length = int(self.headers.get('Content-Length', 0))
    #
    #         # Читаем и декодируем тело
    #         body = self.rfile.read(content_length).decode('utf-8')
    #         print("Received POST data:", body)
    #
    #         # Парсинг JSON (если нужно)
    #         try:
    #             data = json.loads(body)
    #             print("Parsed JSON:", data)
    #         except json.JSONDecodeError:
    #             print("Not a JSON")
    #
    #         # Отправляем успешный ответ
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #
    #         # Можно отправить ответ обратно
    #         response = {"status": "success"}
    #         self.wfile.write(json.dumps(response).encode('utf-8'))
    #
    #     except Exception as e:
    #         self.send_response(500)
    #         self.end_headers()
    #         print("Error:", str(e))

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print("Received POST data:", body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
