import csv
import os
import tkinter as tk
from tkinter import *
import subprocess
from tkinter import ttk, filedialog

import face_recognition
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
import util  # defined window components
import cv2
from glob import glob
from csv import writer
from pandas import pandas as pd
class App:
    def __init__(self):

        self.main_window = tk.Tk()  # main_window = mainframe
        self.main_window.geometry("1200x500+150+100")  # window width x height + x + y
        self.admin_button = util.get_button(self.main_window, "admin", "black", self.admin)  # login button component
        self.admin_button.place(x=750, y=270)  # login button location within the window
        self.login_button = util.get_button(self.main_window, "login", "red", self.login, )
        self.login_button.place(x=750, y=340)  # login button location within the window

        self.register_button = util.get_button(self.main_window, "register", "green", self.register,
                                               fg="black")  # register button component
        self.register_button.place(x=750, y=400)

        self.project_title = util.get_text_label(self.main_window, 'FACE RECOGNITION\nATTENDANCE SYSTEM')
        self.project_title.place(x=770, y=100)

        self.login_guide = util.get_text_label2(self.main_window, 'LOOK STRAIGHT CLOSE TO THE CAMERA AND CLICK')
        self.login_guide.place(x=760, y=250)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=750, height=500)



        ###################################

        self.add_webcam(self.webcam_label)

        self.db_image_dir = 'db/known_face_names'
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self, img=None):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame,1)
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  # convert color
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)


    def register(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x500+270+120")

        self.accept_register_button = util.get_button(self.register_window, "Accept", "green", self.accept_register)
        self.accept_register_button.place(x=750, y=300)

        self.try_again_register_button = util.get_button(self.register_window, "Try again", 'red', self.try_again_register)
        self.try_again_register_button.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_user = util.get_entry_text(self.register_window)
        self.entry_text_register_user.place(x=750, y=200)

        self.text_label_register = util.get_text_label(self.register_window, 'Please input your full name: ')
        self.text_label_register.place(x=750, y=150)

        # db directory
        self.db_dir = 'db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
    def view_sheet(self):
        self.admin_login_window.destroy()
        self.view_sheet_window = tk.Toplevel(self.main_window)
        self.view_sheet_window.geometry("1200x500+150+100")
        self.view_sheet_window.title("ATTENDANCE")

        self.myframe = Frame(self.view_sheet_window)
        self.myframe.pack(pady=20)
        self.my_tree = ttk.Treeview(self.view_sheet_window)
        self.my_menu = Menu(self.view_sheet_window)
        self.view_sheet_window.config(menu=self.my_menu)

        self.file_menu = Menu(self.my_menu)

        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label = "Spreadsheets", menu= self.file_menu)
        self.file_menu.add_command(label="Open", command = self.file_open)
        self.my_label = Label(self.view_sheet_window, text='')
        self.my_label.pack(pady=20)

        self.name_label = util.get_text_label2(self.view_sheet_window, "Name")
        self.name_label.place(x=380, y=70)

        self.time_label = util.get_text_label2(self.view_sheet_window, "Time Log")
        self.time_label.place(x=580, y=70)
        self.date_label = util.get_text_label2(self.view_sheet_window, "Date Log")
        self.date_label.place(x=750, y=70)
    def file_open(self):
        self.filename = filedialog.askopenfilename(
            initialdir="C://Users//JAYTHER JANN//OneDrive//Desktop//faceRecognition//tkFacerec",
            title= "Open A file",
            filetype=(("csv files", "*.csv"), ("All Files", "*.*" ))
        )
        if self.filename:
            try:
                self.filename = r"{}".format(self.filename)
                self.df = pd.read_csv(self.filename)
            except ValueError:
                self.my_label.config(text="File Coudn't be opened...Try Again")
            except FileNotFoundError:
                self.my_label.config(text="File Coudn't be opened...Try Again")
            #clear old tree
            self.clear_tree()
            #Set up new treeview
            self.my_tree["column"] = list(self.df.columns)
            self.my_tree["show"] = "headings"

            #Loop through column lists
            for column in self.my_tree["column"]:
                self.my_tree.heading(column, text=column)

            #Put data in tree view
            self.df_rows = self.df.to_numpy().tolist()
            for row in self.df_rows:
                self.my_tree.insert("", "end", values=row)

            self.my_tree.pack()
            self.view_sheet_window.lift()

    def clear_tree(self):
        self.my_tree.delete(*self.my_tree.get_children())


    def admin(self):
        self.admin_login_window = tk.Toplevel(self.main_window)
        self.admin_login_window.geometry("1200x500+150+100")

        self.login_admin_button = util.get_button(self.admin_login_window, "Login", "green", self.admin_login)
        self.login_admin_button.place(x=750, y=300)

        self.entry_text_register_user2 = util.get_entry_text2(self.admin_login_window)
        self.entry_text_register_user2.place(x=750, y=200)

        self.text_label_register2 = util.get_text_label(self.admin_login_window, 'ENTER PASSWORD: ')
        self.text_label_register2.place(x=750, y=150)
        self.capture_label2 = util.get_img_label(self.admin_login_window)
        self.capture_label2.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label2)
        unknown_img_path = "./tmp.jpg"
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_image_dir, unknown_img_path]))
        name_unknown = output.split(',')[1][:-6]

        if name_unknown in ['unknown_person', 'no_persons_found']:
            util.msg_box("Oops!", "Not recognized as Admin")
        else:
            known_face_encoding = []
            known_faces_names = []
            images = []
            photos = glob('db/admin/*.jpg')
            face_locations = []
            face_encodings = []
            face_names = []

            for img in photos:
                images.append(face_recognition.load_image_file(img))
            for loaded_img in images:
                known_face_encoding.append(face_recognition.face_encodings(loaded_img)[0])

            for known_face in photos:
                filename = os.path.split(known_face)[1]
                face_name = filename.split(".")
                known_faces_names.append(face_name[0])

            print(known_faces_names)
            students = known_faces_names.copy()

            face_locations = face_recognition.face_locations(self.most_recent_capture_arr)
            face_encodings = face_recognition.face_encodings(self.most_recent_capture_arr, face_locations)
            faces_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]
                    util.msg_box("PASSWORD", "Hi, Admin "+name+ "\nENTER PASSWORD TO PROCEED")
                    self.admin_login_window.lift()
        os.remove(unknown_img_path)
    def admin_login(self):
        entered_pass = self.entry_text_register_user2.get()
        if entered_pass == "admin123" :
            self.view_sheet()
        else:
            util.msg_box("Invalid", "Password Incorrect!")
    def login(self):
        now = datetime.now()

        current_date = now.strftime("%Y-%m-%d")
        unknown_img_path = "./.tmp.jpg"
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_image_dir, unknown_img_path]))
        name_unknown = output.split(',')[1][:-5]

        current_time = now.strftime("%H : %M")
        current_day = now.strftime("%d")
        current_month = now.strftime("%m")
        current_year = now.strftime("%Y")

        int_month = None
        month_now = ""
        month = ["", "January", "February", "March", "April", "May", "June", "July", "August",
                 "September", "October", "November", "December"]
        if current_month[0] == str(0):
            int_month = int(current_month[1])
            month_now = month[int_month]
        else:
            int_month = int(current_month)
            month_now = month[int_month]
        if name_unknown in ['unknown_person', 'no_persons_found']:
            util.msg_box("Oops!", "Unknown User, Please Register new User or try again")
        else:
            known_face_encoding = []
            known_faces_names = []
            images = []
            photos = glob('db/known_face_names/*.jpg')
            face_locations = []
            face_encodings = []
            face_names = []

            for img in photos:
                images.append(face_recognition.load_image_file(img))
            for loaded_img in images:
                known_face_encoding.append(face_recognition.face_encodings(loaded_img)[0])

            for known_face in photos:
                filename = os.path.split(known_face)[1]
                face_name = filename.split(".")
                known_faces_names.append(face_name[0])

            print(known_faces_names)
            students = known_faces_names.copy()

            face_locations = face_recognition.face_locations(self.most_recent_capture_arr)
            face_encodings = face_recognition.face_encodings(self.most_recent_capture_arr, face_locations)
            faces_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]

                faces_names.append(name)
                if name in known_faces_names:
                    if name in students:
                        students.remove(name)
                        print(name + ": PRESENT")
                        print(str(students) + ": CURRENTLY NOT PRESENT")
                        csv_file_path = glob("*.csv")
                        csv_files = []
                        for i in csv_file_path:
                            csv_files.append(i+".csv")
                        if current_year+", "+ month_now+" "+current_day+".csv" not in csv_files:
                            f = open(current_year+", "+ month_now+" "+current_day+".csv", "w")
                            lnwriter = csv.writer(f)
                            lnwriter.writerow([name, current_time,current_year+", "+ month_now+" "+current_day])
                            util.msg_box("Welcome",name+" Attendance Saved at "+ current_time+ " | "+" "+current_year+", "+ month_now+" "+current_day)

                        else:
                            with open(current_date+".csv", "a") as f:
                                w_object = writer(f)
                                w_object.writerow([name,current_time,current_year+", "+ month_now+" "+current_day])
                                util.msg_box("Welcome",name+" Attendance Saved at " + " | "+" "+current_year+", " + month_now+" "+current_day)
        os.remove(unknown_img_path)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_capture = self.most_recent_capture_arr.copy()

    def accept_register(self):

        name = self.entry_text_register_user.get(1.0, "end-1c")  # get entered text in the text field.

        cv2.imwrite(os.path.join(self.db_image_dir, '{}.jpg'.format(name)), self.register_capture)

        self.register_window.destroy()

        util.msg_box('Success!', 'Registered Successfully!')
    def try_again_register(self):
        self.register_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()

