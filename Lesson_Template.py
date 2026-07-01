# New Lesson Checklist:
# Create Button on Lessons Page
# Fill in Quiz Questions
# Import into Main
# Add Button to Widgets List
# Add Lesson to 'Complete' Function

from Utils import draw_block, move_block_up, move_block_down, get_dark_mode, lock_buttons, unlock_buttons, move_block_right
import config as cf

quiz_questions = [
        {
            "question": "",
            "answers": ["", "", ""],
            "correct": 0
        },
        {
            "question": "",
            "answers": ["", "", ""],
            "correct": 0
        },
        {
            "question": "",
            "answers": ["", "", ""],
            "correct": 0
        }
]

def get_steps(canvas, root, info_lbl, next_btn, prev_btn):
    W = 750
    H = 600
    c = get_dark_mode()

    def step_0():
        canvas.delete("all")
        info_lbl.config(text="")


    return [step_0]