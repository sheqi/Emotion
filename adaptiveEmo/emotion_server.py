import socket
import pickle
import cv2
import numpy
import preprocessing
from emotion_recognition import EmotionRecognition

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65436        # The port used by the server
display = True

recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvSocket.bind((HOST, PORT))
recvSocket.listen()

network = EmotionRecognition()
network.build_network()

def result_to_emotion(result, default):
    if result is None:
        return default

    if result[0].tolist().index(max(result[0])) == 0:
        return "Smile"
    elif result[0].tolist().index(max(result[0])) == 1:
        return "Calm"
    else:
        return "Unhappy"

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def background_thread():
    while True:
        current_emotion = "unknown"
        count = 1
        conn, addr = recvSocket.accept()
        print('Connected by', addr)
        while True:
            length = recvall(conn,16)
            if not length:
                print("No data, exiting")
                break

            stringData = recvall(conn, int(length))
            if not stringData:
                print("No data, exiting")
                break
            data = numpy.fromstring(stringData, dtype='uint8')
            img=cv2.imdecode(data,1)
            if count % 5 == 0:
                result = network.predict(preprocessing.format_image(img))
                emotion_text = result_to_emotion(result, current_emotion)
                current_emotion = emotion_text
            else:
                emotion_text = current_emotion
            count += 1

            font = cv2.FONT_HERSHEY_SIMPLEX
            location = (32, 64)
            fontScale = 2
            fontColor = (0, 0, 0)
            lineType = 2
            cv2.putText(img, emotion_text, location, font, fontScale, fontColor, lineType)

            if display:
                cv2.imshow("emotion_detection", img)
                cv2.waitKey(10)

        conn.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    background_thread()
