import socket

def get_local_ip():
    # Cria um socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conecta a um endereço remoto arbitrário
        s.connect(("8.8.8.8", 80))
        # Obtém o endereço IP local
        ip_address = s.getsockname()[0]
    except Exception as e: # type: ignore
        ip_address = "Não foi possível obter o IP local"
    finally:
        s.close()
    return ip_address

if __name__ == "__main__":

    print(f"Meu endereço IP local é: http://{get_local_ip()}:8501")