import config as cf

def get_dark_mode():
    if cf.dark_mode:
        c = cf.Dark_colours
    else:
        c = cf.Colours
    return c

def lock_buttons(next_btn, prev_btn):
    next_btn.config(state="disabled")
    prev_btn.config(state="disabled")

def unlock_buttons(next_btn, prev_btn):
    next_btn.config(state="normal")
    prev_btn.config(state="normal")

def draw_block(canvas, root, x, y, text, outline, block_size, tag):
    # Draws rectangle that is centred around x,y
    c = get_dark_mode()

    if block_size == 1:
        x1 = x - 60
        y1 = y - 25
        x2 = x + 60
        y2 = y + 25
    else:
        x1 = x - 15
        y1 = y - 12
        x2 = x + 15
        y2 = y + 12

    canvas.create_rectangle(x1, y1, x2, y2, outline=outline, tags=(tag, tag + "_rect"), width=2)
    canvas.create_text(x, y, text=text, font=cf.Fonts["block_text"], fill=c["text"], anchor="center", tags=(tag, tag + "_text"))


def move_block_down(canvas, root, tag, target_y):
    coords = canvas.bbox(tag)
    current_y = (coords[1] + coords[3]) / 2
    if current_y < target_y:
        canvas.move(tag, 0, 2)
        root.after(10, lambda: move_block_down(canvas, root, tag, target_y))
    else:
        return


def move_block_up(canvas, root, tag, target_y):
    coords = canvas.bbox(tag)
    current_y = (coords[1] + coords[3]) / 2
    if current_y > target_y:
        canvas.move(tag, 0, -2)
        root.after(10, lambda: move_block_up(canvas, root, tag, target_y))
    else:
        return

def move_block_right(canvas, root, tag, target_x):
    coords = canvas.bbox(tag)
    current_x = (coords[0] + coords[2]) / 2
    if current_x < target_x:
        canvas.move(tag, 2, 0)
        root.after(10, lambda: move_block_right(canvas, root, tag, target_x))
    else:
        return

def move_block_left(canvas, root, tag, target_x):
    coords = canvas.bbox(tag)
    current_x = (coords[0] + coords[2]) / 2
    if current_x < target_x:
        canvas.move(tag, -2, 0)
        root.after(10, lambda: move_block_left(canvas, root, tag, target_x))
    else:
        return
