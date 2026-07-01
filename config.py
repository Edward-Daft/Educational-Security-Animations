dark_mode = False
base_font_size = 14
Settings_file = "settings.txt"

Fonts = {
    "body": ("Arial", base_font_size),
    "title": ("Arial", base_font_size + 4, "bold"),
    "subtitle": ("Arial", base_font_size + 2, "bold"),
    "label": ("Arial", base_font_size, "bold"),
    "operation": ("Arial", base_font_size + 6, "bold"),
    "block_text": ("Arial", base_font_size -1),
    "intro_screen_text": ("Arial", base_font_size + 11, "bold")
}

Colours = {
    "bg": "light grey",
    "widget_bg": "white",
    "widget_fg": "black",
    "text": "black",
    "label_bg": "light grey",
    "complete": "light green"
}

Dark_colours = {
    "bg": "gray12",
    "widget_bg": "gray20",
    "widget_fg": "white",
    "text": "white",
    "label_bg": "gray12",
    "complete": "forest green"
}

Block_colours = {
    "iv": "deep pink",
    "key": "blue",
    "keystream": "orange",
    "plaintext": "green",
    "ciphertext": "red",
    "h": "purple",
    "auth_tag": "black"
}

def load_settings():
    global dark_mode, base_font_size
    try:
        file = open(Settings_file, "r")
        lines = file.readlines()
        file.close()

        dark_mode = lines[0].strip() == "True"
        base_font_size = int(lines[1].strip())
    except:
        dark_mode = False
        base_font_size = 14
    update_fonts()

def save_settings():
    file = open(Settings_file, "w")
    file.write(f"{dark_mode}\n")
    file.write(f"{base_font_size}\n")
    file.close()

def update_fonts():
    global Fonts
    Fonts = {
        "body": ("Arial", base_font_size),
        "title": ("Arial", base_font_size + 4, "bold"),
        "subtitle": ("Arial", base_font_size + 2, "bold"),
        "label": ("Arial", base_font_size, "bold"),
        "operation": ("Arial", base_font_size + 6, "bold"),
        "block_text": ("Arial", base_font_size - 1),
        "intro_screen_text": ("Arial", base_font_size + 11, "bold")
    }
