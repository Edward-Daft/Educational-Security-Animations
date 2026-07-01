from Utils import draw_block, move_block_up, move_block_down, get_dark_mode, lock_buttons, unlock_buttons, move_block_right
import config as cf

quiz_questions = [
        {
            "question": "Who is Alice trying to send a message to?",
            "answers": ["Bob", "Eve",
                        "Herself"],
            "correct": 0
        },
        {
            "question": "What is Eve's goal?",
            "answers": ["Stop the message going through", "Intercept and read the message", "Nothing"],
            "correct": 1
        },
        {
            "question": "Placeholder",
            "answers": ["answer1", "answer2", "answer3"],
            "correct": 1
        }
]

def get_steps(canvas, root, info_lbl, next_btn, prev_btn):
    W = 750
    H = 600
    c = get_dark_mode()
    def step_0():
        info_lbl.config(fg= c["text"])
        info_lbl.config(text="Alice wants to send a message to Bob")
        lock_buttons(next_btn, info_lbl)
        draw_block(canvas, root, 155, 300, "Alice", cf.Block_colours["auth_tag"], 1, "Alice")
        draw_block(canvas, root, 600, 300, "Bob", cf.Block_colours["auth_tag"], 1, "Bob")
        root.after(500, lambda: draw_block(canvas, root, 235, 300, "M1", cf.Block_colours["plaintext"], 0, "Message"))
        root.after(1500, lambda: move_block_right(canvas, root, "Message", 515))
        root.after(4000, lambda: canvas.delete("Message"))
        root.after(4500, lambda: info_lbl.config(text="However, Eve wants to intercept and read the message"))
        root.after(5000, lambda: draw_block(canvas, root, 375, 100, "Eve", cf.Block_colours["ciphertext"], 1, "Eve"))
        root.after(5000, lambda: draw_block(canvas, root, 235, 300, "M1", cf.Block_colours["plaintext"], 0, "Message"))
        root.after(5500, lambda: move_block_right(canvas, root, "Message", 375))
        root.after(6500, lambda: move_block_up(canvas, root, "Message", 141))
        root.after(8500, lambda: move_block_down(canvas, root, "Message", 300))
        root.after(10000, lambda: move_block_right(canvas, root, "Message", 515))
        root.after(10000, lambda: info_lbl.config(text = "This gives us the security problem"))
        root.after(12000, lambda: canvas.delete("Message"))
        root.after(12000, lambda: unlock_buttons(next_btn, prev_btn))

    def step_1():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W / 2, H / 2,
                           text="In the next lesson, you will learn how Alice prevents this from happening, and the further problems that also have to be solved.\n\n Press next for the quiz",
                           font=cf.Fonts["body"],
                           fill=c["text"],
                           anchor="center",
                           width=675)


    return [step_0, step_1]