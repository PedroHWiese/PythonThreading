import socket
import threading
import time

def enviar_mensagem(s, message):
    s.sendall(message.encode('utf-8'))
    response = s.recv(1024).decode('utf-8')
    print("Resposta do servidor:", response)

def cliente():
    HOST = '127.0.0.1'  # Endereço IP do servidor (loopback)
    PORT = 12345       # Porta para a comunicação

    # Criar um objeto de socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conectar ao servidor
        s.connect((HOST, PORT))

        threads = []
        for _ in range(100):
            thread = threading.Thread(target=enviar_mensagem, args=(s, 'Olá'))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Fechando a conexão após todas as mensagens serem enviadas
        s.close()

if __name__ == "__main__":
    cliente()
