import tkinter as tk
import Counter_Encryption_Lesson
import GCM_Encryption_Lesson
import Custom_GCM_Lesson
import GCM_Decryption_Lesson
import CTR_Decryption_Lesson
import Security_Problem
import XOR_Lesson
import config as cf
cf.load_settings()
from tkinter import messagebox
from Utils import get_dark_mode

# Creating main window
root = tk.Tk()
root.title("Educational Security Animations")
root.geometry("1000x900")
root.configure(bg= cf.Colours["bg"])
root.resizable(False, False)

# Container to store pages
container = tk.Frame(root, bg= cf.Colours["bg"])
container.place(relx=0, rely=0, relwidth=1, relheight=1)

# Page switching logic
pages = {}
def show_page(name):
    pages[name].lift()

current_step = 0
steps = []
total = 0
current_quiz_questions = []
current_lesson_name = ""

def change_step(direction):
    global current_step
    temp_step = current_step + direction
    if 0 <= temp_step <= total:
        current_step = temp_step
        prog_lbl.config(text=f"{current_step}/{total}")
        prev_btn.config(state="disabled" if current_step == 0 else "normal")
        next_btn.config(state="disabled" if current_step == (total + 1) else "normal")
        steps[current_step]()
    elif temp_step > total:
        load_quiz(current_quiz_questions)
        print("Quiz loading")

def load_lesson(steps_list, questions, lesson_name):
    global steps, current_step, total, current_quiz_questions, current_lesson_name
    current_lesson_name = lesson_name
    steps = steps_list
    current_quiz_questions = questions
    current_step = 0
    total = len(steps) - 1
    prog_lbl.config(text=f"0/{total}")
    prev_btn.config(state="disabled")
    next_btn.config(state="normal")
    steps[0]()
    show_page("animation")

# Global variables needed for quiz
current_quiz = []
answer_vals = []
question_frames = []

def load_quiz(questions):
    global current_quiz, answer_vals, question_frames
    current_quiz = questions
    answer_vals = []
    question_frames = []
    c = get_dark_mode()

    for widget in quiz_canvas.winfo_children():
        widget.destroy()

    # Building container for each question and its answers
    for i, item in enumerate(questions):
        question_frame = tk.Frame(quiz_canvas, bg= c["bg"])
        question_frame.pack(pady=15, anchor="w", padx=40)
        question_frames.append(question_frame)
        question_lbl = tk.Label(question_frame, text=f"Q{i+1}- {item['question']}", bg= c["label_bg"],
                                fg=c["widget_fg"], font=cf.Fonts["label"], wraplength=650, justify="left")
        question_lbl.pack(anchor="w")
        value = tk.IntVar(value=-1)
        answer_vals.append(value)

        for j, answer in enumerate(item["answers"]):
            radio_button = tk.Radiobutton(question_frame, text=answer,
                                          variable = value, value = j,
                                          bg= c["label_bg"], fg=c["widget_fg"],
                                          font=cf.Fonts["body"], anchor="w",
                                          selectcolor= c["widget_bg"], activebackground= c["label_bg"],
                                          activeforeground= c["widget_fg"])
            radio_button.pack(anchor="w", padx=20)

    submit_btn = tk.Button(quiz_canvas, text="Submit", command=submit_quiz,
                           bg= c["widget_bg"], fg=c["widget_fg"],
                           padx=20, pady=5, cursor="hand2")
    submit_btn.pack(pady=20)
    show_page("quiz")

def submit_quiz():
    score = 0
    c = get_dark_mode()
    for i, item in enumerate(current_quiz):
        if answer_vals[i].get() == item["correct"]:
            score += 1

    tk.messagebox.showinfo("Result", f"You scored {score}/3")
    for widget in quiz_canvas.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") in ["Finish", "Try Again"]:
            widget.destroy()

    if score == 3:
        finish_btn = tk.Button(quiz_canvas, text="Finish",
                               command= lambda: (mark_as_complete(current_lesson_name), update_lesson_buttons(), show_page("lessons")),
                               bg= c["widget_bg"], fg=c["widget_fg"], padx=20, pady=5, cursor="hand2")
        finish_btn.pack(pady=5)
    else:
        Try_Again_btn = tk.Button(quiz_canvas, text="Try Again",
                                  command = lambda: load_quiz(current_quiz_questions),
                                  bg=c["widget_bg"], fg=c["widget_fg"],padx=20, pady=5, cursor="hand2")
        Try_Again_btn.pack(pady=5)

# Changing the appearance of lesson buttons when complete
def mark_as_complete(lesson_name):
    file = open("progress.txt", "a")
    file.write(lesson_name + "\n")
    file.close()

def update_lesson_buttons():
    try:
        file = open("progress.txt", "r")
        content = file.read()
        file.close()
    except:
        return

    if cf.dark_mode:
        c = cf.Dark_colours
    else:
        c = cf.Colours

    if "CTR Encryption" in content:
        CTR_animation.config(bg=c["complete"])
    else:
        CTR_animation.config(bg=c["widget_bg"])
    if "GCM Encryption" in content:
        GCM_animation.config(bg=c["complete"])
    else:
        GCM_animation.config(bg=c["widget_bg"])
    if "Custom GCM" in content:
        Custom_GCM.config(bg=c["complete"])
    else:
        Custom_GCM.config(bg=c["widget_bg"])
    if "GCM Decryption" in content:
        GCM_de_animation.config(bg=c["complete"])
    else:
        GCM_de_animation.config(bg=c["widget_bg"])
    if "CTR Decryption" in content:
        CTR_de_animation.config(bg=c["complete"])
    else:
        CTR_de_animation.config(bg=c["widget_bg"])
    if "Security Problem" in content:
        Security_problem_btn.config(bg=c["complete"])
    else:
        Security_problem_btn.config(bg=c["widget_bg"])
    if "XOR" in content:
        XOR_Lesson_btn.config(bg=c["complete"])
    else:
        XOR_Lesson_btn.config(bg=c["widget_bg"])

# SETTINGS FUNCTIONS
# Toggling dark mode logic
def toggle_dark_mode():
    cf.dark_mode = not cf.dark_mode
    if cf.dark_mode:
        dark_btn.config(text="Light Mode")
    else:
        dark_btn.config(text="Dark Mode")
    cf.save_settings()
    apply_theme()

# Font size switching
def update_preview(event=None):
    size = font_slider.get()
    preview_lbl.config(font=("Arial", size))

def apply_font_size():
    cf.base_font_size = font_slider.get()
    cf.update_fonts()
    cf.save_settings()
    apply_theme()

# Creating input screen for Custom_GCM
def open_gcm_setup():
    c = get_dark_mode()
    popup = tk.Toplevel(root)
    popup.title("Custom GCM Setup")
    popup.configure(bg=c["bg"])
    popup.geometry("400x400")

    entries = []
    labels = [
        "Plaintext Block 1",
        "Plaintext Block 2",
        "Plaintext Block 3",
        "Key",
        "IV"
    ]

    for text in labels:
        lbl = tk.Label(popup, text=text, bg=c["label_bg"], fg=c["text"])
        lbl.pack(pady=5)
        entry = tk.Entry(popup, bg=c["widget_bg"], fg=c["widget_fg"], justify="center")
        entry.pack(pady=5)
        entries.append(entry)

    error_lbl = tk.Label(popup, text="", bg=c["bg"], fg="red")
    error_lbl.pack(pady=5)

    def is_valid(value):
        value = value.strip()
        if len(value) != 4:
            return False
        for char in value:
            if char not in ["0", "1"]:
                return False
        return True

    def submit():
        values = []
        for e in entries:
            values.append(e.get().strip())

        for v in values:
            if not is_valid(v):
                error_lbl.config(text="All inputs must be 4 binary bits (only 1 or 0)")
                return

        popup.destroy()

        load_lesson(Custom_GCM_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn, values), Custom_GCM_Lesson.quiz_questions, "Custom GCM")

    submit_btn = tk.Button(popup, text="Start", command=submit, bg=c["widget_bg"], fg=c["widget_fg"])
    submit_btn.pack(pady=15)

def reset_progress():
    file = open("progress.txt", "w")
    file.close()
    update_lesson_buttons()
    messagebox.showinfo("Reset", "Progress Reset Successfully")

# Creating start page
start_page = tk.Frame(container, bg=cf.Colours["bg"])
start_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["start"] = start_page

center_frame = tk.Frame(start_page, bg=cf.Colours["bg"])
center_frame.place(relx=0.5, rely=0.5, anchor="center")
title_label = tk.Label(center_frame,
                       text="Educational Security Animations",
                       bg=cf.Colours["label_bg"],
                       fg=cf.Colours["text"],
                       font=cf.Fonts["intro_screen_text"])
title_label.pack(pady=(0, 48))
btn_stack = tk.Frame(center_frame, bg=cf.Colours["bg"])
btn_stack.pack()
start_btn = tk.Button(btn_stack, text="Start",
                      command=lambda: show_page("lessons"),
                      bg=cf.Colours["widget_bg"],
                      fg=cf.Colours["widget_fg"],
                      padx=32, pady=5, width=12,
                      height=1, cursor="hand2")
start_btn.pack(pady=5)

glsry_btn = tk.Button(btn_stack, text="Glossary", command=lambda: show_page("glossary"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], padx=32, pady=5, width=12, height=1, cursor="hand2")
glsry_btn.pack(pady=5)
settings_btn = tk.Button(btn_stack, text="Settings", command=lambda: show_page("settings"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], padx=32, pady=5, width=12, height=1, cursor="hand2")
settings_btn.pack(pady=5)

# Creating Animation Page
animation_page = tk.Frame(container, bg=cf.Colours["bg"])
animation_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["animation"] = animation_page

back_btn = tk.Button(animation_page, text="Back", command= lambda: show_page("lessons"), cursor="hand2", width=6, height=1, padx=12)
back_btn.place(relx=0.02, rely=0.94)
canvas = tk.Canvas(animation_page, bg=cf.Colours["widget_bg"], width=750, height=600)
canvas.place(relx=0.5, rely=0.5, anchor="center")
info_lbl = tk.Label(animation_page, text="", font=cf.Fonts["label"], wraplength=700, justify="center", bg=cf.Colours["widget_bg"])
info_lbl.place(relx=0.5, rely=0.80, anchor="center")
next_btn = tk.Button(animation_page, text="Next", cursor="hand2", padx=12, command= lambda: change_step(1), width=6, height=1)
next_btn.place(relx=0.87, rely=0.94)
prev_btn = tk.Button(animation_page, text="Previous", cursor="hand2", padx=12, command= lambda: change_step(-1), width=6, height=1)
prev_btn.place(relx=0.75, rely=0.94)
prog_lbl = tk.Label(animation_page, text="0/8", font=cf.Fonts["block_text"], bg=cf.Colours["label_bg"])
prog_lbl.place(relx=0.5, rely=0.13, anchor="center")

# Creating Lessons Page
lessons_page = tk.Frame(container, bg=cf.Colours["bg"])
lessons_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["lessons"] = lessons_page

choose_lbl = tk.Label(lessons_page, text="Choose a lesson", bg=cf.Colours["label_bg"], font=cf.Fonts["operation"])
choose_lbl.pack(pady=60)
Security_problem_btn = tk.Button(lessons_page, text="Security Problem", command= lambda: load_lesson(Security_Problem.get_steps(canvas, root, info_lbl, next_btn, prev_btn), Security_Problem.quiz_questions, "Security Problem"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width=20, height=1, pady=8, cursor="hand2")
Security_problem_btn.pack(pady=8)
XOR_Lesson_btn = tk.Button(lessons_page, text="XOR", command= lambda: load_lesson(XOR_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn), XOR_Lesson.quiz_questions, "XOR"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width=20, height=1, pady=8, cursor="hand2")
XOR_Lesson_btn.pack(pady=8)
CTR_animation = tk.Button(lessons_page, text="CTR Encryption", command= lambda: load_lesson(Counter_Encryption_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn), Counter_Encryption_Lesson.quiz_questions, "CTR Encryption"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width=20, height=1, pady=8, cursor="hand2")
CTR_animation.pack(pady=8)
GCM_animation = tk.Button(lessons_page, text="GCM Encryption", command= lambda: load_lesson(GCM_Encryption_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn), GCM_Encryption_Lesson.quiz_questions, "GCM Encryption"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width= 20, height=1, pady=8, cursor="hand2")
GCM_animation.pack(pady=8)
Custom_GCM = tk.Button(lessons_page, text="GCM Encryption (custom)", command=open_gcm_setup, bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width=20, height=1, pady=8, cursor="hand2")
Custom_GCM.pack(pady=8)
CTR_de_animation = tk.Button(lessons_page, text="CTR Decryption", command = lambda: load_lesson(CTR_Decryption_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn), CTR_Decryption_Lesson.quiz_questions, "CTR Decryption"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width = 20, height=1, pady=8, cursor="hand2")
CTR_de_animation.pack(pady=8)
GCM_de_animation = tk.Button(lessons_page, text="GCM Decryption", command = lambda: load_lesson(GCM_Decryption_Lesson.get_steps(canvas, root, info_lbl, next_btn, prev_btn), GCM_Decryption_Lesson.quiz_questions, "GCM Decryption"), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], width = 20,height=1, pady=8, cursor="hand2")
GCM_de_animation.pack(pady=8)
lessons_back_btn = tk.Button(lessons_page, text="Back", command=lambda: show_page("start"),cursor="hand2", width = 6, height = 1)
lessons_back_btn.place(relx=0.02, rely=0.94)
update_lesson_buttons()

# Creating Glossary page
glossary_page = tk.Frame(container, bg=cf.Colours["bg"])
glossary_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["glossary"] = glossary_page

glossary_title_lbl = tk.Label(glossary_page, text="Glossary", bg=cf.Colours["label_bg"], fg="#000000", font=cf.Fonts["title"])
glossary_title_lbl.pack(pady=30)
glossary_back_btn = tk.Button(glossary_page, text="Back", command=lambda: show_page("start"), cursor="hand2")
glossary_back_btn.place(relx=0.02, rely=0.95)
glossary_canvas = tk.Canvas(glossary_page, bg=cf.Colours["widget_bg"], width=750, height=600)
glossary_canvas.place(relx=0.5, rely=0.5, anchor="center")

term_canvas = tk.Canvas(glossary_canvas, bg=cf.Colours["widget_bg"], width=250, height=600, highlightthickness=0)
term_canvas.place(x=0, y=0)
scrollbar = tk.Scrollbar(glossary_canvas, orient="vertical", command=term_canvas.yview)
scrollbar.place(x=230, y=0, height=700)
term_canvas.configure(yscrollcommand=scrollbar.set)
term_frame = tk.Frame(term_canvas, bg=cf.Colours["widget_bg"])
term_canvas.create_window((0, 0), window=term_frame, anchor="nw")

term_label = tk.Label(glossary_canvas,text="",bg=cf.Colours["widget_bg"],font=cf.Fonts["label"],wraplength=400,justify="left")
term_label.place(x=260, y=20)
definition_label = tk.Label(glossary_canvas,text="Select a term to see its definition",bg=cf.Colours["widget_bg"],font=cf.Fonts["label"],wraplength=400,justify="left")
definition_label.place(x=260, y=50)

# Loading glossary file
file = open("Glossary.txt", "r", encoding="utf-8")
glossary_content = file.read()
file.close()

# Fetching glossary entries
entries = glossary_content.split("**")
glossary_list = []
for entry in entries:
    if "//" in entry:
        items = entry.split("//")
        term = items[0].strip()
        definition = items[1].strip()
        glossary_list.append([term, definition])
glossary_list.sort(key=lambda x: x[0].lower())

def show_definition(term, definition):
    definition_label.config(text=definition)
    term_label.config(text=term + ":")

# Create buttons for each term
glossary_btns = []
for item in glossary_list:
    c = get_dark_mode()
    term = item[0]
    definition = item[1]

    btn = tk.Button(term_frame,text=term,anchor="center",bg=c["widget_bg"], fg=c["widget_fg"],
                    command=lambda t=term, d=definition: show_definition(t, d),cursor="hand2")
    btn.pack(pady=2, padx=1, fill="x")
    glossary_btns.append(btn)

term_frame.update_idletasks()
term_canvas.configure(scrollregion=term_canvas.bbox("all"))

# Creating quiz page
quiz_page = tk.Frame(container, bg=cf.Colours["bg"])
quiz_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["quiz"] = quiz_page

quiz_title_lbl = tk.Label(quiz_page, text="Quiz", bg=cf.Colours["label_bg"], font=cf.Fonts["title"])
quiz_title_lbl.pack(pady=20)
quiz_question_lbl = tk.Label(quiz_page, text="", bg=cf.Colours["label_bg"], font=cf.Fonts["label"], wraplength=700)
quiz_question_lbl.pack(pady=10)
quiz_canvas = tk.Canvas(quiz_page, bg=cf.Colours["bg"], highlightthickness=0, height=500, width=800)
quiz_canvas.pack()

# Creating settings page
settings_page = tk.Frame(container, bg=cf.Colours["bg"])
settings_page.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["settings"] = settings_page

settings_back_btn = tk.Button(settings_page, text="Back", command=lambda: show_page("start"), cursor="hand2", width=6, height=1)
settings_back_btn.place(relx=0.02, rely=0.95)

settings_frame = tk.Frame(settings_page, bg=cf.Colours["bg"])
settings_frame.place(relx=0.5, rely=0.5, anchor="center")

settings_lbl = tk.Label(settings_frame, text="Settings", bg=cf.Colours["label_bg"], fg=cf.Colours["text"], font=cf.Fonts["title"])
settings_lbl.pack(pady=50)

if cf.dark_mode:
    dark_mode_text = "Light Mode"
else:
    dark_mode_text = "Dark Mode"
dark_btn = tk.Button(settings_frame, text=dark_mode_text, command=toggle_dark_mode, bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], padx=32, pady=5, width=10, height=1, cursor="hand2")
dark_btn.pack(pady=10)

reset_prog_btn = tk.Button(settings_frame, text="Reset Progress", command=reset_progress, bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], padx=32, pady=5, width=10, height=1, cursor="hand2")
reset_prog_btn.pack(pady=10)

font_size_lbl = tk.Label(settings_frame, text="Text Size", bg=cf.Colours["label_bg"], font=cf.Fonts["label"], fg=cf.Colours["text"])
font_size_lbl.pack(pady=(20,5))

font_slider = tk.Scale(settings_frame, from_=10, to=16, resolution=1, orient="horizontal", length=300, bg=cf.Colours["bg"], fg=cf.Colours["text"], highlightthickness=0, troughcolor=cf.Colours["widget_bg"])
font_slider.set(cf.base_font_size)
font_slider.pack(pady=5)
font_slider.bind("<Motion>", update_preview)

preview_lbl = tk.Label(settings_frame, text="Preview Text", bg=cf.Colours["label_bg"], fg=cf.Colours["text"], font=cf.Fonts["body"])
preview_lbl.pack(pady=10)

apply_font_btn = tk.Button(settings_frame, text="Apply", command= lambda: apply_font_size(), bg=cf.Colours["widget_bg"], fg=cf.Colours["widget_fg"], cursor="hand2", padx=20, pady=5, width=10, height=1)
apply_font_btn.pack(pady=10)

########################################################################################################################
# Dark mode switching
bg_group = [root, container, start_page, center_frame, btn_stack, lessons_page, animation_page, glossary_page, quiz_page, quiz_canvas, settings_page, settings_frame]
label_group = [title_label, choose_lbl, prog_lbl, glossary_title_lbl, quiz_title_lbl, quiz_question_lbl, settings_lbl, font_size_lbl, preview_lbl]
widget_group = [XOR_Lesson_btn, Security_problem_btn, CTR_de_animation, GCM_de_animation , reset_prog_btn, start_btn, glsry_btn, settings_btn, dark_btn, CTR_animation, GCM_animation, Custom_GCM, lessons_back_btn, back_btn, canvas, info_lbl, next_btn, prev_btn, glossary_back_btn, glossary_canvas, term_canvas, term_frame, term_label, definition_label, settings_back_btn, apply_font_btn, font_slider]

def apply_theme():
    if cf.dark_mode:
        c = cf.Dark_colours
    else:
        c = cf.Colours
    for w in bg_group:
        w.configure(bg=c["bg"])
    for w in label_group:
        w.configure(bg=c["label_bg"], fg=c["text"], font=cf.Fonts["body"])
    for w in widget_group:
        try:
            w.configure(bg=c["widget_bg"], fg=c["widget_fg"], font=cf.Fonts["body"])
        except:
            w.configure(bg=c["widget_bg"])
    for w in glossary_btns:
        w.configure(bg=c["widget_bg"], fg=c["widget_fg"], font=cf.Fonts["body"])
    font_slider.configure(bg=c["bg"], fg=c["text"], troughcolor=c["widget_bg"])
    # Update specific widgets that don't use "body"
    title_label.config(font=cf.Fonts["intro_screen_text"])
    settings_lbl.config(font=cf.Fonts["title"])
    choose_lbl.config(font=cf.Fonts["operation"])
    glossary_title_lbl.config(font=cf.Fonts["title"])
    quiz_title_lbl.config(font=cf.Fonts["title"])
    prog_lbl.config(font=cf.Fonts["block_text"])
    term_frame.update_idletasks()
    term_canvas.config(scrollregion=term_canvas.bbox("all"))
    update_lesson_buttons()
    if len(steps) > 0:
        steps[current_step]()



# Loop to ensure GUI stays visible
apply_theme()
show_page("start")
root.mainloop()


