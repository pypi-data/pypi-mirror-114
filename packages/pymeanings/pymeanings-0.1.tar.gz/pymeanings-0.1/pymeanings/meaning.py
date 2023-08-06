import subprocess
from PyDictionary import PyDictionary
from tkinter import Tk, messagebox
import sys

def find_meaning():
    Tk().withdraw()

    # get the currently selected text
    input_text = subprocess.check_output('xsel -o', shell = True)
    input_text = input_text.decode("UTF-8")

    if not input_text:
        messagebox.showerror("Error", "Please select word for finding meaning")
        sys.exit(1)

    # get meanings from PyDictionary
    dictionary = PyDictionary()
    meaning = dictionary.meaning(input_text)

    if meaning is None:
        messagebox.showerror("Error", f"Can't find meaning of '{input_text}' \nCheck your internet connection or the word you selected might not mean anything!!")
        sys.exit(1)

    # changing the meaning to a more friendly user output
    meanings = []
    for part in list(meaning.keys()):
        meanings.append("{}; {}".format(part, '| '.join(meaning[part])))

    meaning_script = f"{input_text}: "
    for part in meanings:
        meaning_script += part + '\n\n'

    # displaying the output
    messagebox.showinfo(f"Meaning", f"{meaning_script}")
