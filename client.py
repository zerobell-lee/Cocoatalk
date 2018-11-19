from socket import *
from time import strftime
import threading
import time

# 내 이름과 상대방 이름 변수 초기화 (string type)
name = ''
your_name = ''


# 코코아톡 그림을 그리기 위한 string list.
ascii_art = []
ascii_art.append("                                                                  \n ,-----.                            ,--------.       ,--.,--.     \n'  .--./ ,---.  ,---. ,---.  ,--,--.'--.  .--',--,--.|  ||  |,-.  \n|  |    | .-. || .--'| .-. |' ,-.  |   |  |  ' ,-.  ||  ||     /  \n'  '--'\\' '-' '\\ `--.' '-' '\\ '-'  |   |  |  \\ '-'  ||  ||  \\  \\  \n `-----' `---'  `---' `---'  `--`--'   `--'   `--`--'`--'`--'`--' ")

serverName = ''
serverPort = 0

serverName = input('접속하고자 하는 IP를 입력해주세요 >>')
serverPort = int(input('사용하고자 하는 Port를 입력해주세요 >>'))



while True:
    # 공백 이외의 이름을 쓸 때까지 무한 루프
    name = input('이름을 정해주세요. >>')
    if name == '':
        print('공백은 쓸 수 없는 이름입니다. \n')
    else:
        break

fileMode = False

def Receiving():
    global your_name
    global fileMode
    global fileName

    while True:
        #소켓으로부터 1024 byte의 입력을 대기. recv는 입력 완료 때까지 계속 기다린다.
        try:
            data = clientSocket.recv(1024)
            if fileMode:
                try:
                    if data.decode('utf-8').rstrip().upper() == 'FILE END':
                        fp.close()
                        fileMode = False
                        print('Completed!!')
                    else:
                        fp.write(data)
                except UnicodeError:
                    fp.write(data)

            else:
                #byte로 전송된 data를 utf-8 형식으로 다시 디코딩
                if data:
                    data_decoded = data.decode('utf-8')
                    #프로토콜 분석을 위하여 data_decoded를 공백으로 분리한다.
                    stok = data_decoded.split()
                    if (stok[0].upper() == 'NAME'):
                        #만일 프로토콜이 'NAME' 프로토콜이라면
                        if your_name=='':
                            your_name = stok[1]
                            print('상대방(' + serverName + ')의 이름은 ' + your_name + '입니다')
                            #만일 상대방이 처음으로 NAME 프로토콜을 전송한 경우라면, 위와 같이 처리한다.
                        else:
                            print('상대방(' + serverName + ')의 이름이 ' + your_name + '에서 ' + stok[1] + '으로 바뀌었습니다.')
                            your_name = stok[1]
                            #대화 중에 NAME 프로토콜을 전송한 경우라면, 상대방의 이름을 변경하는 메시지를 표시한다.
                    elif (stok[0].upper() == 'MSG'):
                        #만일 프로토콜이 'MSG' 프로토콜이라면
                        del stok[0]
                        msg = " ".join(stok)
                        print('['+strftime('%H:%M:%S')+'] <' + your_name + '> : ' + msg)
                        #그 이후에 나오는 메시지를 전부 [timestamp] <your_name> : message 형식으로 print 한다.
                    elif stok[0].upper() == 'FILE':
                        if stok[1].upper() == 'START':
                            fileName = stok[2]
                            fp = open(fileName, 'wb')
                            fileMode = True
                            print('Establishing File Transfer...')
        except ConnectionResetError:
            print('상대방이 나갔습니다.')
            exit(-1)

    clientSocket.close() #소켓을 닫는다. 정상적으로는 실행될 일 없음.

def Sending():
    global name
    notification = 'NAME ' + name
    clientSocket.send(notification.encode('utf-8'))
    #첫 연결이 되었을 때, 자신의 이름을 NAME 프로토콜로 알리도록 한다.
    while True:
        send = input('')
        if send=='':
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
                    clientSocket.send(send.encode('utf-8'))
                    print('이름이 ' + name + '으로 변경되었습니다.')
                    #NAME 프로토콜을 전송 후 print를 띄움.​
            elif stok[0][1:].upper() == 'EXIT':
                clientSocket.close() #소켓을 종료합니다.
            elif stok[0][1:].upper() == 'SEND':
                filePath = stok[1]
                fileName = filePath.split('/')[-1]

                send = 'FILE START ' + fileName

                print('Establishing File Transfer...')
                clientSocket.send(send.encode('utf-8'))
                fp = open(filePath, 'rb')
                sendB = fp.read(1024)
                while len(sendB) > 0:
                    clientSocket.send(sendB)
                    sendB = fp.read(1024)

                time.sleep(0.5)
                send = 'FILE END'
                clientSocket.send(send.encode('utf-8'))

                fp.close()
                print('Completed!!')
            else:
                print('Undefined Function!!!') #NAME, EXIT 이외의 명령어는 모르는 명령어입니다.
        else:
            send = 'MSG ' + send
            clientSocket.send(send.encode('utf-8'))
            #그 외는 전부 메시지로 처리하여 전송한다. utf-8로 encoding 하여 전송한다.


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#서버 이름과 포트를 연결

threading._start_new_thread(Receiving, ())
threading._start_new_thread(Sending, ())

print(ascii_art[0] + '\n')
print('대화를 시작합니다. 이름 변경은 /name (바꿀이름) 종료는 /exit')

#첫 대화 시작시 메시지 표시.

while True:
    continue

#파이썬은 끝 줄을 만나면 종료되므로 while문으로 무한루프 시키도록 한다.

