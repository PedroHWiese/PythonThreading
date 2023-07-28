import socket
import threading
import time

def handle_client(conn, addr):
    print("Conexão estabelecida com", addr)

    for _ in range(100):
        # Receber a mensagem do cliente
        data = conn.recv(1024).decode('utf-8')
        print("Cliente:", data)

        if data == 'Olá':
            # Enviar "Oi" como resposta para o cliente
            response = "Oi\n"
            conn.sendall(response.encode('utf-8'))

    print("Conexão encerrada com", addr)
    conn.close()

def servidor():
    HOST = '127.0.0.1'  # Endereço IP do servidor (loopback)
    PORT = 12345       # Porta para a comunicação

    # Criar um objeto de socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Vincular o socket ao endereço e porta especificados
        s.bind((HOST, PORT))

        # Permitir que o servidor aguarde conexões entrantes
        s.listen()

        print("Servidor aguardando conexões...")

        while True:
            # Aguardar uma nova conexão
            conn, addr = s.accept()

            # Criar uma thread para lidar com o cliente conectado
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    servidor()
