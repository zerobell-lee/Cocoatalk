from socket import *
from time import strftime
import threading

#주석은 client.py를 참조하세요.

ascii_art = []
ascii_art.append("                                                                  \n ,-----.                            ,--------.       ,--.,--.     \n'  .--./ ,---.  ,---. ,---.  ,--,--.'--.  .--',--,--.|  ||  |,-.  \n|  |    | .-. || .--'| .-. |' ,-.  |   |  |  ' ,-.  ||  ||     /  \n'  '--'\\' '-' '\\ `--.' '-' '\\ '-'  |   |  |  \\ '-'  ||  ||  \\  \\  \n `-----' `---'  `---' `---'  `--`--'   `--'   `--`--'`--'`--'`--' ")
serverPort = 5124
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
fileMode = False
fileName = ''

#서버소켓을 바인드

print('준비 완료')
print('connected by', addr)




def Receiving():
    global your_name
    global addr
    global fileMode
    global fileName

    while True:
        data = connectionSocket.recv(1024)
        # byte로 전송된 data를 utf-8 형식으로 다시 디코딩
        try:
            data_decoded = data.decode('utf-8')
            if data:
                # 프로토콜 분석을 위하여 data_decoded를 공백으로 분리한다.
                stok = data_decoded.split()
                if (stok[0].upper() == 'NAME'):
                    # 만일 프로토콜이 'NAME' 프로토콜이라면
                    if your_name == '':
                        your_name = stok[1]
                        print('상대방(' + str(addr[0]) + ')의 이름은 ' + your_name + '입니다')
                        # 만일 상대방이 처음으로 NAME 프로토콜을 전송한 경우라면, 위와 같이 처리한다.
                    else:
                        print('상대방(' + str(addr[0]) + ')의 이름이 ' + your_name + '에서 ' + stok[1] + '으로 바뀌었습니다.')
                        your_name = stok[1]
                        # 대화 중에 NAME 프로토콜을 전송한 경우라면, 상대방의 이름을 변경하는 메시지를 표시한다.
                elif (stok[0].upper() == 'MSG'):
                    # 만일 프로토콜이 'MSG' 프로토콜이라면
                    del stok[0]
                    msg = " ".join(stok)
                    print('[' + strftime('%H:%M:%S') + '] <' + your_name + '> : ' + msg)
                    # 그 이후에 나오는 메시지를 전부 [timestamp] <your_name> : message 형식으로 print 한다.
                elif stok[0].upper() == 'FILE':
                    if stok[1].upper() == 'START':
                        fileName = stok[2]
                        fp = open(fileName, 'wb')
                        fileMode = True
                    elif stok[1].upper() == 'END':
                        fp.close()
                        fileMode = False
        except:
            if fileMode:
                fp.write(data)

    connectionSocket.close()

def Sending():
    global name
    notification = 'NAME ' + name
    connectionSocket.send(notification.encode('utf-8'))
    while True:
        send = input('')
        if (send==''):
            continue
        if send[0] == '/':
            #만일 '/'로 시작하는 메시지라면, 명령어로서 처리하도록 한다.
            stok = send.split()
            if stok[0][1:].upper() == 'NAME':
                #이름을 바꾸는 /name 명령어라면, 이름 변경 명령을 실행
                if len(stok) != 2:
                    print('[Warning] 이름이 정의되지 않았거나, 두 어절 이상입니다!!')
                else:
                    name = stok[1]
                    send = 'NAME ' + name
                    connectionSocket.send(send.encode('utf-8'))
                    print('이름이 ' + name + '으로 변경되었습니다.')
                    #NAME 프로토콜을 전송 후 print를 띄움.
            elif stok[0][1:].upper() == 'EXIT':
                connectionSocket.close() #소켓을 종료합니다.
            else:
                print('Undefined Function!!!')  # NAME 이외의 명령어는 모르는 명령어입니다.
        else:
            send = 'MSG ' + send
            connectionSocket.send(send.encode('utf-8'))
        

threading._start_new_thread(Receiving, ())
threading._start_new_thread(Sending,())

print(ascii_art[0] + '\n')
print('대화를 시작합니다. 이름 변경은 /name (바꿀이름) 종료는 /exit')

while True:
    continue


