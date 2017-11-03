from socket import *
from time import strftime
import threading

ascii_art = []
ascii_art.append("                                                                  \n ,-----.                            ,--------.       ,--.,--.     \n'  .--./ ,---.  ,---. ,---.  ,--,--.'--.  .--',--,--.|  ||  |,-.  \n|  |    | .-. || .--'| .-. |' ,-.  |   |  |  ' ,-.  ||  ||     /  \n'  '--'\\' '-' '\\ `--.' '-' '\\ '-'  |   |  |  \\ '-'  ||  ||  \\  \\  \n `-----' `---'  `---' `---'  `--`--'   `--'   `--`--'`--'`--'`--' ")
serverPort = 5123
BUFSIZE = 1024

name = ''
your_name = ''

while True:
    name = input('이름을 정해주세요. >>')
    if name=='':
        print('공백은 쓸 수 없는 이름입니다. \n')
    else:
        break

print('접속을 대기합니다')

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()

print('준비 완료')
print('connected by', addr)




def Receiving():
    global your_name
    global addr

    while True:
        data = connectionSocket.recv(1024)
        data_decoded = data.decode('utf-8')

        stok = data_decoded.split()
        if (stok[0].upper() == 'NAME'):
            if your_name=='':
                your_name = stok[1]
                print('상대방의 이름은 ' + your_name + '입니다')
            else:
                print('상대방의 이름이 ' + your_name + '에서 ' + stok[1] + '으로 바뀌었습니다.')
                your_name = stok[1]
        elif (stok[0].upper() == 'MSG'):
            del stok[0]
            msg = " ".join(stok)
            print('[' + strftime('%H:%M:%S')+'] <' + your_name + '> : ' + msg)



def Sending():
    notification = 'NAME ' + name
    connectionSocket.send(notification.encode('utf-8'))
    while True:
        send = input('')
        if send[0] == '/':
            if send[1:send.index(' ')].upper() == 'NAME':
                name = send[send.index(' ')+1:]
                send = 'NAME ' + name
                connectionSocket.send(send.encode('utf-8'))
        else:
            send = 'MSG ' + send
            connectionSocket.send(send.encode('utf-8'))
        

threading._start_new_thread(Receiving, ())
threading._start_new_thread(Sending,())

print(ascii_art[0] + '\n')
print('대화를 시작합니다. 이름 변경은 /name (바꿀이름) ')

while True:
    continue



    
