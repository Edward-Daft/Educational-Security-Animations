from Utils import draw_block, move_block_up, move_block_down, get_dark_mode, lock_buttons, unlock_buttons
import config as cf

quiz_questions = [
        {
            "question": "What does CTR mode use to generate a keystream?",
            "answers": ["An incrementing counter encrypted with AES", "The plaintext XORed with the key",
                        "A random number generator"],
            "correct": 0
        },
        {
            "question": "What operation is used to combine the keystream with the plaintext?",
            "answers": ["AND", "XOR", "OR"],
            "correct": 1
        },
        {
            "question": "What must never be reused in CTR mode?",
            "answers": ["The key", "The ciphertext", "The IV / Nonce"],
            "correct": 2
        }
]

def get_steps(canvas, root, info_lbl, next_btn, prev_btn):

    # Defining Constants
    W = 750
    H = 600
    IVs = ["0011", "0100", "0101"]
    Full_CT = ["0011", "1111", "0111"]
    c = get_dark_mode()

    # Defining the steps of the animation
    def step_0():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W/2, H/2,
            text="CTR is a mode of operation that turns a block cipher into a stream cipher. It does this by creating keystreams to encrypt each block with. The main components of CTR are: Plaintext, Key, Initialisation Vector (Nonce). This nonce must never be reused.\n"
                 "\nFor this example we will use the following values:\nPlaintext: 0001,1100,0011\nKey: 1111\nIV: 0010",
            font=cf.Fonts["body"],
            fill=c["text"],
            anchor="center",
            width=675)

    def step_1():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W/2, H/2,
            text="The first step is to create keystreams for each of the plaintext blocks\n"
                 "This is done by incrementing the IV and encrypting it with the key using AES\n"
                 "NOTE: For this demo AES not used due to size of the blocks,\n"
                 "simplified algorithm used instead to illustrate",
            font=cf.Fonts["body"],
            fill=c["text"],
            anchor="center",
            justify="center")

    def step_2():
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W/2, 30, text="Keystream Generation", fill=c["text"], font=cf.Fonts["title"])
        column_width = W/3
        info_lbl.config(text="Incremented IVs are encrypted with the key")
        lock_buttons(next_btn, prev_btn)
        for i in range(3):
            x_center = column_width * i + column_width/2
            block_tag = "IV" + str(i)
            draw_block(canvas, root, x_center, 100, IVs[i], cf.Block_colours["iv"], 1, block_tag)
        for i in range(3):
            x_center = column_width * i + column_width/2
            block_tag = "Key" + str(i)
            draw_block(canvas, root, x_center, 300, "1111", cf.Block_colours["key"], 1,  block_tag)
        canvas.create_line(125, 130, 125, 270, arrow="last", tag="arrow1")
        canvas.create_line(375, 130, 375, 270, arrow="last", tag="arrow2")
        canvas.create_line(625, 130, 625, 270, arrow="last", tag="arrow3")
        move_block_down(canvas, root, "IV0", 300)
        root.after(2000, lambda: (canvas.delete("arrow1"), canvas.delete("IV0"), canvas.itemconfigure("Key0_text", text="0010"), canvas.itemconfigure("Key0_rect", outline=cf.Block_colours["keystream"])))
        root.after(2100, lambda: move_block_down(canvas, root, "IV1", 300))
        root.after(4100, lambda: (canvas.delete("arrow2"), canvas.delete("IV1"),canvas.itemconfigure("Key1_text", text="0011"), canvas.itemconfigure("Key1_rect", outline=cf.Block_colours["keystream"])))
        root.after(4200, lambda: move_block_down(canvas, root, "IV2", 300))
        root.after(6200, lambda: (canvas.delete("arrow3"), canvas.delete("IV2"),canvas.itemconfigure("Key2_text", text="0100"),canvas.itemconfigure("Key2_rect", outline=cf.Block_colours["keystream"])))
        root.after(6200, lambda: (info_lbl.config(text="Which gives us 3 keystream blocks"), unlock_buttons(next_btn, prev_btn)))

    def step_3():
        # Setting up the screen
        PT1 = ["0", "0", "0", "1"]
        KS1 = ["0", "0", "1", "0"]
        CT1 = ["0", "0", "1", "1"]
        lock_buttons(next_btn, prev_btn)
        info_lbl.config(text="")
        canvas.delete("all")
        canvas.create_text(W / 2, 30, text="Encryption of PT block 1", fill=c["text"], font=cf.Fonts["title"])
        info_lbl.config(text="First plaintext block XORed with the first keystream")
        next_block_center = W / 2 - 45
        for i in range(4):
            PT_block_tag = "PT_Char" + str(i)
            KS_block_tag = "KS_Char" + str(i)
            draw_block(canvas, root, next_block_center, 100, PT1[i] , cf.Block_colours["plaintext"], 2, PT_block_tag)
            draw_block(canvas, root, next_block_center, 300, KS1[i], cf.Block_colours["keystream"], 2, KS_block_tag)
            next_block_center = next_block_center + 30
        canvas.create_text(200, 100, text="Plaintext:", fill=c["text"], font=cf.Fonts["label"])
        canvas.create_text(200, 300, text="Keystream:", fill=c["text"], font=cf.Fonts["label"])
        canvas.create_text(200, 200, text="XOR", fill=c["text"], font=cf.Fonts["operation"])
        start_delay = 500
        start_x = 330
        for x in range(4):
            PT_block_tag_to_move = "PT_Char" + str(x)
            KS_block_tag_to_move = "KS_Char" + str(x)
            root.after(start_delay, lambda pt=PT_block_tag_to_move, ks=KS_block_tag_to_move: (move_block_down(canvas, root, pt, 200), move_block_up(canvas, root, ks, 200)))
            root.after(start_delay + 1000, lambda pt=PT_block_tag_to_move, ks=KS_block_tag_to_move: (canvas.delete(pt),canvas.delete(ks)))
            root.after(start_delay + 1100, lambda x_pos=start_x, txt = CT1[x]: (draw_block(canvas, root, x_pos, 200, txt, cf.Block_colours["ciphertext"], 2, "CT")))
            start_delay += 1000
            start_x += 30
        root.after(5000, lambda: (info_lbl.config(text="Giving us our first ciphertext block"), unlock_buttons(next_btn, prev_btn)))

    def step_4():
        info_lbl.config(text="")
        col_width = W / 3
        delay = 0
        canvas.delete("all")
        lock_buttons(next_btn, prev_btn)
        canvas.create_text(W / 2, 30, text="Encryption", fill=c["text"], font=cf.Fonts["title"])
        info_lbl.config(text="The other plaintext blocks are XORed with their respective keystream\ngiving us the following full ciphertext")
        for i in range(3):
            x_center = col_width * i + col_width / 2
            text = "Ciphertext Block " + str(i+1)
            canvas.create_text(x_center, 250, text=text, fill=c["text"], font=cf.Fonts["label"])

        for i in range(3):
            x_center = col_width * i + col_width / 2
            root.after(delay, lambda x = x_center, txt = Full_CT[i]: draw_block(canvas, root, x, 300, txt, cf.Block_colours["ciphertext"], 1, "CipherText"))
            delay = delay + 1000

        root.after(2800, lambda: unlock_buttons(next_btn, prev_btn))

    def step_5():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
                           text="This ciphertext is then sent to the recipient alongside the IV\n"
                                "Using CTR is simple, however it is not as secure as it can be.\n\n"
                                "In future lessons, GCM will be explored, which is a mode of operation\n"
                                "that builds upon CTR by adding authentication",
                           font=cf.Fonts["body"],
                           fill=c["text"],
                           anchor="center",
                           justify="center")

    def step_6():
        canvas.delete("all")
        info_lbl.config(text="")
        canvas.create_text(W / 2, H / 2,
                           text="Lesson complete! Press next to take the quiz",
                           font=cf.Fonts["title"],
                           fill=c["text"],
                           anchor="center",
                           justify="center"
        )

    return [step_0, step_1, step_2, step_3, step_4, step_5, step_6]


