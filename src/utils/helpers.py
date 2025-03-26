def connect_to_modem(host, port):
    import telnetlib
    try:
        tn = telnetlib.Telnet(host, port)
        return tn
    except Exception as e:
        print(f"Failed to connect to modem at {host}:{port} - {e}")
        return None

def send_command(tn, command):
    try:
        tn.write(command.encode('ascii') + b"\n")
        response = tn.read_until(b"OK", timeout=5)
        return response.decode('ascii')
    except Exception as e:
        print(f"Failed to send command '{command}' - {e}")
        return None

def disconnect_from_modem(tn):
    if tn:
        tn.close()