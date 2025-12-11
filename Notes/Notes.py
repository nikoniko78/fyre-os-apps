import os
import time
from m5stack import speaker
from m5stack_ui import M5Screen, M5Label, M5Btn

# ---------------------
#   CONFIG
# ---------------------
NOTES_DIR = "/sd/Apps/Notes"
NOTES_FILE = NOTES_DIR + "/notes.txt"

screen = M5Screen()
screen.clean_screen()

notes = []


# ---------------------
#   FILE I/O
# ---------------------
def load_notes():
    global notes
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

    with open(NOTES_FILE, "r") as f:
        notes = f.read().split("\n")


def save_notes():
    with open(NOTES_FILE, "w") as f:
        f.write("\n".join(notes))


# ---------------------
#   UI
# ---------------------
labels = []
scroll_offset = 0


def render_notes():
    global labels
    for l in labels:
        screen.remove(l)

    labels = []
    y = 10 - scroll_offset

    for n in notes:
        lbl = M5Label(n, x=5, y=y, color=0xFFFFFF, font=FONT_MID)
        labels.append(lbl)
        y += 20


def scroll_up():
    global scroll_offset
    scroll_offset = max(0, scroll_offset - 20)
    render_notes()


def scroll_down():
    global scroll_offset
    scroll_offset += 20
    render_notes()


def add_note():
    global notes

    # Simple input mode
    screen.clean_screen()
    title = M5Label("Type note:", x=10, y=10, font=FONT_MID)

    buf = ""

    def kb(event):
        nonlocal buf
        key = event
        if key == "Enter":
            notes.append(buf)
            save_notes()
            show_main()
        elif key == "Backspace":
            buf = buf[:-1]
        else:
            buf += key

        screen.remove(input_label)
        draw_input()

    def draw_input():
        global input_label
        input_label = M5Label(buf, x=10, y=40, font=FONT_MID)

    draw_input()
    screen.set_key_callback(kb)


# ---------------------
#   MAIN SCREEN
# ---------------------
def show_main():
    screen.clean_screen()
    render_notes()

    M5Btn(text="Up", x=0, y=200, w=60, h=40, callback=scroll_up)
    M5Btn(text="Down", x=70, y=200, w=60, h=40, callback=scroll_down)
    M5Btn(text="Add", x=140, y=200, w=80, h=40, callback=add_note)


# ---------------------
#   START
# ---------------------
load_notes()
show_main()
