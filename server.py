import socket
import threading

# Налаштування сервера
HOST = '127.0.0.1'  # Локальний хост
PORT = 12345        # Виберіть будь-який вільний порт

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Функція розсилки повідомлень всім клієнтам
def broadcast(message):
    for client in clients:
        client.send(message)

# Функція обробки повідомлень від клієнта
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} вийшов з чату!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Прийом підключень до сервера
def receive():
    while True:
        client, address = server.accept()
        print(f"Підключено {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Нікнейм клієнта: {nickname}')
        broadcast(f'{nickname} приєднався до чату!'.encode('utf-8'))
        client.send('Ви підключилися до сервера!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Сервер працює...")
receive()
