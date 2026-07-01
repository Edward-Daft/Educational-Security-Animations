from Utils import draw_block, move_block_up, move_block_down, get_dark_mode, lock_buttons, unlock_buttons, \
    move_block_right
import config as cf

quiz_questions = [
    {
        "question": "Which statement best describes XOR?",
        "answers": ["Outputs 1 when both inputs are the same", "Outputs 1 when both inputs are different", "Always outputs 0"],
        "correct": 1
    },
    {
        "question": "Which one of these is a characteristic of XOR?",
        "answers": ["Reversible", "Fast", "Both"],
        "correct": 2
    },
    {
        "question": "What is the result of 1 XOR 1?",
        "answers": ["1", "0", "Depends on the key"],
        "correct": 1
    }
]


def get_steps(canvas, root, info_lbl, next_btn, prev_btn):
    W = 750
    H = 600
    c = get_dark_mode()

    def step_0():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
            text="XOR is a logical operation used commonly in security algorithms. It means 'exclusive or' meaning the result is 1, only if the 2 inputs are different",
            font=cf.Fonts["body"],
            fill=c["text"],
            anchor="center",
            width=675)

    def step_1():
        canvas.delete("all")
        lock_buttons(next_btn, prev_btn)
        info_lbl.config(text="If we start with 2 '0's, the output is 0")
        draw_block(canvas, root, 225, 112, "0", "green", 0, "xor")
        draw_block(canvas, root, 300, 112, "XOR", "", 1, "xor")
        draw_block(canvas, root, 375, 112, "0", "green", 0, "xor")
        draw_block(canvas, root, 425, 112, "=", "", 0, "xor")
        root.after(1500, lambda: draw_block(canvas, root, 475, 112, "0", "green", 0, "xor"))

        # Second Case
        root.after(2500, lambda:  (
            info_lbl.config(text="If we have one '1' and one '0' then the result is 1"),
            draw_block(canvas, root, 225, 236, "1", "green", 0, "xor"),
            draw_block(canvas, root, 300, 236, "XOR", "", 1, "xor"),
            draw_block(canvas, root, 375, 236, "0", "green", 0, "xor"),
            draw_block(canvas, root, 425, 236, "=", "", 0, "xor"),

            draw_block(canvas, root, 225, 360, "0", "green", 0, "xor"),
            draw_block(canvas, root, 300, 360, "XOR", "", 1, "xor"),
            draw_block(canvas, root, 375, 360, "1", "green", 0, "xor"),
            draw_block(canvas, root, 425, 360, "=", "", 0, "xor"),
        ))

        root.after(3500, lambda: (
            draw_block(canvas, root, 475, 236, "1", "green", 0, "xor"),
            draw_block(canvas, root, 475, 360, "1", "green", 0, "xor")
        ))

        root.after(5500, lambda: (
            info_lbl.config(text="When we have two '1's is where XOR is different from OR"),
            draw_block(canvas, root, 225, 484, "1", "green", 0, "xor"),
            draw_block(canvas, root, 300, 484, "XOR", "", 1, "xor"),
            draw_block(canvas, root, 375, 484, "1", "green", 0, "xor"),
            draw_block(canvas, root, 425, 484, "=", "", 0, "xor"),
        ))

        root.after(8000, lambda: (draw_block(canvas, root, 475, 484, "0", "green", 0, "xor"), info_lbl.config(text="The result is 0 because the inputs are the same")))
        root.after(8500, lambda: unlock_buttons(next_btn, prev_btn))

    def step_2():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
            text="XOR is used very commonly in cryptography systems for multiple reasons, one being the fact that it is incredibly fast and easy to compute.\n\nThe other benefit is that XOR is reversible.",
            font=cf.Fonts["body"],
            fill=c["text"],
            anchor="center",
            width=675)

    def step_3():
        canvas.delete("all")
        info_lbl.config(text="A plaintext is XORed with a key to create ciphertext")
        lock_buttons(next_btn, prev_btn)

        canvas.create_text(200, 100, font=cf.Fonts["title"], fill=c["text"], anchor="center", text="Plaintext", tag="PT_lbl")
        canvas.create_text(200, 175, font=cf.Fonts["operation"], fill=c["text"], anchor="center", text="XOR")
        canvas.create_text(200, 250, font=cf.Fonts["title"], fill=c["text"], anchor="center", text="Key")
        canvas.create_text(200, 325, font=cf.Fonts["title"], fill=c["text"], anchor="center", text="Ciphertext", tag="CT_lbl")

        PT = ["1", "1", "1", "0"]
        K = ["0", "1", "0", "1"]
        CT = ["1", "0", "1", "1"]
        y_coord = 100
        for x in range(4):
            x_coord = 330 + (x * 30)
            PT_tag = "PT" + str(x)
            K_tag = "K" + str(x)
            draw_block(canvas, root, x_coord, y_coord, PT[x], cf.Block_colours["plaintext"], 0, PT_tag)
            draw_block(canvas, root, x_coord, y_coord + 150, K[x], cf.Block_colours["key"], 0, K_tag)

        down_to = 325
        delay = 1000
        for i in range(4):
            target_pt_tag = "PT" + str(i)
            target_k_tag = "K" + str(i)

            root.after(delay, lambda pt=target_pt_tag, k=target_k_tag: (
                move_block_down(canvas, root, pt, down_to),
                move_block_down(canvas, root, k, down_to),
            ))

            root.after(delay + 2000, lambda pt=target_pt_tag, k=target_k_tag, val=CT[i]: (
                canvas.delete(pt),
                canvas.itemconfig(k + "_text", text=val),
                canvas.itemconfig(k + "_rect", outline=cf.Block_colours["ciphertext"])
            ))

            delay += 3000

        root.after(14000, lambda: (
            info_lbl.config(text="Now the receiver can take that ciphertext and XOR it with the key to obtain the plaintext"),
            canvas.itemconfig("PT_lbl", text="Ciphertext"),
            canvas.itemconfig("CT_lbl", text="Plaintext"),
        ))

        for i in range(4):
            tag = "K" + str(i)
            root.after(14000, lambda tag = tag: canvas.delete(tag))

        for i in range(4):
            x_coord = 330 + (i * 30)
            CT_tag = "CT2_" + str(i)
            K_tag = "K2_" + str(i)
            root.after(15000, lambda X_val=x_coord,ct=CT_tag, k=K_tag, CT_val=CT[i], K_val=K[i]: (
                draw_block(canvas, root, X_val, y_coord, CT_val, cf.Block_colours["ciphertext"], 0, ct),
                draw_block(canvas, root, X_val, y_coord + 150, K_val, cf.Block_colours["key"], 0, k)
            ))

        # This doesnt work
        delay = 16000
        for i in range(4):
            target_ct_tag = "CT2_" + str(i)
            target_k_tag = "K2_" + str(i)

            root.after(delay, lambda ct=target_ct_tag, k=target_k_tag: (
                move_block_down(canvas, root, ct, down_to),
                move_block_down(canvas, root, k, down_to),
            ))

            root.after(delay + 2000, lambda ct=target_ct_tag, k=target_k_tag, val=PT[i]: (
                canvas.delete(ct),
                canvas.itemconfig(k + "_text", text=val),
                canvas.itemconfig(k + "_rect", outline=cf.Block_colours["plaintext"])
            ))

            delay += 3000

        root.after(27000, lambda: info_lbl.config(text="This is why XOR is so useful"))
        root.after(28000, lambda: unlock_buttons(next_btn, prev_btn))


    def step_4():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
            text="Lesson complete! Press next to take the quiz",
            font=cf.Fonts["title"],
            fill=c["text"],
            anchor="center",
            justify="center"
            )

    return [step_0, step_1, step_2, step_3, step_4]