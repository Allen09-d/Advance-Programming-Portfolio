from tkinter import *
from tkinter import ttk
import random

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("600x500")  # Set window size (portrait)

        # Game control variables
        self.game_state = 'menu'  
        self.difficulty = 'easy'
        self.problems = []  # Stores generated math problems
        self.current_index = 0
        self.attempts = 0
        self.score = 0

        # Tkinter variables for text and entry fields
        self.user_answer = StringVar()
        self.message = StringVar()
        self.show_result = False  # Controls button/entry states

        self.create_menu()  # Start with menu screen

    def random_int(self, min_val, max_val):
        return random.randint(min_val, max_val)

    def decide_operation(self):
        return '+' if random.random() > 0.5 else '-'  # Randomly pick + or -

    def generate_problems(self, diff):
        # Set number ranges for each difficulty level
        ranges = {'easy': [1, 9], 'moderate': [10, 99], 'advanced': [1000, 9999]}
        min_val, max_val = ranges[diff]
        problems = []

        # Create 10 random math problems
        for _ in range(10):
            num1 = self.random_int(min_val, max_val)
            num2 = self.random_int(min_val, max_val)
            operation = self.decide_operation()
            answer = num1 + num2 if operation == '+' else num1 - num2
            problems.append({'num1': num1, 'num2': num2, 'operation': operation, 'answer': answer})
        return problems

    def start_quiz(self, diff):
        # Reset quiz state and generate new problems
        self.difficulty = diff
        self.problems = self.generate_problems(diff)
        self.game_state = 'playing'
        self.current_index = 0
        self.score = 0
        self.attempts = 0
        self.user_answer.set('')
        self.message.set('')
        self.show_result = False
        self.create_playing()  # Load playing screen

    def check_answer(self):
        if not self.user_answer.get().strip():  # Empty input
            return

        problem = self.problems[self.current_index]
        try:
            user_num = int(self.user_answer.get())
        except ValueError:  # Handles non-numeric input
            self.message.set('Invalid input')
            return

        is_correct = user_num == problem['answer']

        if is_correct:
            # Full points if first try, half if second try
            points = 10 if self.attempts == 0 else 5
            self.score += points
            self.message.set(f'✓ Correct! +{points} points')
            self.show_result = True
            self.root.after(1500, self.next_problem)  # Move to next after delay
        else:
            # Allow one retry before showing correct answer
            if self.attempts == 0:
                self.attempts = 1
                self.message.set('✗ Incorrect, Try again!')
                self.user_answer.set('')
                self.show_result = False
            else:
                self.message.set(f'✗ Wrong! Answer: {problem["answer"]}')
                self.show_result = True
                self.root.after(1500, self.next_problem)

    def next_problem(self):
        # Prepare next question or go to results
        self.show_result = False
        self.user_answer.set('')
        self.attempts = 0
        self.message.set('')
        if self.current_index < 9:
            self.current_index += 1
            self.create_playing()
        else:
            self.game_state = 'results'
            self.create_results()

    def get_rank(self, score):
        # Converts numeric score to letter grade
        if score >= 95: return 'A+'
        elif score >= 90: return 'A'
        elif score >= 85: return 'B+'
        elif score >= 80: return 'B'
        elif score >= 75: return 'C+'
        elif score >= 70: return 'C'
        else: return 'F'

    def play_again(self):
        self.game_state = 'menu'
        self.create_menu()  # Return to menu screen

    def update_submit_button(self, event=None):
        # Enable submit only when user typed something and not showing result
        if not self.show_result and self.user_answer.get().strip():
            self.submit_btn.config(state='normal')
        else:
            self.submit_btn.config(state='disabled')

    def create_menu(self):
        # Clears screen and shows main menu
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = Frame(self.root, bg='#e0f2fe')
        main_frame.pack(fill=BOTH, expand=True)

        Label(main_frame, text="Math Quiz", font=("Arial", 36, "bold"),
              bg='#e0f2fe', fg="#000000").pack(pady=20)

        Label(main_frame, text="Select a difficulty level", font=("Arial", 16),
              bg='#e0f2fe', fg='#546e7a').pack(pady=10)

        button_frame = Frame(main_frame, bg='#e0f2fe')
        button_frame.pack(pady=20)

        # Difficulty selection buttons
        difficulties = ['easy', 'moderate', 'advanced']
        for i, level in enumerate(difficulties, 1):
            btn = Button(button_frame, text=f"{i}. {level.capitalize()}",
                         font=("Arial", 16, "bold"), bg='white', bd=2, relief='solid',
                         command=lambda l=level: self.start_quiz(l))
            btn.pack(pady=5, ipadx=20, ipady=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#e3f2fd'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='white'))

    def create_playing(self):
        # Clears screen and shows quiz question
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = Frame(self.root, bg='#f3e5f5')
        main_frame.pack(fill=BOTH, expand=True)

        # Progress bar and question number
        progress_frame = Frame(main_frame, bg='#f3e5f5')
        progress_frame.pack(pady=10)

        Label(progress_frame, text=f"Question {self.current_index + 1}/10",
              font=("Arial", 10), bg='#f3e5f5', fg='#546e7a').pack()

        progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
        progress['value'] = ((self.current_index + 1) / 10) * 100
        progress.pack()

        # Display math question
        problem = self.problems[self.current_index]
        Label(main_frame, text=f"{problem['num1']} {problem['operation']} {problem['num2']} =",
              font=("Arial", 24, "bold"), bg='#f3e5f5', fg='#37474f').pack(pady=20)

        # Answer input field
        entry = Entry(main_frame, textvariable=self.user_answer, font=("Arial", 16),
                      justify='center', state='normal' if not self.show_result else 'disabled')
        entry.pack(pady=10, ipadx=10, ipady=5)
        entry.focus()
        entry.bind('<Return>', lambda e: self.check_answer())
        entry.bind('<KeyRelease>', self.update_submit_button)

        # Submit button
        self.submit_btn = Button(main_frame, text="Submit", font=("Arial", 14, "bold"),
                                 bg='#1976d2', fg='white', command=self.check_answer, state='disabled')
        self.submit_btn.pack(pady=10, ipadx=20, ipady=5)
        self.update_submit_button()

        # Feedback message and score display
        Label(main_frame, textvariable=self.message, font=("Arial", 14, "bold"), bg='#f3e5f5').pack(pady=10)
        Label(main_frame, text=f"Score: {self.score}", font=("Arial", 10),
              bg='#f3e5f5', fg='#546e7a').pack()

    def create_results(self):
        # Final results screen
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = Frame(self.root, bg='#e8f5e8')
        main_frame.pack(fill=BOTH, expand=True)

        result_frame = Frame(main_frame, bg='white', bd=2, relief='solid')
        result_frame.pack(pady=50, padx=50, fill=BOTH, expand=True)

        Label(result_frame, text="Quiz Complete!", font=("Arial", 28, "bold"),
              bg='white', fg='#37474f').pack(pady=20)

        Label(result_frame, text=f"{self.score}/100", font=("Arial", 48, "bold"),
              bg='white', fg='#1976d2').pack(pady=10)

        # Display letter grade
        rank = self.get_rank(self.score)
        Label(result_frame, text=f"Grade: {rank}", font=("Arial", 36, "bold"),
              bg='white', fg='#3f51b5').pack(pady=20)

        # Restart button
        Button(result_frame, text="Play Again", font=("Arial", 16, "bold"),
               bg='#1976d2', fg='white', command=self.play_again).pack(pady=20, ipadx=20, ipady=10)

if __name__ == "__main__":
    root = Tk()
    app = MathQuizApp(root)
    root.mainloop()