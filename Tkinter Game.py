import tkinter as tk
from tkinter import messagebox
import random

# Global high scores
PL1_HIGH_SCORE = 0
PL2_HIGH_SCORE = 0

# Winning rules
win = {1: 3, 2: 1, 3: 2}
choice_names = {1: "Rock", 2: "Paper", 3: "Scissors"}


class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.num_players = tk.IntVar(value=1)
        self.num_games = tk.IntVar(value=3)

        self.current_round = 0
        self.pl1_total = 0
        self.pl2_total = 0

        self.player1_choice = None
        self.player2_choice = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Rock Paper Scissors", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        mode_frame = tk.LabelFrame(self.root, text="Game Settings", padx=10, pady=10)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Number of Players:").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(mode_frame, text="1 Player", variable=self.num_players, value=1, command=self.reset_game).grid(row=0, column=1)
        tk.Radiobutton(mode_frame, text="2 Players", variable=self.num_players, value=2, command=self.reset_game).grid(row=0, column=2)

        tk.Label(mode_frame, text="Number of Rounds:").grid(row=1, column=0, sticky="w")
        tk.Entry(mode_frame, textvariable=self.num_games, width=10).grid(row=1, column=1, pady=5)

        self.round_label = tk.Label(self.root, text="Round: 0", font=("Arial", 12))
        self.round_label.pack()

        self.score_label = tk.Label(self.root, text="Score - Player1: 0 | Player2/Computer: 0", font=("Arial", 12))
        self.score_label.pack(pady=5)

        self.high_score_label = tk.Label(self.root, text="High Scores - Player1: 0 | Player2: 0", font=("Arial", 12))
        self.high_score_label.pack(pady=5)

        self.info_label = tk.Label(self.root, text="Choose Rock, Paper, or Scissors", font=("Arial", 14, "bold"))
        self.info_label.pack(pady=10)

        self.choice_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.choice_label.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Rock", width=12, command=lambda: self.play(1)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Paper", width=12, command=lambda: self.play(2)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Scissors", width=12, command=lambda: self.play(3)).grid(row=0, column=2, padx=5)

        self.reset_button = tk.Button(self.root, text="Reset Game", width=15, command=self.reset_game)
        self.reset_button.pack(pady=10)

    def play(self, pl1_choice):
        global PL1_HIGH_SCORE, PL2_HIGH_SCORE

        if self.num_games.get() <= 0:
            messagebox.showerror("Invalid Input", "Number of rounds must be greater than 0.")
            return

        if self.current_round >= self.num_games.get():
            messagebox.showinfo("Game Over", "This game is already finished. Please reset to play again.")
            return

        self.current_round += 1

        if self.num_players.get() == 1:
            pl2_choice = random.randint(1, 3)
        else:
            # Simple 2-player version in same GUI:
            pl2_choice = self.ask_player2_choice()
            if pl2_choice is None:
                self.current_round -= 1
                return

        player1_text = choice_names[pl1_choice]
        player2_text = choice_names[pl2_choice]

        if pl1_choice == pl2_choice:
            result = "TIE"
        elif win[pl1_choice] == pl2_choice:
            result = "PLAYER1 WINS THIS ROUND"
            self.pl1_total += 1
            PL1_HIGH_SCORE = max(PL1_HIGH_SCORE, self.pl1_total)
        else:
            result = "PLAYER2 WINS THIS ROUND"
            self.pl2_total += 1
            PL2_HIGH_SCORE = max(PL2_HIGH_SCORE, self.pl2_total)

        self.choice_label.config(
            text=f"Player1 chose: {player1_text}\nPlayer2/Computer chose: {player2_text}\n\n{result}"
        )

        self.update_labels()

        if self.current_round == self.num_games.get():
            self.show_final_winner()

    def ask_player2_choice(self):
        choice_window = tk.Toplevel(self.root)
        choice_window.title("Player 2 Choice")
        choice_window.geometry("300x200")
        choice_window.resizable(False, False)
        choice_window.grab_set()

        selected_choice = tk.IntVar(value=0)

        tk.Label(choice_window, text="Player 2: Choose your move", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Radiobutton(choice_window, text="Rock", variable=selected_choice, value=1).pack()
        tk.Radiobutton(choice_window, text="Paper", variable=selected_choice, value=2).pack()
        tk.Radiobutton(choice_window, text="Scissors", variable=selected_choice, value=3).pack()

        def confirm():
            if selected_choice.get() not in [1, 2, 3]:
                messagebox.showerror("Invalid Choice", "Please select a valid choice.")
                return
            choice_window.destroy()

        tk.Button(choice_window, text="Confirm", command=confirm).pack(pady=10)

        self.root.wait_window(choice_window)

        if selected_choice.get() in [1, 2, 3]:
            return selected_choice.get()
        return None

    def update_labels(self):
        global PL1_HIGH_SCORE, PL2_HIGH_SCORE

        self.round_label.config(text=f"Round: {self.current_round}/{self.num_games.get()}")
        self.score_label.config(
            text=f"Score - Player1: {self.pl1_total} | Player2/Computer: {self.pl2_total}"
        )
        self.high_score_label.config(
            text=f"High Scores - Player1: {PL1_HIGH_SCORE} | Player2: {PL2_HIGH_SCORE}"
        )

    def show_final_winner(self):
        if self.pl1_total > self.pl2_total:
            final_result = "PLAYER1 is the WINNER of this Game!"
        elif self.pl1_total < self.pl2_total:
            final_result = "PLAYER2 is the WINNER of this Game!"
        else:
            final_result = "It's a TIE!"

        messagebox.showinfo("Final Result", final_result)

    def reset_game(self):
        self.current_round = 0
        self.pl1_total = 0
        self.pl2_total = 0
        self.choice_label.config(text="")
        self.update_labels()


root = tk.Tk()
app = RockPaperScissorsGUI(root)
root.mainloop()