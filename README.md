# 4G Modem Manager

This project is a graphical user interface (GUI) application designed to manage a 4G modem using Telnet access on port 4719. The application allows users to connect to the modem, send commands, and manage settings through an intuitive interface.

## Features

- Connect to the 4G modem via Telnet.
- Send commands to the modem and receive responses.
- User-friendly GUI for easy interaction.
- Configuration management for modem settings.

## Project Structure

```
4g-modem-manager
├── src
│   ├── main.py               # Entry point of the application
│   ├── gui                   # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py     # Main application window
│   │   └── styles.py         # Styling for GUI components
│   ├── telnet                # Telnet communication
│   │   ├── __init__.py
│   │   ├── connection.py      # Manages Telnet connection
│   │   └── commands.py       # Sends commands to the modem
│   └── utils                 # Utility functions
│       ├── __init__.py
│       └── helpers.py        # Helper functions
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── .gitignore                # Files to ignore in version control
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd 4g-modem-manager
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen instructions to connect to your 4G modem and manage its settings.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.