from tkinter import *
from face_saving import start_photo
from ml_script import recong_start
from recognition_script import start

root = Tk()
root.title("Обучение системы компьютерного зрения")
root.geometry("400x600")


label_photo = Label(text="1. Сфотографируйте пользователей", font=("Arial", 16))
button_photo = Button(text="Начать фото", font=("Arial", 16), command=start_photo)
label_ml = Label(text="2. Начните обучение", font=("Arial", 16))
button_ml = Button(text="Обучить", font=("Arial", 16),command=recong_start)
label_start = Label(text="3. Распознать", font=("Arial", 16))
button_start = Button(text="Распознать", font=("Arial", 16),command=start)
label_photo.pack(pady=20)
button_photo.pack(pady=20)
label_ml.pack(pady=20)
button_ml.pack(pady=20)
label_start.pack(pady=20)
button_start.pack(pady=20)

root.mainloop()