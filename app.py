from tkinter import *
from random import randint
from math import floor

class App:
    def __init__(self, window):
        # Loading highscore from file and initializing score (new_highscore is initialized
        # to ensure that the "highscore" is updated in game when the score surpasses it)
        with open("highscore.txt", "r") as file:
            self.highscore = int(file.read())
        self.score = 0
        self.new_highscore = self.highscore

        #  ---------------------------------------UI SETUP---------------------------------------
        self.window = window
        self.window.title("Quick Math!")
        self.window.config(background="lightblue")
        self.window.minsize(400, 400)

        self.welcome_label = Label(self.window, text="Welcome to Quick Math!\nPress Start to continue.\nGood luck!",
                              font=("Times New Roman", 28, "normal"), bg="lightblue")
        self.welcome_label.grid(row=2, column=2, padx=50, pady=50)

        self.start_button = Button(self.window, text="Start", width=15, height=2, font=("Times New Roman", 12, "normal"), bg="lightgreen",
                              command=self.show_question)
        self.start_button.grid(row=3, column=2, padx=50, pady=50)
        # -----------------------------------------------------

        # Initializing relevant widgets, and the two multiplicands a and b (they start off as None)
        self.a, self.b, self.question_label, self.user_input, self.timer_label, self.score_label, self.highscore_label = [None] * 7
        self.game_over_label, self.restart_button = None, None
        self.timer = None

        # Will toggle if user failed the question instead of letting time run out. Can you find out why?
        self.user_missed = False

    # Function to end the game!
    def end_game(self):
        # Code to clear the screen completely!
        for widget in self.window.winfo_children():
            widget.destroy()

        # Updating user's highscore
        self.highscore = max(self.highscore, self.score)
        with open('highscore.txt', "w") as file:
            file.write(str(self.highscore))

        #  ----------------------------------GAME OVER SCREEN SETUP----------------------------------
        self.game_over_label = Label(self.window,
            text=f"{'Nope!' if self.user_missed else 'Time up!'} The answer was {self.a * self.b}.\n"
                 f"Your score was {self.score}, and your \n{'new' if self.score > self.highscore else ''} highscore "
                 f"{'remains' if self.highscore >= self.score else 'is'} {self.highscore}."
                 f"\n\nTry again?", font=("Times New Roman", 28, "normal"), bg="lightblue")
        self.game_over_label.grid(row=2, column=2, padx=50, pady=50)

        self.restart_button = Button(self.window, text="Restart", width=15, height=2, font=("Times New Roman", 12, "normal"),
                                bg="lightgreen",
                                command=self.show_question)
        self.restart_button.grid(row=3, column=2, padx=50, pady=50)

        # Resetting self.score in case user wants to restart
        self.score = 0

    # Function to show each question
    def show_question(self):
        # Code to clear the screen permanently!
        for widget in self.window.winfo_children():
            widget.destroy()

        # Choosing random numbers to ask the user to multiply
        self.a = randint(10, 25)
        self.b = randint(10, 25)

        # ------------------------------------------QUESTION SCREEN SETUP--------------------------------------
        self.question_label = Label(self.window, text=f"{self.score + 1}. {self.a} x {self.b} = ", font=("Yu Gothic", 28, "normal"), bg="lightblue")
        self.question_label.place(relx=0.15, rely=0.4)

        self.user_input = Entry(self.window, width=5, font=("Yu Gothic", 20))
        self.user_input.place(relx=0.63, rely=0.42)

        # Code to ensure the cursor is ever-present at the beginning of the entry box
        self.user_input.focus()
        self.user_input.icursor(0)

        # Line of code that binds the "Enter" key to the function that checks the answer
        self.user_input.bind("<Return>", self.check_answer)

        self.timer_label = Label(self.window, text=f"5.00", font=("Yu Gothic", 25, "normal"), bg="lightblue")
        self.timer_label.place(relx=0.79, rely=0.1)

        self.score_label = Label(self.window, text=f"Score: {self.score}", font=("Yu Gothic", 20, "normal"), bg="lightblue")
        self.score_label.place(relx=0.09, rely=0.8)

        self.highscore_label = Label(self.window, text=f"High Score: {self.new_highscore}", font=("Yu Gothic", 20, "normal"), bg="lightblue")
        self.highscore_label.place(relx=0.59, rely=0.8)

        self.count_down(5.00)

    # Function that checks user's answer
    def check_answer(self, event):
        self.window.after_cancel(self.timer)
        answer = int(self.user_input.get())

        if self.a * self.b == answer:
            self.score += 1
            if self.score > self.highscore:
                # Trick to update the highscore display-in game!
                self.new_highscore = self.score
            self.show_question()
        else:
            self.user_missed = True
            self.end_game()


    # Function that models a timer
    def count_down(self, secs: float):
        secs = round(secs, 2)

        # Constructing the new text to display
        whole_secs, part_secs = floor(secs), round(100 * (secs - floor(secs)))
        if part_secs < 10:
            new_text = f"{whole_secs}.0{part_secs}"
        else:
            new_text = f"{whole_secs}.{part_secs}"
        self.timer_label.config(text=new_text)
        if secs > 0:
            # Use the window.after() method and reduce secs to simulate a countdown. Save into a timer to
            # cancel it later!
            self.timer = self.window.after(10, self.count_down, secs - 0.01)
        else:
            self.end_game()


