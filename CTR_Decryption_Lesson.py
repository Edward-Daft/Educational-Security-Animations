from Utils import draw_block, move_block_up, move_block_down, get_dark_mode, lock_buttons, unlock_buttons
import config as cf

quiz_questions = [
        {
            "question": "What happens if the ciphertext is modified in CTR mode?",
            "answers": ["It's detected and the ciphertext is rejected","The decryption fails","It decrypts the incorrect ciphertext without warning"],
            "correct": 2
        },
        {
            "question": "Does CTR provide authentication?",
            "answers": ["Yes","No","Sometimes"],
            "correct": 1
        },
        {
            "question": "What part of CTR ensures different outputs each time, even with the same plaintext-key pair?",
            "answers": ["The IV","Galois field multiplication","The XOR operation"],
            "correct": 0
        }
]

def get_steps(canvas, root, info_lbl, next_btn, prev_btn):
    W = 750
    H = 600
    c = get_dark_mode()
    IVs = ["0011", "0100", "0101"]
    Full_CT = ["0011", "1111", "0111"]
    Full_PT = ["0001", "1100", "0011"]
    Y_Sequence = ["0000", "0011", "1011", "0100", "0100", "0011", "1011"]
    def step_0():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W / 2, H / 2,
                           text="To decrypt a message using CTR mode, we start by calculating the keystreams\n"
                                "We do this by incrementing the IV for every ciphertext block,\n"
                                "then encrypting the IVs with the key using AES\n",
                           font=cf.Fonts["body"],
                           fill=c["text"],
                           anchor="center")

    def step_1():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W / 2, 30, text="Keystream Generation", font=cf.Fonts["title"], fill=c["text"])
        column_width = W / 3
        info_lbl.config(text="Incremented IVs are encrypted with the key")
        next_btn.config(state="disabled")
        lock_buttons(next_btn, prev_btn)
        for i in range(3):
            x_center = column_width * i + column_width / 2
            block_tag = "IV" + str(i)
            draw_block(canvas, root, x_center, 100, IVs[i], cf.Block_colours["iv"], 1, block_tag)
        for i in range(3):
            x_center = column_width * i + column_width / 2
            block_tag = "Key" + str(i)
            draw_block(canvas, root, x_center, 300, "1111", cf.Block_colours["key"], 1, block_tag)
        canvas.create_line(125, 130, 125, 270, arrow="last", tag="arrow1", fill=c["text"])
        canvas.create_line(375, 130, 375, 270, arrow="last", tag="arrow2", fill=c["text"])
        canvas.create_line(625, 130, 625, 270, arrow="last", tag="arrow3", fill=c["text"])
        move_block_down(canvas, root, "IV0", 300)
        root.after(2000, lambda: (canvas.delete("arrow1"), canvas.delete("IV0"),canvas.itemconfigure("Key0_text", text="0010"),canvas.itemconfigure("Key0_rect", outline=cf.Block_colours["keystream"])))
        root.after(2100, lambda: move_block_down(canvas, root, "IV1", 300))
        root.after(4100, lambda: (canvas.delete("arrow2"), canvas.delete("IV1"),canvas.itemconfigure("Key1_text", text="0011"),canvas.itemconfigure("Key1_rect", outline=cf.Block_colours["keystream"])))
        root.after(4200, lambda: move_block_down(canvas, root, "IV2", 300))
        root.after(6200, lambda: (canvas.delete("arrow3"), canvas.delete("IV2"), canvas.itemconfigure("Key2_text", text="0100"), canvas.itemconfigure("Key2_rect", outline=cf.Block_colours["keystream"])))
        root.after(6200, lambda: (info_lbl.config(text="Which gives us 3 keystream blocks"), unlock_buttons(next_btn, prev_btn)))

    def step_2():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W / 2, H / 2,
                           text="Now we have the keystreams, we will XOR with the ciphertext blocks\n"
                                "giving us the plaintext. This works because XOR is reversible\n"
                                "meaning that XORing the ciphertext with the keystreams cancels out\n"
                                "the keystream and leaves the plaintext",
                           font=cf.Fonts["body"],
                           fill=c["text"],
                           anchor="center",)

    def step_3():
        PT1 = ["0", "0", "0", "1"]
        KS1 = ["0", "0", "1", "0"]
        CT1 = ["0", "0", "1", "1"]
        lock_buttons(next_btn, prev_btn)
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, 30, text="Decryption of CT block 1", font=cf.Fonts["title"], fill=c["text"])
        info_lbl.config(text="First ciphertext block XORed with the first keystream")
        next_block_center = W / 2 - 45
        for i in range(4):
            CT_block_tag = "CT_Char" + str(i)
            KS_block_tag = "KS_Char" + str(i)
            draw_block(canvas, root, next_block_center, 100, CT1[i], cf.Block_colours["ciphertext"], 2, CT_block_tag)
            draw_block(canvas, root, next_block_center, 300, KS1[i], cf.Block_colours["keystream"], 2, KS_block_tag)
            next_block_center = next_block_center + 30
        canvas.create_text(200, 100, text="Ciphertext:", font=cf.Fonts["label"], fill=c["text"])
        canvas.create_text(200, 300, text="Keystream:", font=cf.Fonts["label"], fill=c["text"])
        canvas.create_text(200, 200, text="XOR", font=cf.Fonts["operation"], fill=c["text"])
        start_delay = 500
        start_x = 330
        for x in range(4):
            CT_block_tag_to_move = "CT_Char" + str(x)
            KS_block_tag_to_move = "KS_Char" + str(x)
            root.after(start_delay,lambda ct=CT_block_tag_to_move, ks=KS_block_tag_to_move: (move_block_down(canvas, root, ct, 200),move_block_up(canvas, root, ks, 200)))
            root.after(start_delay + 1000,lambda ct=CT_block_tag_to_move, ks=KS_block_tag_to_move: (canvas.delete(ct), canvas.delete(ks)))
            root.after(start_delay + 1100, lambda x_pos=start_x, txt=PT1[x]: (draw_block(canvas, root, x_pos, 200, txt, cf.Block_colours["plaintext"], 2, "PT")))
            start_delay += 1000
            start_x += 30
        root.after(5000, lambda: (info_lbl.config(text="Giving us our first plaintext block"),unlock_buttons(next_btn, prev_btn)))

    def step_4():
        col_width = W / 3
        delay = 0
        canvas.delete("all")
        info_lbl.config(text="")
        lock_buttons(next_btn, prev_btn)
        canvas.create_text(W / 2, 30, text="Decryption", font=cf.Fonts["title"], fill=c["text"])
        info_lbl.config(text="The other ciphertext blocks are XORed with their respective keystream\ngiving us the following full plaintext")
        for i in range(3):
            x_center = col_width * i + col_width / 2
            text = "Plaintext Block " + str(i + 1)
            canvas.create_text(x_center, 250, text=text, font=cf.Fonts["label"], fill=c["text"])
        for i in range(3):
            x_center = col_width * i + col_width / 2
            root.after(delay, lambda x=x_center, txt=Full_PT[i]: draw_block(canvas, root, x, 300, txt, cf.Block_colours["plaintext"], 1, "CipherText"))
            delay = delay + 1000
        root.after(3000, lambda: unlock_buttons(next_btn, prev_btn))

    def step_5():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
                           text="Lesson complete! Press next to take the quiz",
                           font=cf.Fonts["title"],
                           fill=c["text"],
                           anchor="center",
                           justify="center"
                           )


    return [step_0, step_1, step_2, step_3, step_4, step_5]