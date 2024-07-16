from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from table import Table, Pharmacist

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("1100x600")
        self.create_main_view()
        self.resizable(width=False, height=False)

    def create_main_view(self):
        self.clear_window()
        self.title("PharmAssist")

        # Load images
        title_image = ImageTk.PhotoImage(Image.open("title.png"))
        left_pill = Image.open("left_pill.png")
        right_pill = Image.open("right_pill.png")

        # Create labels for images
        label_title = Label(self, image=title_image)
        label_title.image = title_image

        # Function to darken image on hover
        def darken_image(image_path):
            img = Image.open(image_path)
            img = img.point(lambda p: p * 0.7)  # Darken the image by 30%
            return ImageTk.PhotoImage(img)

        left_pill_normal = ImageTk.PhotoImage(left_pill)
        left_pill_hover = darken_image("left_pill.png")

        right_pill_normal = ImageTk.PhotoImage(right_pill)
        right_pill_hover = darken_image("right_pill.png")

        # Create buttons with images
        student_button = Button(self, image=left_pill_normal, borderwidth=0,
                         command=lambda: self.student_view("Button 1"))
        student_button.image = left_pill_normal  # Keep a reference to avoid garbage collection
        student_button.bind("<Enter>", lambda e: student_button.config(image=left_pill_hover))
        student_button.bind("<Leave>", lambda e: student_button.config(image=left_pill_normal))
        student_button.place(x=(555 - 200), y=300)

        pharmacist_button = Button(self, image=right_pill_normal, borderwidth=0,
                         command=self.create_login_view)
        pharmacist_button.image = right_pill_normal  # Keep a reference to avoid garbage collection
        pharmacist_button.bind("<Enter>", lambda e: pharmacist_button.config(image=right_pill_hover))
        pharmacist_button.bind("<Leave>", lambda e: pharmacist_button.config(image=right_pill_normal))
        pharmacist_button.place(x = 555, y=300)

        # Place the title image
        label_title.place(x=(1100 - 666) // 2, y=0)

    def student_view(self, button_name):
        self.clear_window()
        self.title(button_name)

        student = Table(self)

        back_button = Button(self, text="Back", command=self.create_main_view, width=10)
        back_button.place(x=20, y=360)

    def create_login_view(self):
        self.clear_window()
        self.title("Login")
        self.geometry("1100x600")
        # self.configure(bg="#9fc4cb")

        frame = Frame(self, bg="#d9f4f1", bd=2, relief=SOLID, padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        label_title = Label(frame, bg="#d9f4f1", text="LOGIN", width=15, font=("bold", 15))
        label_title.grid(row=0, columnspan=2, pady=10)

        label_id = Label(frame, text="Faculty ID:", bg="#d9f4f1")
        label_id.grid(row=1, column=0, sticky=W, pady=10)
        self.entry_id = Entry(frame)
        self.entry_id.grid(row=1, column=1, pady=5)

        label_password = Label(frame, text="Password:", bg="#d9f4f1")
        label_password.grid(row=2, column=0, sticky=W, pady=10)
        self.entry_password = Entry(frame, show="*")
        self.entry_password.grid(row=2, column=1, pady=5)

        show_password_var = IntVar()
        show_password_check = Checkbutton(frame, text="Show Password", variable=show_password_var,command=lambda: self.toggle_password_visibility(self.entry_password, show_password_var),bg="#d9f4f1")
        show_password_check.grid(row=3, columnspan=2, pady=10)
        # print(self.entry_password.get())
        login_button = Button(frame, text="Login", command=lambda: self.check_credentials(self.entry_id.get(), self.entry_password.get()), bg="#b5e0de", fg="black")
        login_button.grid(row=4, columnspan=2, pady=10)

        back_button = Button(self, text="Home", command=self.create_main_view, width=10)
        back_button.place(x=10, y=10)

    def toggle_password_visibility(self, entry, var):
        if var.get():
            entry.config(show="")
        else:
            entry.config(show="*")

    def check_credentials(self, faculty_id, password):
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE faculty_id=? AND password=?", (faculty_id, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.clear_window()
            Pharmacist(self)
            back_button = Button(self, text="Home", command=self.create_main_view, width=10)
            back_button.place(x=750, y=481)

        else:
            error_label = Label(self, text="Invalid Credentials", fg="red")
            error_label.pack(pady=10)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()