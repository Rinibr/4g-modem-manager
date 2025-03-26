def send_command(connection, command):
    """
    Отправляет команду на модем через Telnet и возвращает ответ.
    """
    if not connection:
        return "Нет подключения."
    try:
        print(f"Отправка команды: {command}")  # Отладочный вывод
        connection.write(command.encode('ascii') + b"\r\n")  # Отправка команды с \r\n
        
        # Увеличенный таймаут для ожидания ответа
        response = connection.read_until(b"#", timeout=15).decode('ascii', errors='ignore')
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


def reboot_modem(connection):
    """
    Перезагружает модем.
    """
    return send_command(connection, "reboot")


def get_help(connection):
    """
    Получает список доступных команд.
    """
    return send_command(connection, "help")


def get_pwd(connection):
    """
    Получает текущую директорию.
    """
    return send_command(connection, "pwd")


def list_files(connection):
    """
    Показывает список файлов в текущей директории.
    """
    return send_command(connection, "ls")


def exit_shell(connection):
    """
    Выходит из режима оболочки (если модем находится в BusyBox).
    """
    return send_command(connection, "exit")


def get_uptime(connection):
    """
    Получает время работы системы.
    """
    return send_command(connection, "uptime")


def get_version(connection):
    """
    Получает информацию о версии системы.
    """
    return send_command(connection, "version")