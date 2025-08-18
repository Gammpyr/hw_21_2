# Импорт встроенной библиотеки для работы веб-сервера
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    # def do_GET(self):
    #     """ Метод для обработки входящих GET-запросов """
    #     self.send_response(200)  # Отправка кода ответа
    #     self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
    #     self.end_headers()  # Завершение формирования заголовков ответа
    #     with open('contacts.html', 'r', encoding='utf-8') as file:
    #         data = file.read()
    #     self.wfile.write(bytes(data, "utf-8"))  # Тело ответа

    def do_GET(self):
        if self.path == '/':
            self.path = '/contacts.html'
        try:
            with open(self.path[1:], 'r', encoding='utf-8') as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(file.read(), "utf-8"))
        except:
            self.send_error(404)

    # def do_POST(self):
    #     """ Метод для обработки входящих POST-запросов """
    #     content_length = int(self.headers['Content-Length'])
    #     body = self.rfile.read(content_length)
    #     print("Received POST data:", body)
    #     self.send_response(200)
    #     self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Парсим данные формы
        form_data = parse_qs(post_data)

        # Выводим в консоль сервера
        print("\n=== Получены данные формы ===")
        print(f"Имя: {form_data.get('name', [''])[0]}")
        print(f"Email: {form_data.get('email', [''])[0]}")
        print(f"Сообщение: {form_data.get('message', [''])[0]}")
        print("============================")

        # Отправляем ответ
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = {"status": "success", "message": "Форма получена"}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))


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
    print("Сервер остановлен")
