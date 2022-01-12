from tkinter import ttk
from tkinter import Tk, PhotoImage, IntVar, Label
from tkinter.constants import END
from PIL import ImageTk, Image
from pyperclip import copy

from Generator import Generator

class App(Tk):
    def __init__(self):
        super().__init__()
        self.resizable(0, 0)
        self.title('Password Generator')
        self.geometry("282x340")
        self.columnconfigure(1, weight=2)
        self.iconphoto(False, PhotoImage(file='images/logos/logo.png'))
        self.__background = '#ecf0f1'

        self.__background_lbl = ttk.Label(self, background=self.__background)
        self.__background_lbl.place(x=0, y=0, relheight=1, relwidth=1)

        self.__title_img = ImageTk.PhotoImage(Image.open("images/others/title.png"))
        self.__title_lbl = ttk.Label(self, image=self.__title_img, background=self.__background)
        self.__title_lbl.grid(row = 0, column=0, columnspan=3, pady=15)
        self.__pwd_settings = [IntVar(),IntVar(),IntVar(),IntVar()]
        self.__len = IntVar()
        self.__len.set(8)
        self.__security_lvl = 0
        self.__password = ""

        self.__security_img =  [ImageTk.PhotoImage(Image.open("images/others/red lock.png")),
                                ImageTk.PhotoImage(Image.open("images/others/yellow lock.png")),
                                ImageTk.PhotoImage(Image.open("images/others/green lock.png")),
                                ImageTk.PhotoImage(Image.open("images/others/blue lock.png"))]

        self.__clipboard_img = ImageTk.PhotoImage(Image.open("images/others/clipboard.png").resize((18, 22), Image.ANTIALIAS))

        self.__lower_btn = ttk.Checkbutton(self,
                                           text='Lowercase',
                                           onvalue = 1,
                                           offvalue = 0,
                                           width=10,
                                           variable = self.__pwd_settings[0],
                                           command=self.calculateSecurityLvl
                                           )
        self.__upper_btn = ttk.Checkbutton(self,
                                           text = 'Uppercase',
                                           onvalue = 1,
                                           offvalue = 0,
                                           width=10,
                                           variable = self.__pwd_settings[1],
                                           command=self.calculateSecurityLvl
                                           )
        self.__num_btn = ttk.Checkbutton(self,
                                           text='Numbers  ',
                                           onvalue = 1,
                                           offvalue = 0,
                                           width=10,
                                           variable = self.__pwd_settings[2],
                                           command=self.calculateSecurityLvl
                                           )
        self.__symbols_btn = ttk.Checkbutton(self,
                                           text = 'Symbols',
                                           onvalue = 1,
                                           offvalue = 0,
                                           width=10,
                                           variable = self.__pwd_settings[3],
                                           command=self.calculateSecurityLvl
                                           )

        self.__lower_btn.grid(row=1, column=0, sticky='W', padx = 20, pady=2)
        self.__upper_btn.grid(row=2, column=0, sticky='W', padx = 20, pady=2)
        self.__num_btn.grid(row=3, column=0, sticky='W', padx = 20, pady=2)
        self.__symbols_btn.grid(row=4, column=0, sticky='W', padx = 20, pady=2)

        self.__security_img_lbl = ttk.Label(self, image = self.__security_img[self.__security_lvl], background=self.__background)
        self.__security_img_lbl.grid(row=1, column=1, rowspan=4, columnspan=2)


        self.__scale_len = ttk.Scale(self,
                                    from_=1,
                                    to=20,
                                    variable=self.__len,
                                    length=200,
                                    command=self.calculateSecurityLvl,
                                    )
        self.__len_lbl = ttk.Label(self, text = self.__len.get(), width=6, background=self.__background)
        self.__error_lbl = Label(self, text = "", width=20, background=self.__background, fg="#c0392b")
        self.__generate_btn = ttk.Button(self, text="Generate", width=20, command=self.generateFunc)
        self.__len_title = ttk.Label(self, text = "Length", width=6, background=self.__background)
        self.__pwd_view = ttk.Entry(self, width=32, font=('Arial',10), state='readonly')
        self.__copy_btn = ttk.Button(self, image=self.__clipboard_img, command=self.copyToClipboard)
        

        self.__scale_len.grid(row = 6, column=0, padx=6, columnspan=2, pady=5)
        self.__len_lbl.grid(row = 6, column=2, padx=6, columnspan=2, pady=5)
        self.__len_title.grid(row=5, column=0, columnspan=3, pady=5)
        self.__generate_btn.grid(row=7, column=0, columnspan=3, pady=5)
        self.__error_lbl.grid(row=8, column=0, columnspan=3, pady=0)
        self.__pwd_view.grid(row=9, column=0, columnspan=2, pady=5, padx=10)
        self.__copy_btn.grid(row=9, column=2, sticky='E', padx=5)


        self.__author_lbl = ttk.Label(self, text = "By Omnia Beyond™", width=18, background=self.__background)
        self.__author_lbl.grid(row=10, column=0, columnspan=3)


    def calculateSecurityLvl(self, len = 0):
        selected = 0
        len = self.__len.get()
        self.__len_lbl["text"] = len
        for x in self.__pwd_settings:
            if x.get() == 1: selected += 1
        if selected > 0: selected-=1
        if float(len) < 15 and selected >= 2: selected = 2
        if float(len) < 10 and selected >= 1: selected = 1
        if float(len) < 5: selected = 0
        self.__security_img_lbl.configure(image=self.__security_img[selected])
        self.__security_img_lbl.image = self.__security_img[selected]

    
    def generateFunc(self):
        selected = 0
        for x in self.__pwd_settings:
            if x.get() == 1: selected += 1

        if selected == 0:
            self.__error_lbl["text"] = "Select at least one field"
            return
        else: self.__error_lbl["text"] = ""

        generator = Generator(self.__len.get(), [i.get() for i in self.__pwd_settings])
        self.__password = generator.generatePwd()

        self.__pwd_view["state"] = "active"
        self.__pwd_view.delete(0, END)
        self.__pwd_view.insert(0, self.__password)
        self.__pwd_view["state"] = "readonly"


    def copyToClipboard(self):
        if(self.__password != ""): copy(self.__password)