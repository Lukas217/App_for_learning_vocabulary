from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
from deep_translator import GoogleTranslator

# Window
root = Tk()
root.geometry('400x369')
root.resizable(False, False)
root.iconbitmap('images/icon_for_word_checker.ico')
root.title("Zgadnij jakie to słówko")
root.configure(background='white')


def get_words_from_excel():
    df = pd.read_excel('polskie_slowka.xlsx', sheet_name=0)  # can also index sheet by name or fetch all sheets
    words_to_guess = df['slowka_polski'].tolist()
    return words_to_guess


class LearnWordsApp:

    def __init__(self):
        self.entry_space = Entry(root)
        self.counter = 0
        self.users_words = []
        self.words_to_guess = get_words_from_excel()

        self.correct_img = ImageTk.PhotoImage(Image.open("images/ok_img_for_word_checker.jpg"))
        self.label_of_correct_img = Label(image=self.correct_img)
        self.uncorrect_img = ImageTk.PhotoImage(Image.open("images/no_img_for_word_checker.jpg"))
        self.ask_img = ImageTk.PhotoImage(Image.open("images/ask.jpg"))

        self.label = Label(image=self.ask_img)
        self.label.grid(row=5, column=1, pady=30)
        self.label.grid_rowconfigure(1, weight=1)
        self.label.grid_columnconfigure(1, weight=1)

        self.info_word = Label(root, text='Zgadnij słówko', bd=1, fg='red', bg='white', height=2)

        self.guess = Label(root, text=self.words_to_guess[self.counter], fg='black', bg='white', width=25,
                           relief=SUNKEN)
        self.guess.config(font=('Helvatical bold', 20))
        self.guess.grid(row=1, column=1)
        self.guess.grid_rowconfigure(1, weight=1)
        self.guess.grid_columnconfigure(1, weight=1)

    def info_for_user(self, announcement):
        self.info_word = Label(root, text=announcement, bd=1, fg='red', bg='white', height=2)
        self.info_word.grid(row=6, column=1, columnspan=2)
        self.info_word.grid_rowconfigure(1, weight=1)
        self.info_word.grid_columnconfigure(1, weight=1)

    def user_buttons(self):
        # Checking butto
        self.checking_button = Button(root, text="Sprawdź", command=self.checker, fg='white', bg='green', width=20,
                                      height=2)
        self.checking_button.grid(row=3, column=1, pady=15)
        self.checking_button.grid_rowconfigure(1, weight=1)
        self.checking_button.grid_columnconfigure(1, weight=1)
        # Go next button
        self.go_next_button = Button(root, text="Następne słowo ", command=self.go_next, fg='white',
                                     bg='#717171', height=2)
        self.go_next_button.grid(row=6, column=1, sticky=E)
        # Go back button
        self.go_back_button = Button(root, text="Poprzednie słowo", command=self.go_back, fg='white',
                                     bg='#717171', height=2)
        self.go_back_button.grid(row=6, column=1, sticky=W)
        # Language change button
        self.language_change_ru = Button(root, text="Rosyjski", command=self.ru_language, fg='white',
                                         bg='#717171', height=2, width=28)
        self.language_change_ru.grid(row=0, column=1, sticky=E)
        self.language_change_en = Button(root, text="Angielski", command=self.eng_language, fg='white',
                                         bg='#717171', height=2, width=28)
        self.language_change_en.grid(row=0, column=1, sticky=W)

    def user_entry_space(self):
        self.entry_space.config(font=("Helvatical bold", 20), justify='center', width=27, fg='black', bg='#C8C9CA')
        self.entry_space.insert(0, 'Wpisz słowo')
        self.entry_space.grid(row=2, column=1, columnspan=4, pady=15, sticky=W)
        self.entry_space.bind('<Button-1>', self.click)

    def ru_language(self):
        if len(self.users_words) != 0:
            self.users_words.clear()
        language_translator = 'ru'
        for i in self.words_to_guess:
            translated = GoogleTranslator(source='auto', target=language_translator).translate(i)
            self.users_words.append(translated.lower())

    def eng_language(self):
        if len(self.users_words) != 0:
            self.users_words.clear()
        language_translator = 'en'
        for i in self.words_to_guess:
            translated = GoogleTranslator(source='auto', target=language_translator).translate(i)
            self.users_words.append(translated.lower())

    def checker(self):
        try:
            if self.entry_space.get() == self.users_words[self.counter]:
                label = Label(image=self.correct_img)
                label.grid(row=5, column=1, pady=30)
                label.grid_rowconfigure(1, weight=1)
                label.grid_columnconfigure(1, weight=1)
            else:
                label = Label(image=self.uncorrect_img)
                label.grid(row=5, column=1, columnspan=2, pady=30)
                label.grid_rowconfigure(1, weight=1)
                label.grid_columnconfigure(1, weight=1)
        except IndexError:
            messagebox.showerror(title='Błąd', message='Wybierz język!!!')

    def go_next(self):
        self.entry_space.delete(0, END)
        self.info_word.destroy()
        label = Label(image=self.ask_img)
        label.grid(row=5, column=1, pady=30)
        label.grid_rowconfigure(1, weight=1)
        label.grid_columnconfigure(1, weight=1)
        if self.counter <= len(self.words_to_guess) - 2:
            print(len(self.words_to_guess))
            # print(counter)
            self.guess.destroy()
            self.counter += 1
            guess = Label(root, text=self.words_to_guess[self.counter], fg='black', bg='white', width=25)
            guess.config(font=('Helvatical bold', 20))
            guess.grid(row=1, column=1)
            guess.grid_rowconfigure(1, weight=1)
            guess.grid_columnconfigure(1, weight=1)
        else:
            info_word = Label(root, text='To jest ostatnie słówko!', bd=1, relief=SUNKEN, fg='red', bg='white',
                              height=2)
            info_word.grid(row=6, column=1, columnspan=2)
            info_word.grid_rowconfigure(1, weight=1)
            info_word.grid_columnconfigure(1, weight=1)

    def go_back(self):
        self.entry_space.delete(0, END)
        self.info_word.destroy()
        if self.counter >= 1:
            print(self.counter)
            self.guess.destroy()
            self.counter -= 1
            guess = Label(root, text=self.words_to_guess[self.counter], fg='black', bg='white', width=25, )
            guess.config(font=('Helvatical bold', 20))
            guess.grid(row=1, column=1)
            guess.grid_rowconfigure(1, weight=1)
            guess.grid_columnconfigure(1, weight=1)
        else:
            info_word = Label(root, text='To jest pierwsze słówko!', bd=1, relief=SUNKEN, fg='red', bg='white',
                              height=2)
            info_word.grid(row=6, column=1, columnspan=2)
            info_word.grid_rowconfigure(1, weight=1)
            info_word.grid_columnconfigure(1, weight=1)

    def click(self, *args):
        self.entry_space.delete(0, 'end')


a = LearnWordsApp()
a.user_entry_space()
a.user_buttons()


def on_close_ask():
    response = messagebox.askyesno('Exit', 'Na pewno chcesz wyjść z programu?')
    if response:
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close_ask)
root.mainloop()
