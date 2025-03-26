import telnetlib


class TelnetConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """Устанавливает соединение с модемом через Telnet."""
        try:
            self.connection = telnetlib.Telnet(self.host, self.port, timeout=10)
            print(f"Успешное подключение к {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def authenticate(self, login, password):
        """Авторизуется на модеме с использованием логина и пароля."""
        try:
            # Ожидание строки "login:" или аналогичной
            response = self.connection.read_until(b"login:", timeout=10).decode('ascii', errors='ignore')
            print(f"Ответ модема (логин): {response}")  # Отладочный вывод
            if "login" in response.lower():
                self.connection.write(login.encode('ascii') + b"\n")
            else:
                print("Не удалось найти приглашение для ввода логина.")
                return False

            # Ожидание строки "Password:" или аналогичной
            response = self.connection.read_until(b"Password:", timeout=10).decode('ascii', errors='ignore')
            print(f"Ответ модема (пароль): {response}")  # Отладочный вывод
            if "password" in response.lower():
                self.connection.write(password.encode('ascii') + b"\n")
            else:
                print("Не удалось найти приглашение для ввода пароля.")
                return False

            # Чтение ответа после авторизации
            response = self.connection.read_until(b"\n", timeout=10).decode('ascii', errors='ignore')
            print(f"Ответ модема (после авторизации): {response}")  # Отладочный вывод

            # Если модем не отправляет явного подтверждения, считаем авторизацию успешной
            if not response.strip():
                print("Авторизация завершена, но подтверждение не получено.")
                return True

            # Проверяем стандартные подтверждения
            if "success" in response.lower() or "welcome" in response.lower():
                return True

            print("Авторизация не удалась. Ответ модема не содержит подтверждения.")
            return False
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            return False

    def send_command(self, command):
        """Отправляет команду на модем через Telnet."""
        if not self.connection:
            return "Нет подключения."
        try:
            # Отправка команды с возвратом каретки (\r\n)
            print(f"Отправка команды: {command}")  # Отладочный вывод
            self.connection.write(command.encode('ascii') + b"\r\n")
            
            # Увеличенный таймаут для ожидания ответа
            response = self.connection.read_until(b"#", timeout=15).decode('ascii', errors='ignore')
            print(f"Полный ответ на команду '{command}': {response}")  # Отладочный вывод

            # Удаляем баннер BusyBox, если он присутствует
            if "BusyBox" in response or "Enter 'help'" in response:
                response = response.split("\n", 1)[-1]  # Убираем первую строку с баннером

            # Удаляем приглашение оболочки (~ #)
            response = response.replace("~ #", "").strip()

            # Удаляем лишние пустые строки
            response_lines = [line.strip() for line in response.splitlines() if line.strip()]
            response = "\n".join(response_lines)

            # Если ответ пустой, возможно, команда не выполнена
            if not response.strip():
                return "Команда не выполнена или модем не ответил."

            return response
        except Exception as e:
            print(f"Ошибка при выполнении команды '{command}': {e}")
            return f"Ошибка: {e}"

    def is_connected(self):
        """Проверяет, установлено ли соединение."""
        return self.connection is not None

    def disconnect(self):
        """Закрывает Telnet-соединение."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Соединение закрыто.")