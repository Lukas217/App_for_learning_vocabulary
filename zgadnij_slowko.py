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

df = pd.read_excel('polskie_slowka.xlsx', sheet_name=0)  # can also index sheet by name or fetch all sheets
words_to_guess = df['slowka_polski'].tolist()
answers_russian = []

# Choosing language

def ru_language():
    if len(answers_russian) != 0:
        answers_russian.clear()
    language_translator = 'ru'
    for i in words_to_guess:
        translated = GoogleTranslator(source='auto', target=language_translator).translate(i)
        answers_russian.append(translated.lower())

    print(answers_russian)


def eng_language():
    if len(answers_russian) != 0:
        answers_russian.clear()
    language_translator = 'en'
    for i in words_to_guess:
        translated = GoogleTranslator(source='auto', target=language_translator).translate(i)
        answers_russian.append(translated.lower())


correct_img = ImageTk.PhotoImage(Image.open("images/ok_img_for_word_checker.jpg"))
label_of_correct_img = Label(image=correct_img)
uncorrect_img = ImageTk.PhotoImage(Image.open("images/no_img_for_word_checker.jpg"))
ask_img = ImageTk.PhotoImage(Image.open("images/ask.jpg"))

label = Label(image=ask_img)
label.grid(row=5, column=1, pady=30)
label.grid_rowconfigure(1, weight=1)
label.grid_columnconfigure(1, weight=1)

counter = 0

guess = Label(root, text=words_to_guess[counter], fg='black', bg='white', width=25, relief=SUNKEN)
guess.config(font=('Helvatical bold', 20))
guess.grid(row=1, column=1)
guess.grid_rowconfigure(1, weight=1)
guess.grid_columnconfigure(1, weight=1)

info_word = Label(root, text='Zgadnij słówko!', bd=1, fg='red', bg='white', height=2)
info_word.grid(row=6, column=1, columnspan=2)
info_word.grid_rowconfigure(1, weight=1)
info_word.grid_columnconfigure(1, weight=1)


def checker():
    global counter
    try:
        if entry_space.get() == answers_russian[counter]:
            label = Label(image=correct_img)
            label.grid(row=5, column=1, pady=30)
            label.grid_rowconfigure(1, weight=1)
            label.grid_columnconfigure(1, weight=1)
        else:
            label = Label(image=uncorrect_img)
            label.grid(row=5, column=1, columnspan=2, pady=30)
            label.grid_rowconfigure(1, weight=1)
            label.grid_columnconfigure(1, weight=1)
    except IndexError:
        messagebox.showerror(title='Błąd', message='Wybierz język!!!')


def go_next():
    global counter, guess, info_word
    entry_space.delete(0, END)
    info_word.destroy()
    label = Label(image=ask_img)
    label.grid(row=5, column=1, pady=30)
    label.grid_rowconfigure(1, weight=1)
    label.grid_columnconfigure(1, weight=1)
    if counter <= len(words_to_guess) - 2:
        print(len(words_to_guess))
        # print(counter)
        guess.destroy()
        counter += 1
        guess = Label(root, text=words_to_guess[counter], fg='black', bg='white', width=25, )
        guess.config(font=('Helvatical bold', 20))
        guess.grid(row=1, column=1)
        guess.grid_rowconfigure(1, weight=1)
        guess.grid_columnconfigure(1, weight=1)

    else:
        info_word = Label(root, text='To jest ostatnie słówko!', bd=1, relief=SUNKEN, fg='red', bg='white', height=2)
        info_word.grid(row=6, column=1, columnspan=2)
        info_word.grid_rowconfigure(1, weight=1)
        info_word.grid_columnconfigure(1, weight=1)


def go_back():
    global counter, guess, info_word
    entry_space.delete(0, END)
    info_word.destroy()
    if counter >= 1:
        print(counter)
        guess.destroy()
        counter -= 1
        guess = Label(root, text=words_to_guess[counter], fg='black', bg='white', width=25, )
        guess.config(font=('Helvatical bold', 20))
        guess.grid(row=1, column=1)
        guess.grid_rowconfigure(1, weight=1)
        guess.grid_columnconfigure(1, weight=1)
    else:
        info_word = Label(root, text='To jest pierwsze słówko!', bd=1, relief=SUNKEN, fg='red', bg='white', height=2)
        info_word.grid(row=6, column=1, columnspan=2)
        info_word.grid_rowconfigure(1, weight=1)
        info_word.grid_columnconfigure(1, weight=1)


def click(*args):
    entry_space.delete(0, 'end')


def on_close():
    response = messagebox.askyesno('Exit', 'Na pewno chcesz wyjść z programu?')
    if response:
        root.destroy()


root.protocol('WM_DELETE_WINDOW', on_close)

entry_space = Entry(root)
entry_space.config(font=("Helvatical bold", 20), justify='center', width=27, fg='black', bg='#C8C9CA')
entry_space.insert(0, 'Wpisz słowo')
entry_space.grid(row=2, column=1, columnspan=4, pady=15, sticky=W)
entry_space.bind('<Button-1>', click)

# Checking butto
checking_button = Button(root, text="Sprawdź", command=checker, fg='white', bg='green', width=20, height=2)
checking_button.grid(row=3, column=1, pady=15)
checking_button.grid_rowconfigure(1, weight=1)
checking_button.grid_columnconfigure(1, weight=1)
# Go next button
go_next_button = Button(root, text="Następne słowo ", command=go_next, fg='white', bg='#717171', height=2)
go_next_button.grid(row=6, column=1, sticky=E)
# Go back button
go_back_button = Button(root, text="Poprzednie słowo", command=go_back, fg='white', bg='#717171', height=2)
go_back_button.grid(row=6, column=1, sticky=W)
# Language change button
language_change_ru = Button(root, text="Rosyjski", command=ru_language, fg='white', bg='#717171', height=2, width=28)
language_change_ru.grid(row=0, column=1, sticky=E)
language_change_en = Button(root, text="Angielski", command=eng_language, fg='white', bg='#717171', height=2, width=28)
language_change_en.grid(row=0, column=1, sticky=W)

root.mainloop()
