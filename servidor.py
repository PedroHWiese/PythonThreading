import socket
import threading
import time
import queue

def handle_client(conn, addr, response_queue):
    print("Conexão estabelecida com", addr)

    for i in range(100):
        # Receber a mensagem do cliente
        data = conn.recv(1024).decode('utf-8')
        messages = data.split()  # Dividir as mensagens com base nos espaços em branco

        for message in messages:
            print("Cliente:", message)

            if message == 'Olá':
                # Enviar "Oi" como resposta para o cliente
                time.sleep(1)
                response = "Oi\n"
                response_queue.put(response.encode('utf-8'))  # Coloca a resposta na fila
                response_queue.join()  # Aguarda até que a resposta anterior tenha sido enviada

    print("Conexão encerrada com", addr)
    conn.close()

def enviar_resposta(response_queue):
    HOST = '127.0.0.1'  # Endereço IP do servidor (loopback)
    PORT = 12345       # Porta para a comunicação

    # Criar um objeto de socket para enviar respostas
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as response_conn:
        response_conn.connect((HOST, PORT))

        while True:
            response = response_queue.get()
            response_conn.sendall(response)
            response_queue.task_done()

def servidor():
    HOST = '127.0.0.1'  # Endereço IP do servidor (loopback)
    PORT = 12345       # Porta para a comunicação

    response_queue = queue.Queue()

    # Criar um objeto de socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Vincular o socket ao endereço e porta especificados
        s.bind((HOST, PORT))

        # Permitir que o servidor aguarde conexões entrantes
        s.listen()

        print("Servidor aguardando conexões...")

        response_thread = threading.Thread(target=enviar_resposta, args=(response_queue,))
        response_thread.start()

        while True:
            
            # Aguardar uma nova conexão
            conn, addr = s.accept()

            # Criar uma thread para lidar com o cliente conectado
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, response_queue))
            client_thread.start()

if __name__ == "__main__":
    servidor()
