from socket import *
from time import strftime
import threading

name = ''
your_name = ''

ascii_art = []
ascii_art.append("                                                                  \n ,-----.                            ,--------.       ,--.,--.     \n'  .--./ ,---.  ,---. ,---.  ,--,--.'--.  .--',--,--.|  ||  |,-.  \n|  |    | .-. || .--'| .-. |' ,-.  |   |  |  ' ,-.  ||  ||     /  \n'  '--'\\' '-' '\\ `--.' '-' '\\ '-'  |   |  |  \\ '-'  ||  ||  \\  \\  \n `-----' `---'  `---' `---'  `--`--'   `--'   `--`--'`--'`--'`--' ")

while True:
    name = input('이름을 정해주세요. >>')
    if name == '':
        print('공백은 쓸 수 없는 이름입니다. \n')
    else:
        break

def Receiving():
    global your_name
    while True:
        data = clientSocket.recv(1024)
        data_decoded = data.decode('utf-8')

        stok = data_decoded.split()
        if (stok[0].upper() == 'NAME'):
            if your_name=='':
                your_name = stok[1]
                print('상대방(' + serverName + ')의 이름은 ' + your_name + '입니다')
            else:
                print('상대방(' + serverName + ')의 이름이 ' + your_name + '에서 ' + stok[1] + '으로 바뀌었습니다.')
                your_name = stok[1]
        elif (stok[0].upper() == 'MSG'):
            del stok[0]
            msg = " ".join(stok)
            print('['+strftime('%H:%M:%S')+'] <' + your_name + '> : ' + msg)

def Sending():
    global name
    notification = 'NAME ' + name
    clientSocket.send(notification.encode('utf-8'))
    while True:
        send = input('')
        if send[0] == '/':
            if send[1:send.index(' ')].upper() == 'NAME':
                name = send[send.index(' ')+1:]
                send = 'NAME ' + name
                clientSocket.send(send.encode('utf-8'))
        else:
            send = 'MSG ' + send
            clientSocket.send(send.encode('utf-8'))

serverName = '127.0.0.1'
serverPort = 5123
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


threading._start_new_thread(Receiving, ())
threading._start_new_thread(Sending, ())

print(ascii_art[0] + '\n')
print('대화를 시작합니다. 이름 변경은 /name (바꿀이름) ')

while True:
    continue


