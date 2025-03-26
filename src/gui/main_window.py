import json
import subprocess
import platform
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit, QLabel, QTabWidget, QProgressBar, QFileDialog, QHBoxLayout, QComboBox
)
from telnet.connection import TelnetConnection
from telnet.commands import send_command


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4G Modem Manager")
        self.setGeometry(100, 100, 600, 400)

        # Telnet connection
        self.telnet = None

        # Main layout with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Tab 1: Connection and Commands
        self.connection_tab = QWidget()
        self.tabs.addTab(self.connection_tab, "Подключение")
        self.setup_connection_tab()

        # Tab 2: Signal Monitoring
        self.signal_tab = QWidget()
        self.tabs.addTab(self.signal_tab, "Сигнал")
        self.setup_signal_tab()

        # Tab 3: Network Diagnostics
        self.diagnostics_tab = QWidget()
        self.tabs.addTab(self.diagnostics_tab, "Диагностика сети")
        self.setup_diagnostics_tab()

        # Tab 4: Connection Management
        self.connection_management_tab = QWidget()
        self.tabs.addTab(self.connection_management_tab, "Управление подключением")
        self.setup_connection_management_tab()

        # Tab 5: Network Interface Management
        self.network_interface_tab = QWidget()
        self.tabs.addTab(self.network_interface_tab, "Сетевые интерфейсы")
        self.setup_network_interface_tab()

        # Timer for dynamic updates
        self.signal_timer = QTimer()
        self.signal_timer.timeout.connect(self.refresh_signal)

    def setup_connection_tab(self):
        layout = QVBoxLayout(self.connection_tab)

        # Compact layout for connection inputs
        form_layout = QHBoxLayout()

        # IP and Port input
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP (например, 192.168.100.1)")
        form_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Порт (например, 4719)")
        form_layout.addWidget(self.port_input)

        layout.addLayout(form_layout)

        # Login and Password input
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Buttons for connection and settings
        button_layout = QHBoxLayout()

        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.connect_to_modem)
        button_layout.addWidget(self.connect_button)

        self.save_settings_button = QPushButton("Сохранить")
        self.save_settings_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_settings_button)

        self.load_settings_button = QPushButton("Загрузить")
        self.load_settings_button.clicked.connect(self.load_settings)
        button_layout.addWidget(self.load_settings_button)

        layout.addLayout(button_layout)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

    def setup_signal_tab(self):
        layout = QVBoxLayout(self.signal_tab)

        # Signal Strength Label
        self.signal_label = QLabel("Уровень сигнала:")
        layout.addWidget(self.signal_label)

        # Signal Strength Progress Bar
        self.signal_progress = QProgressBar()
        self.signal_progress.setRange(0, 100)
        layout.addWidget(self.signal_progress)

        # Detailed Signal Information
        self.signal_details = QTextEdit()
        self.signal_details.setReadOnly(True)
        layout.addWidget(self.signal_details)

        # Start/Stop Signal Monitoring Button
        self.toggle_signal_button = QPushButton("Начать мониторинг")
        self.toggle_signal_button.clicked.connect(self.toggle_signal_monitoring)
        layout.addWidget(self.toggle_signal_button)

    def toggle_signal_monitoring(self):
        if self.signal_timer.isActive():
            self.signal_timer.stop()
            self.toggle_signal_button.setText("Начать мониторинг")
            self.signal_label.setText("Мониторинг сигнала остановлен.")
        else:
            self.signal_timer.start(5000)  # Обновление каждые 5 секунд
            self.toggle_signal_button.setText("Остановить мониторинг")
            self.signal_label.setText("Мониторинг сигнала запущен.")

    def refresh_signal(self):
        if not self.telnet or not self.telnet.is_connected():
            self.signal_label.setText("Ошибка: Сначала подключитесь к модему.")
            return

        # Пример команды для получения уровня сигнала
        response = send_command(self.telnet.connection, "cat /proc/net/wireless")
        if response:
            try:
                lines = response.splitlines()
                for line in lines:
                    if "wlan0" in line:
                        parts = line.split()
                        link_quality = int(float(parts[2]))
                        signal_level = int(float(parts[3]))
                        noise_level = int(float(parts[4]))

                        # Обновляем прогресс-бар и метку
                        self.signal_progress.setValue(max(0, min(100, link_quality)))
                        self.signal_label.setText(f"Уровень сигнала: {link_quality}%")

                        # Обновляем подробную информацию
                        self.signal_details.setText(
                            f"Качество связи: {link_quality}%\n"
                            f"Уровень сигнала: {signal_level} dBm\n"
                            f"Уровень шума: {noise_level} dBm\n"
                        )
            except Exception as e:
                self.signal_label.setText(f"Ошибка при обработке сигнала: {e}")
        else:
            self.signal_label.setText("Не удалось получить данные о сигнале.")

    def setup_diagnostics_tab(self):
        layout = QVBoxLayout(self.diagnostics_tab)

        # Input for diagnostics commands
        self.diagnostics_input = QLineEdit()
        self.diagnostics_input.setPlaceholderText("Введите команду (например, ping 8.8.8.8)")
        layout.addWidget(self.diagnostics_input)

        # Run diagnostics button
        self.run_diagnostics_button = QPushButton("Выполнить")
        self.run_diagnostics_button.clicked.connect(self.run_diagnostics)
        layout.addWidget(self.run_diagnostics_button)

        # Diagnostics output
        self.diagnostics_output = QTextEdit()
        self.diagnostics_output.setReadOnly(True)
        layout.addWidget(self.diagnostics_output)

    def setup_connection_management_tab(self):
        layout = QVBoxLayout(self.connection_management_tab)

        # Buttons for enabling/disabling mobile internet
        self.enable_internet_button = QPushButton("Включить интернет")
        self.enable_internet_button.clicked.connect(self.enable_internet)
        layout.addWidget(self.enable_internet_button)

        self.disable_internet_button = QPushButton("Отключить интернет")
        self.disable_internet_button.clicked.connect(self.disable_internet)
        layout.addWidget(self.disable_internet_button)

        # Status output
        self.connection_status_output = QTextEdit()
        self.connection_status_output.setReadOnly(True)
        layout.addWidget(self.connection_status_output)

    def setup_network_interface_tab(self):
        layout = QVBoxLayout(self.network_interface_tab)

        # Dropdown for selecting network interface
        self.interface_selector = QComboBox()
        self.interface_selector.addItem("Выберите интерфейс")
        layout.addWidget(self.interface_selector)

        # Input for manual IP configuration
        self.ip_config_input = QLineEdit()
        self.ip_config_input.setPlaceholderText("Введите IP-адрес (например, 192.168.1.100)")
        layout.addWidget(self.ip_config_input)

        # Buttons for setting IP or enabling DHCP
        button_layout = QHBoxLayout()

        self.set_ip_button = QPushButton("Установить IP")
        self.set_ip_button.clicked.connect(self.set_manual_ip)
        button_layout.addWidget(self.set_ip_button)

        self.enable_dhcp_button = QPushButton("Включить DHCP")
        self.enable_dhcp_button.clicked.connect(self.enable_dhcp)
        button_layout.addWidget(self.enable_dhcp_button)

        layout.addLayout(button_layout)

        # Output area for network interface management
        self.interface_output = QTextEdit()
        self.interface_output.setReadOnly(True)
        layout.addWidget(self.interface_output)

    def connect_to_modem(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        if not ip or not port:
            self.output_area.append("Ошибка: Укажите IP-адрес и порт.")
            return

        if not login or not password:
            self.output_area.append("Ошибка: Укажите логин и пароль.")
            return

        self.telnet = TelnetConnection(ip, int(port))
        if self.telnet.connect():
            self.output_area.append(f"Успешное подключение к {ip}:{port}")
            if self.telnet.authenticate(login, password):
                self.output_area.append("Авторизация завершена.")
                self.load_network_interfaces()
            else:
                self.output_area.append("Ошибка авторизации. Проверьте логин и пароль.")
        else:
            self.output_area.append(f"Ошибка подключения к {ip}:{port}")

    def load_network_interfaces(self):
        if not self.telnet or not self.telnet.is_connected():
            self.interface_output.append("Ошибка: Сначала подключитесь к модему.")
            return

        response = send_command(self.telnet.connection, "ifconfig -a")
        if response:
            self.interface_selector.clear()
            self.interface_selector.addItem("Выберите интерфейс")
            for line in response.splitlines():
                if line and not line.startswith(" "):
                    interface_name = line.split()[0]
                    self.interface_selector.addItem(interface_name)
            self.interface_output.append(f"Доступные интерфейсы:\n{response}")
        else:
            self.interface_output.append("Не удалось загрузить список интерфейсов.")

    def set_manual_ip(self):
        interface = self.interface_selector.currentText()
        ip_address = self.ip_config_input.text()

        if interface == "Выберите интерфейс" or not ip_address:
            self.interface_output.append("Ошибка: Укажите интерфейс и IP-адрес.")
            return

        command = f"ifconfig {interface} {ip_address} netmask 255.255.255.0 up"
        response = send_command(self.telnet.connection, command)
        self.interface_output.append(f"Установка IP-адреса:\n{response}")

    def enable_dhcp(self):
        interface = self.interface_selector.currentText()

        if interface == "Выберите интерфейс":
            self.interface_output.append("Ошибка: Укажите интерфейс.")
            return

        command = f"dhclient {interface}"
        response = send_command(self.telnet.connection, command)
        self.interface_output.append(f"Включение DHCP:\n{response}")

    def run_diagnostics(self):
        command = self.diagnostics_input.text()
        if not command:
            self.diagnostics_output.append("Ошибка: Укажите команду для диагностики.")
            return

        try:
            encoding = "cp866" if platform.system() == "Windows" else "utf-8"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding=encoding)
            self.diagnostics_output.append(f"$ {command}\n{result.stdout}\n{result.stderr}")
        except Exception as e:
            self.diagnostics_output.append(f"Ошибка выполнения команды: {e}")

    def enable_internet(self):
        if not self.telnet or not self.telnet.is_connected():
            self.connection_status_output.append("Ошибка: Сначала подключитесь к модему.")
            return

        response = send_command(self.telnet.connection, "AT+CFUN=1")
        self.connection_status_output.append(f"Включение интернета:\n{response}")

    def disable_internet(self):
        if not self.telnet or not self.telnet.is_connected():
            self.connection_status_output.append("Ошибка: Сначала подключитесь к модему.")
            return

        response = send_command(self.telnet.connection, "AT+CFUN=0")
        self.connection_status_output.append(f"Отключение интернета:\n{response}")

    def save_settings(self):
        settings = {
            "ip": self.ip_input.text(),
            "port": self.port_input.text(),
            "login": self.login_input.text(),
            "password": self.password_input.text(),
        }
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить настройки", "settings.json", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as file:
                json.dump(settings, file)
            self.output_area.append(f"Настройки сохранены в {file_path}.")

    def load_settings(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить настройки", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as file:
                settings = json.load(file)
                self.ip_input.setText(settings.get("ip", ""))
                self.port_input.setText(settings.get("port", ""))
                self.login_input.setText(settings.get("login", ""))
                self.password_input.setText(settings.get("password", ""))
            self.output_area.append(f"Настройки загружены из {file_path}.")