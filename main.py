import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from malaysia_data import questions
from tkinter import Frame  # Add this to your existing imports

time_left = 5  # Seconds per question
is_paused = False
remaining_time = 0

def reset_timer():
    global time_left, is_paused
    time_left = 5
    if not is_paused:
        time_display.config(text=str(time_left), foreground="black")
        if hasattr(root, 'timer_job'):
            root.after_cancel(root.timer_job)
        update_timer()

def update_timer():
    global time_left, is_paused
    
    if is_paused:
        return  # Don't update if paused
    
    time_left -= 1
    time_display.config(text=str(time_left))
    
    if time_left <= 2:
        time_display.config(foreground="red")
    
    if time_left <= 0:
        time_up()
    else:
        root.timer_job = root.after(1000, update_timer)

def time_up():
    feedback_label.config(text="Time's up!", foreground="red")
    roast_label.config(text="Too slow! Try to answer faster next time.", foreground="orange")
    
    # Disable all answer buttons
    for button in choice_btns:
        button.config(state="disabled")
    
    # Enable next button
    next_btn.config(state="normal")

def toggle_pause():
    global is_paused, remaining_time, time_left
    
    is_paused = not is_paused  # Toggle state
    
    if is_paused:
        # Store remaining time and stop timer
        remaining_time = time_left
        if hasattr(root, 'timer_job'):
            root.after_cancel(root.timer_job)
        pause_btn.config(text="▶")  # Play symbol
        time_display.config(text="Paused")
        # Disable all buttons except pause button
        for btn in choice_btns:
            btn.config(state="disabled")
    else:
        # Restore timer
        time_left = remaining_time
        pause_btn.config(text="⏸")  # Pause symbol
        time_display.config(text=str(time_left))
        update_timer()
        # Re-enable choice buttons if question is active
        if feedback_label.cget("text") == "":
            for btn in choice_btns:
                btn.config(state="normal")

# Function to display the current question and choices
def show_question():
    # Get the current question from the questions list
    question = questions[current_question]
    qs_label.config(text=question["prompt"])

    # Display the choices on the button
    choices = question["options"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal") # Reset button stated

    # Clear the feedback label and disable next button
    feedback_label.config(text="")
    roast_label.config(text="")
    next_btn.config(state="disabled")

     # Reset and start the timer
    reset_timer()
    if is_paused:
        time_display.config(text="Paused")  # Show paused state
    else:
        time_display.config(text=str(time_left))

# Function to check the selected answer and provide feedback
def check_answer(choice):
    # Cancel timer only if not paused
    if not is_paused and hasattr(root, 'timer_job'):
        root.after_cancel(root.timer_job)

    # Get the current question from the questions list
    question = questions[current_question]
    selected_choice = choice_btns[choice].cget("text")

    # Check if the selected choice matches the correct answer
    if selected_choice == question["answer"]:
        # Update the score and display it
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(questions)))
        feedback_label.config(text="Correct!", foreground="green")
        roast_label.config(text="")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
        roast_label.config(text=question["roast"], foreground="orange")

    # Disable all choice buttons and enable next button
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

# Function to move to the next question
def next_question():
    global current_question
    current_question +=1

    if current_question < len(questions):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final Score: {}/{}".format(score, len(questions)))
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Malaysian Quiz App")
root.geometry("600x700")
style = Style(theme="flatly")

# Font Sizes for question and choice button
style.configure("TLabel", font=("Montserrat", 20))
style.configure("TButton", font=("Montserrat", 14))

# Create a top control frame
control_frame = Frame(root)
control_frame.pack(fill=tk.X, padx=10, pady=5)

# Pause Button (Left side)
pause_btn = ttk.Button(
    control_frame,
    text="⏸",  # Pause symbol
    command=lambda: toggle_pause(),
    width=3
)
pause_btn.pack(side=tk.LEFT)

# Timer Display (Right side)
timer_frame = Frame(control_frame)
timer_frame.pack(side=tk.RIGHT)

timer_icon = ttk.Label(
    timer_frame,
    text="⏱️",  # Timer icon
    font=("Montserrat", 14)
)
timer_icon.pack(side=tk.LEFT, padx=2)

time_display = ttk.Label(
    timer_frame,
    text="5",
    font=("Montserrat", 14, "bold")
)
time_display.pack(side=tk.LEFT)

# Question Label
qs_label = ttk.Label(
    root, 
    text="",
    anchor="center",
    justify="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=(50, 10), fill='x')

# Choice Button
choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Feedback Label
feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=1
)
feedback_label.pack(pady=(10, 0))

# Roast Label (for funny responses when wrong)
roast_label = ttk.Label(
    root,
    anchor="center",
    padding=1,
    wraplength=500,  
    font=("Montserrat", 12, "italic")  
)
roast_label.pack(pady=0)

# Initialize the score
score = 0

# Create the score label
score_label = ttk.Label(
    root,
    text="Score: 0/{}".format(len(questions)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

# Initialize the current question Index
current_question = 0

# Show the first question
show_question()

# Start the main event loop
root.mainloop()