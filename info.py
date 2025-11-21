import tkinter as tk
import subprocess
import sys
import os

# ==============================
RULES_TEXT = """
    Background info (rules at the bottom)
    Mental Health is a very big factor in our life. It impacts what we do, and the efficiency we do it in. 
    there are a lot of factors which decide your mental health and some of them are Stress, Energy, Mood,
    and Social Connection. For example if you dont study for a test you have tomorrow you are going
    to be stressed about it. Or if you stay up until 2 am and you have school tomorrow, 
    you are probably going to be very tired which can impact how well you do on your
    test. 
    
    How to play the game
    1. Click the play button
    2. The bars on top act like health bars the following bars increase: Energy, Mood, Social Connection.
    The Stress bar decreases (less stress the better)
    3. The buttons are decisions which you make, each decision has different impacts
    4. after clicking a button you will see to the left of the bar a added ammount or a decrease 
    (REMEMBER STRESS DECREASING IS GOOD)
    5. If a bar drops to zero (other than stress which if gets to 100) then you lose

    Citations (Cited in MLA)
    Centers for Disease Control and Prevention. Mental Health. CDC, 12 Oct. 2023, www.cdc.gov/healthy-youth/mental-health/index.html.
    World Health Organization. Adolescent Mental Health. WHO, 24 Mar. 2023, www.who.int/news-room/fact-sheets/detail/adolescent-mental-health.
    Annie E. Casey Foundation. Youth Mental Health Statistics. AECF, 15 Feb. 2023, www.aecf.org/blog/youth-mental-health-statistics.
    Office of Population Affairs, U.S. Department of Health & Human Services. Mental Health in Adolescents. OPA, 2023, opa.hhs.gov/adolescent-health/mental-health-adolescents.
    Centers for Disease Control and Prevention. Mental Health Numbers. CDC, 12 Oct. 2023, www.cdc.gov/healthy-youth/mental-health/mental-health-numbers.html.
    Centers for Disease Control and Prevention. Children’s Mental Health: Data & Research. CDC, 2023, www.cdc.gov/children-mental-health/data-research/index.html.
    Compass Health Center. Teen Mental Health Statistics. Compass Health Center, 10 Jan. 2023, compasshealthcenter.net/blog/teen-mental-health-statistics/.
    Author(s) Not Listed. “Title Not Provided.” arXiv, 13 June 2023, arxiv.org/abs/2306.06552.
    Author(s) Not Listed. “Title Not Provided.” arXiv, 25 Aug. 2025, arxiv.org/abs/2508.10062.
"""
# ==============================

def back_to_menu():

    script_path = os.path.join(os.path.dirname(__file__), "StartMenu.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

root = tk.Tk()
root.title("Information")
root.geometry("600x500")


back_button = tk.Button(root, text="Back to Main Menu", font=("Arial", 14),
                        command=back_to_menu)
back_button.pack(pady=10)


frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)


text_widget = tk.Text(frame, wrap="none", font=("Arial", 12))
text_widget.insert("1.0", RULES_TEXT)
text_widget.config(state="disabled")  # Read-only
text_widget.pack(side="left", fill="both", expand=True)

v_scroll = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
v_scroll.pack(side="right", fill="y")
text_widget.config(yscrollcommand=v_scroll.set)

h_scroll = tk.Scrollbar(root, orient="horizontal", command=text_widget.xview)
h_scroll.pack(fill="x")
text_widget.config(xscrollcommand=h_scroll.set)

text_widget.xview_moveto(0)

root.mainloop()
