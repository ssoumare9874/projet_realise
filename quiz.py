import tkinter as tk
from tkinter import messagebox
import json
import os

# Fonction pour charger les questions depuis le fichier JSON
def load_questions_from_json(filename="questions.json"):
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier {filename} n'a pas été trouvé.")
        return []
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print("Questions chargées avec succès !")  # Message de débogage
            return data
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {filename} est mal formé.")
        return []

# Variables globales
questions = load_questions_from_json()  # Charger les questions depuis le fichier JSON
current_question = 0
score = 0

# Vérification que le fichier JSON est correctement chargé
if not questions:
    print("Aucune question disponible. Veuillez vérifier le fichier JSON.")
    exit()  # Si le fichier JSON ne se charge pas, le programme s'arrête.

# Fonction pour vérifier la réponse
def check_answer(answer):
    global score, current_question

    if answer == questions[current_question]["answer"]:
        score += 1
    
    current_question += 1
    if current_question < len(questions):
        load_question()
    else:
        show_result()

# Fonction pour charger la question suivante
def load_question():
    question_label.config(text=questions[current_question]["question"])
    score_label.config(text=f"Score: {score}/{len(questions)}")
    
    for i, option in enumerate(questions[current_question]["options"]):
        buttons[i].config(text=option, command=lambda ans=option: check_answer(ans))

# Fonction pour afficher le résultat final
def show_result():
    messagebox.showinfo("Quiz terminé", f"Votre score est de {score}/{len(questions)}")
    restart_game()

# Fonction pour quitter l'application avec confirmation
def quit_game():
    response = messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter le jeu ?")
    if response:
        root.quit()

# Fonction pour réinitialiser le quiz
def restart_game():
    global score, current_question
    score = 0
    current_question = 0
    load_question()

# Création de la fenêtre principale
root = tk.Tk()
root.config(bg='#74FDFF')
root.title("Jeu de Quiz")
root.geometry("500x400")

# Création de la Frame pour contenir les widgets
frame = tk.Frame(root,  bg='#74FDFF', bd=2, relief='sunken')
frame.pack(expand='yes', pady=30,padx=30)

# Ajout des widgets dans la Frame
score_label = tk.Label(frame, text=f"Score: {score}/{len(questions)}",bg='#74FDFF',fg='#397C7D', font=("Arial", 15))
score_label.pack(pady=10)

question_label = tk.Label(frame, text="", font=("Arial", 14), wraplength=400,fg='#397C7D')
question_label.pack(pady=20)

buttons = []
for i in range(4):
    btn = tk.Button(frame, text="",bg='#397C7D', font=("Arial", 12), width=30, height=2)
    btn.pack(pady=5)
    buttons.append(btn)

# Création des boutons Quitter et Réinitialiser en dehors de la Frame
quit_button = tk.Button(root, text="Quitter",fg='white', font=("Arial", 12), command=quit_game)
quit_button.pack(side="left", padx=20, pady=20)

restart_button = tk.Button(root, text="Réinitialiser",bg='#397C7D',fg='white', font=("Arial", 12), command=restart_game)
restart_button.pack(side="right", padx=20, pady=20)

# Chargement de la première question
load_question()

# Lancement de l'application
root.mainloop()
