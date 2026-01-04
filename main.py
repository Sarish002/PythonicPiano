import time
import pygame
import threading
import numpy as np
from customtkinter import *

root = CTk()
root.title("Pythonic Piano")
root.geometry("450x300")

pygame.init()

def change_pitch(key, factor):  # NEW
    WhiteKey.factor = factor
    BlackKey.factor = factor
    note = pygame.mixer.Sound(key.note)
    samples = pygame.sndarray.array(note)
    new_len = int(len(samples) / factor)
    indices = np.linspace(0, len(samples), new_len, endpoint=False).astype(int)
    pitched_samples = samples[indices]
    return pygame.sndarray.make_sound(pitched_samples)

def play(key, factor):
    note = change_pitch(key, factor)
    key.key.configure(fg_color="#808080")
    root.update()
    note.play()
    root.after(100)
    if "b" not in key.note:
        key.key.configure(fg_color="white")
    else:
        key.key.configure(fg_color="black")

class WhiteKey:
    notes = ["C", "D", "E", "F", "G", "A", "B"]
    factor = 1
    def __init__(self, master, note):
        self.master = master
        self.note = f"{note}3.mp3"
        self.place = (WhiteKey.notes.index(note) + 1) / 8
        self.key = CTkButton(master=master,
                             fg_color="white",
                             corner_radius=0,
                             border_width=5,
                             border_color="black",
                             text="",
                             hover=False,
                             height=250,
                             width=59.25,
                             command=lambda: play(self, WhiteKey.factor))

whites = []
for key in WhiteKey.notes:
    button = WhiteKey(root, key)
    button.key.place(relx=button.place, rely=0.5, anchor="center")
    whites.append(button)

class BlackKey:
    notes = ["", "Db", "Eb", "", "Gb", "Ab", "Bb"]
    factor = 0.75
    def __init__(self, master, note):
        self.master = master
        self.note = f"{note}3.mp3"
        self.place = (BlackKey.notes.index(note) + 1) / 8 - 0.07
        self.key = CTkButton(master=master,
                             fg_color="black",
                             border_width=5,
                             border_color="black",
                             corner_radius=0,
                             text="",
                             hover=False,
                             height=125,
                             width=40,
                             command=lambda: play(self, WhiteKey.factor))


blacks = []
for key in BlackKey.notes:
    if key == "":
        continue
    button = BlackKey(root, key)
    button.key.place(relx=button.place, rely=0.292, anchor="center")
    blacks.append(button)

keys = {
    "c": whites[0],
    "d": whites[1],
    "e": whites[2],
    "f": whites[3],
    "g": whites[4],
    "a": whites[5],
    "b": whites[6],
    "1": blacks[0],
    "2": blacks[1],
    "3": blacks[2],
    "4": blacks[3],
    "5": blacks[4],
}

def on_key(event):
    key = event.char.lower() # NEW
    if key == "=":
        WhiteKey.factor *= 2
        print(WhiteKey.factor)
        return
    elif key == "-":
        WhiteKey.factor /= 2
        print(WhiteKey.factor)
        return
    if key in keys:
        keys[key].key.configure(fg_color="#808080")
        play(keys[key], WhiteKey.factor)


def on_key_rels(event):
    key: str = event.char.lower()
    if key in keys:
        if not key.isdigit():
            keys[key].key.configure(fg_color="white")
        else:
            keys[key].key.configure(fg_color="black")

root.bind("<KeyPress>", on_key) # NEW
root.bind("<KeyRelease>", on_key_rels)
root.focus_set()
root.mainloop()
