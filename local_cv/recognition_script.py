import cv2
import numpy as np
import os
import sqlite3
from datetime import datetime
def start():
    print('Запущено')
    #Список пришедших
    # coming_list = []
    with open("names.txt") as f:
        names= f.readlines()

    # conn = sqlite3.connect('FACES.db')
    # cur = conn.cursor()



    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face.yml')
    faceCascade = cv2.CascadeClassifier(r'venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    # Тип шрифта
    font = cv2.FONT_HERSHEY_COMPLEX

    # iniciate id counter
    id = 0

    # Список имен для id
    # cur.execute("SELECT userid, name FROM faces;")
    # names = dict(cur.fetchall())


    cam = cv2.VideoCapture(0)
    cam.set(3, 800)  # set video width
    cam.set(4, 600)  # set video height

    #Получаем последний id

    # try:
    #     # cur.execute("""SELECT att_id FROM attend3 ORDER BY att_id DESC LIMIT 1""")
    #     # bbbb = cur.fetchone()[0]+1
    # except TypeError:
    #     bbbb  = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(10, 10),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # Проверяем что лицо распознано
            if (confidence < 100):
                #если человек уже проходил, пропускаем
                # if id in coming_list:
                #     pass
                # else:
                #     #если нет, пишем в список пришедших
                #     coming_list += [id]
                #     #определяем дату
                #     today = datetime.now()
                    #пишем в БД
                    #проверка, есть ли ужее запись с этим пользователем на этот день (вдруг в id не было)
                    # try:
                    #     cur.execute('SELECT date FROM attend3 WHERE userid=? ORDER BY date DESC LIMIT 1;', (id,))
                    #     dt = cur.fetchone()[0][:11]
                    #     dn = str(today)[:11]
                    #     if dt == dn:
                    #         continue

                    # except:
                    #     cur.execute('INSERT INTO attend3 (att_id, userid, date) VALUES (?, ?, ?) ;', (bbbb, id, today))
                    #     bbbb += 1
                    #     conn.commit()
                name = names[id]
                # это можно убрать
                # print(name, 'пришел')
                # print(coming_list)
            else:
                name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # 'ESC' для Выхода
        if k == 27:
            break
    # cur.execute('SELECT * FROM attend3 ORDER BY att_id;')
    # print(cur.fetchall())
    cam.release()
    cv2.destroyAllWindows()
