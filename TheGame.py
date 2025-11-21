import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import subprocess
import sys

# Difficulty Setup
difficulty = os.environ.get("GAME_DIFFICULTY", "Normal")

if difficulty == "Easy":
    start_value = 70
elif difficulty == "Hard":
    start_value = 20
else:
    start_value = 50

#stats adjustment
stats = {
    "Stress": 80 if difficulty == "Hard" else start_value,
    "Energy": start_value,
    "Mood": start_value,
    "Social Connection": start_value
}
last_change = {stat: 0 for stat in stats}

# Facts for bottom display which are chosen randomly
facts = [
    "Globally, about 1 in 7 adolescents experience a mental health disorder.",
    "In the U.S., 4 in 10 high school students reported persistent sadness or hopelessness in 2023.",
    "Nearly 18% of youth ages 12 to 17 had at least one major depressive episode in the past year.",
    "Feeling connected to school or peers is a protective factor against poor mental health.",
    "About 20% of adolescents reported having unmet mental health care needs.",
    "Anxiety disorders affect an estimated 31.9% of teens.",
    "Bullying victims are significantly more likely to experience anxiety, depression and poor sleep quality.",
    "Adolescents who feel supported are less likely to experience mental disorders.",
    "Excessive screen time (4+ hours) is linked to higher risk of anxiety and depression among teens.",
    "Early action and good habits in adolescence can reduce the impact of mental health conditions in adulthood."
]


# Scenarios which randomly cycle through in game
scenarios = [
    {
        "text": "You have a big science project due tomorrow.",
        "choices": [
            ("Study all night", {"Stress": +15, "Energy": -20, "Mood": -5},
             "Studying all night increases stress and reduces energy, which can hurt performance."),
            ("Study 2 hours, then sleep", {"Stress": -5, "Energy": +5, "Mood": +5},
             "Studying a bit then resting reduces stress and improves mood—balanced approach!"),
            ("Ignore it", {"Stress": -10, "Mood": +10, "Social Connection": -5},
             "Ignoring work lowers stress short term but may affect grades and trust from others.")
        ]
    },
    {
        "text": "Your friend asks for help with homework.",
        "choices": [
            ("Help them", {"Social Connection": +15, "Energy": -10, "Stress": -5},
             "Helping friends strengthens social bonds, even if a bit tiring."),
            ("Say no, study yourself", {"Stress": +5, "Mood": -5},
             "Prioritizing yourself is fine, but may slightly affect relationships."),
            ("Ignore them", {"Social Connection": -10, "Mood": -5},
             "Ignoring friends can harm relationships and mood over time.")
        ]
    },
    {
        "text": "You have a soccer game today but you feel tired.",
        "choices": [
            ("Play anyway", {"Energy": -15, "Mood": +10, "Stress": +5},
             "Pushing yourself can boost mood but drains energy and increases stress."),
            ("Skip practice", {"Stress": -5, "Mood": -5, "Social Connection": -10},
             "Resting reduces stress, but missing social activity affects connections."),
            ("Go watch friends play", {"Social Connection": +5, "Energy": -5, "Mood": +5},
             "Supporting friends helps social bonds with minimal energy loss.")
        ]
    },
    {
        "text": "You feel overwhelmed by social media.",
        "choices": [
            ("Take a break", {"Stress": -10, "Mood": +5, "Social Connection": 0},
             "Short breaks let your mind relax, reducing stress and improving mood."),
            ("Keep scrolling", {"Mood": -10, "Stress": +5},
             "Overuse of social media can increase stress and lower mood."),
            ("Post something funny", {"Social Connection": +10, "Mood": +5},
             "Positive interactions online can boost mood and social connection.")
        ]
    },
    {
        "text": "A friend invites you to their birthday party.",
        "choices": [
            ("Go", {"Social Connection": +20, "Energy": -10, "Stress": -5},
             "Socializing reduces stress and strengthens friendships."),
            ("Stay home and relax", {"Stress": -10, "Mood": +10, "Social Connection": -5},
             "Resting helps mood and stress but can slightly reduce social connections."),
            ("Study instead", {"Stress": +5, "Mood": -5},
             "Prioritizing work can increase stress and lower mood.")
        ]
    },
    {
        "text": "You get in trouble with a teacher and the teacher is angry at you.",
        "choices": [
            ("Talk to teacher", {"Stress": -5, "Social Connection": +5, "Mood": 0},
             "Addressing conflict calmly reduces stress and improves relationships."),
            ("Ignore it", {"Stress": +10, "Mood": -5},
             "Ignoring conflicts can increase stress and hurt mood."),
            ("Complain to friends", {"Social Connection": +5, "Stress": +5},
             "Sharing feelings helps connections but may increase stress slightly.")
        ]
    },
    {
        "text": "You forgot to study for a quiz, and you come into the classroom and remember about it.",
        "choices": [
            ("Cram last minute", {"Stress": +15, "Energy": -10, "Mood": -5},
             "Cramming can increase stress and reduce energy."),
            ("Accept grade", {"Stress": -5, "Mood": -5},
             "Accepting outcomes reduces stress but may lower mood slightly."),
            ("Ask friend to explain", {"Social Connection": +10, "Mood": +5, "Stress": -5},
             "Getting help strengthens social bonds and reduces stress.")
        ]
    },
    {
        "text": "You feel lonely during lunch.",
        "choices": [
            ("Invite yourself to a table", {"Social Connection": +10, "Stress": -5},
             "Taking initiative improves connections and reduces stress."),
            ("Stay alone", {"Mood": -10, "Stress": +5},
             "Isolation can decrease mood and slightly increase stress."),
            ("Do something fun alone", {"Mood": +5, "Stress": -5},
             "Alone time can improve mood and reduce stress.")
        ]
    },
    {
        "text": "You have a speech you have to perform to your class.",
        "choices": [
            ("Practice intensively", {"Stress": +10, "Energy": -10, "Mood": +5},
             "Preparation improves confidence but increases stress and energy use."),
            ("Practice moderately", {"Stress": -5, "Mood": +5},
             "Balanced practice reduces stress and maintains mood."),
            ("Skip practice", {"Stress": -5, "Mood": -5},
             "Skipping practice reduces stress short term but may lower mood.")
        ]
    },
    {
        "text": "Your phone dies and you do not have a charger on you.",
        "choices": [
            ("Stay calm", {"Stress": -5, "Mood": +5},
             "Remaining calm reduces stress and improves mood."),
            ("Panic", {"Stress": +10, "Mood": -5},
             "Panic increases stress and lowers mood."),
            ("Borrow charger from friend", {"Social Connection": +5, "Stress": -5},
             "Getting help strengthens social connection and reduces stress.")
        ]
    },
    {
        "text": "You feel sick before school.",
        "choices": [
            ("Go anyway", {"Energy": -10, "Stress": +5, "Mood": -5},
             "Pushing through illness reduces energy and mood."),
            ("Stay home and rest", {"Energy": +10, "Stress": -5},
             "Resting restores energy and reduces stress."),
            ("Go but tell no one", {"Mood": -5, "Stress": +5},
             "Hiding illness increases stress and reduces mood.")
        ]
    },
    {
        "text": "One of your friends starts to spread rumors about you.",
        "choices": [
            ("Confront them", {"Stress": +5, "Social Connection": -5},
             "Addressing the issue may increase stress but can protect relationships."),
            ("Ignore it", {"Stress": +5, "Mood": -5},
             "Ignoring can increase stress and reduce mood."),
            ("Talk to trusted friend", {"Social Connection": +5, "Stress": -5},
             "Seeking support reduces stress and strengthens connections.")
        ]
    },
    {
        "text": "Someone invites you to join a new club.",
        "choices": [
            ("Join", {"Social Connection": +15, "Stress": +5},
             "Trying new activities boosts connections but may increase stress initially."),
            ("Decline", {"Stress": -5, "Mood": -5},
             "Declining reduces stress but slightly lowers mood."),
            ("Research first", {"Mood": +5, "Stress": -5},
             "Planning ahead reduces stress and improves confidence.")
        ]
    },
    {
        "text": "You break a picture of you and your parents.",
        "choices": [
            ("Admit it", {"Stress": +5, "Social Connection": +5, "Mood": -5},
             "Being honest slightly increases stress but improves relationships."),
            ("Hide it", {"Stress": +10, "Mood": -5},
             "Hiding increases stress and reduces mood."),
            ("Blame sibling", {"Social Connection": -5, "Stress": +5},
             "Blaming harms social connections and increases stress.")
        ]
    },
    {
        "text": "You were given a lot of homework tonight.",
        "choices": [
            ("Work all night", {"Stress": +15, "Energy": -20, "Mood": -5},
             "Pulling all nighters increases stress and reduces energy."),
            ("Prioritize a few", {"Stress": -5, "Mood": +5, "Energy": -5},
             "Prioritizing tasks reduces stress and maintains mood."),
            ("Skip it", {"Stress": -10, "Mood": +5, "Social Connection": -5},
             "Skipping lowers stress temporarily but affects performance and social bonds.")
        ]
    },
    {
        "text": "You are feeling anxious before a presentation.",
        "choices": [
            ("Practice in front of mirror", {"Stress": -5, "Mood": +5},
             "Preparation reduces stress and boosts confidence."),
            ("Wing it", {"Stress": +10, "Mood": -5},
             "Not preparing increases stress and reduces mood."),
            ("Ask friend to practice", {"Social Connection": +5, "Stress": -5},
             "Practicing with friends reduces stress and strengthens connections.")
        ]
    },
    {
        "text": "You witness bullying.",
        "choices": [
            ("Intervene", {"Social Connection": +10, "Stress": +5, "Mood": +5},
             "Helping others strengthens connections and mood, though a bit stressful."),
            ("Ignore", {"Stress": -5, "Mood": -5},
             "Ignoring reduces immediate stress but may reduce mood."),
            ("Comfort later", {"Social Connection": +5, "Mood": +5},
             "Providing support later boosts connections and mood.")
        ]
    },
    {
        "text": "You want to start exercising.",
        "choices": [
            ("Go to gym", {"Energy": -10, "Mood": +10, "Stress": -5},
             "Exercise reduces stress and improves mood, though it costs energy."),
            ("Walk around", {"Energy": -5, "Mood": +5},
             "Light activity improves mood and slightly uses energy."),
            ("Skip", {"Mood": -5, "Stress": +5},
             "Skipping activity may slightly worsen mood and stress.")
        ]
    },
    {
        "text": "You want to improve grades on a certain subject.",
        "choices": [
            ("Study extra", {"Stress": +5, "Energy": -10, "Mood": +5},
             "Extra study can improve grades but slightly increases stress."),
            ("Ask for tutor", {"Social Connection": +5, "Stress": -5},
             "Getting help reduces stress and strengthens connections."),
            ("Ignore it", {"Mood": -5, "Stress": +5},
             "Ignoring studies may increase stress and lower mood.")
        ]
    }
]

used_scenarios = []

root = tk.Tk()
root.title("Balance – Mental Health Journey")
root.geometry("650x600")

stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

bars = {}
change_labels = {}

style = ttk.Style()
style.theme_use('default')
style.configure("Red.Horizontal.TProgressbar", troughcolor='gray', background='red')
style.configure("Orange.Horizontal.TProgressbar", troughcolor='gray', background='orange')
style.configure("Green.Horizontal.TProgressbar", troughcolor='gray', background='green')
style.configure("BrightGreen.Horizontal.TProgressbar", troughcolor='gray', background='#4CAF50')
style.configure("BlueGreen.Horizontal.TProgressbar", troughcolor='gray', background='#009688')
style.configure("Blue.Horizontal.TProgressbar", troughcolor='gray', background='blue')
style.configure("LightBlue.Horizontal.TProgressbar", troughcolor='gray', background='#03A9F4')
style.configure("Gray.Horizontal.TProgressbar", troughcolor='gray', background='gray')

def update_bar_color(bar, stat_name, value):
    if stat_name == "Stress":
        if value > 75:
            bar.configure(style="Red.Horizontal.TProgressbar")
        elif value > 50:
            bar.configure(style="Orange.Horizontal.TProgressbar")
        else:
            bar.configure(style="Green.Horizontal.TProgressbar")
    elif stat_name == "Energy":
        if value > 75:
            bar.configure(style="BrightGreen.Horizontal.TProgressbar")
        elif value > 50:
            bar.configure(style="Green.Horizontal.TProgressbar")
        else:
            bar.configure(style="Red.Horizontal.TProgressbar")
    elif stat_name == "Mood":
        if value > 75:
            bar.configure(style="BlueGreen.Horizontal.TProgressbar")
        elif value > 50:
            bar.configure(style="Green.Horizontal.TProgressbar")
        else:
            bar.configure(style="Gray.Horizontal.TProgressbar")
    elif stat_name == "Social Connection":
        if value > 75:
            bar.configure(style="Blue.Horizontal.TProgressbar")
        elif value > 50:
            bar.configure(style="LightBlue.Horizontal.TProgressbar")
        else:
            bar.configure(style="Red.Horizontal.TProgressbar")

def create_stat_bar(name):
    row = tk.Frame(stats_frame)
    row.pack()
    change_lbl = tk.Label(row, text="  ", font=("Arial", 10), width=4)
    change_lbl.pack(side="left")
    change_labels[name] = change_lbl
    label = tk.Label(row, text=name, width=15, anchor="w")
    label.pack(side="left")
    bar = ttk.Progressbar(row, length=300, maximum=100)
    bar["value"] = stats[name]
    bar.pack(side="left")
    bars[name] = bar
    update_bar_color(bar, name, stats[name])

for s in stats:
    create_stat_bar(s)

scenario_text = tk.Label(root, text="", wraplength=600, font=("Arial", 12))
scenario_text.pack(pady=15)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

fact_label = tk.Label(root, text="", font=("Arial", 10), wraplength=600, justify="left", fg="gray")
fact_label.pack(pady=5)

buttons = []

def go_to_main_menu():
    script_path = os.path.join(os.path.dirname(__file__), "StartMenu.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

def game_over(message):
    for b in buttons:
        b.destroy()
    buttons.clear()
    scenario_text.config(text=message)


    restart_btn = tk.Button(button_frame, text="Restart Game", width=30, font=("Arial", 14),
                            command=restart_game)
    restart_btn.pack(pady=5)
    buttons.append(restart_btn)


    menu_btn = tk.Button(button_frame, text="Main Menu", width=30, font=("Arial", 14),
                         command=go_to_main_menu)
    menu_btn.pack(pady=5)
    buttons.append(menu_btn)

def check_game_over():

    if stats["Stress"] >= 100:
        game_over("💥 Your stress reached overwhelming levels. You couldn't cope anymore. Game Over.")
        return True


    for stat, value in stats.items():
        if value <= 0:
            if stat == "Stress":
                msg = "You were overwhelmed by stress and couldn't cope. Game Over."
            elif stat == "Energy":
                msg = "You suffered severe sleep deprivation and could no longer continue. Game Over."
            elif stat == "Mood":
                msg = "You felt extremely down and lost motivation to continue. Game Over."
            elif stat == "Social Connection":
                msg = "You felt completely isolated and disconnected from friends. Game Over."
            game_over(msg)
            return True


    for stat, value in stats.items():
        if stat != "Stress" and value >= 100:
            game_over("🎉 Congrats! You built a strong healthy stat! You Win!")
            return True

    return False

def apply_changes(changes, explanation):
    for stat in last_change:
        last_change[stat] = changes.get(stat, 0)
    for stat, value in changes.items():
        stats[stat] = max(0, min(100, stats[stat] + value))
    for stat in stats:
        bars[stat]["value"] = stats[stat]
        update_bar_color(bars[stat], stat, stats[stat])
        change = last_change[stat]
        if change > 0:
            change_labels[stat].config(text=f"+{change}", fg="green")
        elif change < 0:
            change_labels[stat].config(text=f"{change}", fg="red")
        else:
            change_labels[stat].config(text="  ")


    fact_label.config(text="💡 Fact: " + random.choice(facts))


    if explanation:
        popup = tk.Toplevel(root)
        popup.title("Why this choice?")
        popup.geometry("450x200")
        tk.Label(popup, text=explanation, font=("Arial", 12), wraplength=400, justify="left").pack(padx=20, pady=20)

        def continue_scenario():
            popup.destroy()
            if not check_game_over():
                new_scenario()

        tk.Button(popup, text="Continue", font=("Arial", 12), command=continue_scenario).pack(pady=10)
        popup.grab_set()
    else:
        if not check_game_over():
            new_scenario()

def new_scenario():
    global used_scenarios
    if len(used_scenarios) == len(scenarios):
        used_scenarios = []
    available = [s for s in scenarios if s not in used_scenarios]
    current = random.choice(available)
    used_scenarios.append(current)

    for b in buttons:
        b.destroy()
    buttons.clear()

    scenario_text.config(text=current["text"])
    fact_label.config(text="💡 Fact: " + random.choice(facts))

    for text, effects, explanation in current["choices"]:
        btn = tk.Button(button_frame, text=text, width=50,
                        command=lambda eff=effects, exp=explanation: apply_changes(eff, exp))
        btn.pack(pady=5)
        buttons.append(btn)

def restart_game():
    global used_scenarios
    used_scenarios = []
    if difficulty == "Easy":
        start_val = 70
    elif difficulty == "Hard":
        start_val = 20
    else:
        start_val = 50
    for stat in stats:
        stats[stat] = start_val
        bars[stat]["value"] = start_val
        update_bar_color(bars[stat], stat, start_val)
        change_labels[stat].config(text="  ")
    new_scenario()

new_scenario()
root.mainloop()
