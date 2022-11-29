import cv2
import os
import sqlite3, time

conn = sqlite3.connect('FACES.db')
cur = conn.cursor()





#cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(r'C:\Users\yush-student\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')


#Получаем последний id

try:
     cur.execute("""SELECT userid FROM faces ORDER BY userid DESC LIMIT 1""")
     u_id = cur.fetchone()[0]
except TypeError:
     u_id = -1


#запускаем цикл
for i in range(4):
     # Вводим id лица которое добавляется в имя и потом будет использовать в распознавание.
     u_id += 1
     face_id = u_id
     name = input('Введите имя  ==>  ')
     cur.execute("""INSERT INTO faces(userid, name) 
                       VALUES(?, ?);""", (face_id, name))
     conn.commit()
     
     print("\n [INFO] Инициализируем камеру, подожите …")
     time.sleep(1)
     count = 0
     while(True):
          ret, img = cam.read()  
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          faces = face_detector.detectMultiScale(gray, 1.3, 5)
          for (x,y,w,h) in faces:     
               cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
               count += 1     
               # Сохраняем лицо
               cv2.imwrite('face/user.' + str(face_id) + '.' + str(count) + '.jpg', gray[y:y+h,x:x+w])
               cv2.imshow('image', img); k = cv2.waitKey(100) & 0xff #  'ESC'

          if count >= 30: # Если сохранили 30 изображений выход.
              break
     print("\n [INFO] Заносите нового")
print('Конец')
cam.release()
cv2.destroyAllWindows()
cur.close()
conn.close()

