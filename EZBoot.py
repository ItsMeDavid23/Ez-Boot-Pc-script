# Description: This script is used to automate the login process for games and applications on a Windows PC.
import time
import pyautogui
import time
import socket
import os

#codigo para mostrar o diretorio de onde este ficheiro esta a correr
print(os.getcwd())  # Mostra o diretório de trabalho atual

def send_success_message(connection):
    success_message = "Information received successfully\n"
    connection.send(success_message.encode('utf-8'))
    print("Information received successfully from mobile app -> client")

def send_finish_message(connection):
    finish_message = "Order completed successfully"
    connection.send(finish_message.encode('utf-8'))
    print("Order completed successfully -> client")

def login_to_game(game_or_app, needs_auth, username, password, staySignedIn):

    pyautogui.hotkey('winleft')
    
    if needs_auth == "1":
        if game_or_app == "LOL" or game_or_app == "Valorant":
                pyautogui.typewrite(game_or_app)
                pyautogui.press('enter')

                # Aguardar o jogo abrir
                time.sleep(8.5)  # Ajuste o tempo com base no desempenho do seu sistema

                # Simular clique nos campos de nome de usuário e senha
                pyautogui.typewrite(username)
                pyautogui.press('tab')
                pyautogui.typewrite(password)

                # Se a opção "Stay Signed In" estiver marcada, pressione a tecla Tab
                if staySignedIn == "1":
                    # Simular clique na Check box "Stay Signed In" + botão de login
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    time.sleep(0.1)
                    pyautogui.press('enter')
                    pyautogui.press('tab')
                    pyautogui.press('enter')
                else:
                    # Simular clique no botão de login
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('tab')
                    pyautogui.press('enter')

                # Entrar no perfil do jogador
                time.sleep(20)  # Ajuste o tempo com base no desempenho do seu sistema
                pyautogui.click(x=1007, y=138)  # Ajuste as coordenadas com base na resolução do seu ecrã
                pyautogui.moveTo(x=1919, y=550)  # Ajuste as coordenadas com base na resolução do seu ecrã

        if game_or_app == "GTA5":   
            # Abrir RockStar Games Laucher - GTA 5
                pyautogui.typewrite('Rockstar Games')
                pyautogui.press('enter') 
                time.sleep(15)
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('enter')
                
    else: 
        pyautogui.typewrite(game_or_app)
        pyautogui.press('enter')

    send_finish_message(connection) 

# Esperar que o PC tenha internet
print("Esperando que o PC tenha internet...")  # Ajuste a mensagem conforme necessário
time.sleep(5)
print("começou")
PC_PORT = 12345
while True:
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        break  # Saia do loop se o bind for bem-sucedido

    except socket.error as e:
        if e.errno == 10049:
            print("Erro 10049 ao vincular o soquete. Tentando novamente em 3 segundos.")
            time.sleep(3)
        else:
            print(f"Erro inesperado: {e}")
            break

server_socket.settimeout(30)  # Define o tempo limite para 30 segundos
TIMEOUT = 10  # Tempo limite em segundos

# Tenta vincular o soquete dentro do limite de tempo
start_time = time.time()
while True:
    try:
        server_socket.bind(("192.168.1.71", PC_PORT))
        print("Soquete vinculado com sucesso!")
        break  # Sai do loop se a ligação for bem-sucedida
    except Exception as e:
        if time.time() - start_time > TIMEOUT:
            print(f"Erro ao vincular o soquete: {e}")
            time.sleep(10)
            break
        else:
            time.sleep(0.5)  # Aguarda meio segundo antes de tentar novamente

server_socket.listen(1)
print(f"Servidor aguardando conexão na porta {PC_PORT}...")

try:
    connection, address = server_socket.accept()
    print(f"Conexão recebida de {address}")

    # Leia a variável enviada pelo cliente
    data = connection.recv(1024)

    if data:
        received_variable = data[2:].decode('utf-8') 

        print(f"Variável recebida: {received_variable}")
        #print("ASCII:", [ord(char) for char in received_variable])

        # Passo 1: Dividir a string recebida
        parts = received_variable.split(',')

        # Passo 2: Atribuir valores às variáveis
        game_or_app = parts[0]
        needs_auth = parts[1]
        username = parts[2]
        password = parts[3] 
        staySignedIn = parts[4] 

        # Passo 3: Verificar a necessidade de autenticação
        if needs_auth == "1":
            print(f"Autenticação necessária para {game_or_app}.")
            print(f"Username: {username}, Password: {password}, Stay Signed In: {staySignedIn}")
        else:
            print(f"Nenhuma autenticação necessária para {game_or_app}.")

        send_success_message(connection)        
    
        if game_or_app and needs_auth and username and password and staySignedIn:
            login_to_game(game_or_app, needs_auth, username, password, staySignedIn)    
        else:
            print("Credenciais não fornecidas.")

except socket.timeout:
    print("Tempo limite de espera excedido. Nenhuma conexão recebida.")
    time.sleep(5)

finally:
    # Feche a conexão e o soquete do servidor
    connection.close()
    server_socket.close()
    print("Terminado")
    time.sleep(100)