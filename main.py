import tkinter as tk
import tkinter.font as tkfont
import random
import time
import math

# Creating main window
root = tk.Tk()
root.title("Minesweeper")
root.geometry("800x600")

# Initializing Variables
instructions = "1. Click on a cell to reveal what's underneath.\n" \
               "2. If the cell contains a mine, the game is over and you lose.\n" \
               "3. If the cell does not contain a mine, a number is revealed indicating how many adjacent cells contain mines.\n" \
               "4. Use the numbers to deduce where the mines are located.\n" \
               "5. Right-click on a cell to flag it as a mine. This helps you keep track of where you think the mines are located.\n" \
               "6. Right-click on a cell that already has a flag to remove the flag.\n" \
               "7. Win the game by flagging all cells that contain mines.\n" \
               "\n" \
               "Good luck!"

title_font = tkfont.Font(family="Bungee", size=30)
difficulty_font = tkfont.Font(family="Bungee", size=24)
default_font = tkfont.Font(family="Bungee", size=12)
small_font = tkfont.Font(family="Bungee", size=10)

easy_rows = 9
easy_columns = 9
easy_mines = 10
easy_flags = easy_mines

medium_rows = 16
medium_columns = 16
medium_mines = 40
medium_flags = medium_mines

hard_rows = 16
hard_columns = 30
hard_mines = 99
hard_flags = hard_mines

bg_color = "#ABC4AA"
unclicked_cell_color = "#a8dba8"
clicked_cell_color = "#F3DEBA"
mine_text_colors = {
    "X": "#ff0000",
    0: "#424242",
    1: "#1976d2",
    2: "#388e3c",
    3: "#d33030",
    4: "#7b1fa2",
    5: "#e65100",
    6: "#1976d2",
    7: "#388e3c",
    8: "#d33030"
}
flag_color = "#EB455F"
text_color = "#000000"
button_bg_color = "#539165"
timer_color = "#060047"
button_highlight_color = "#e5ffe5"
cell_highlight_color = "#c1ffc1"


# Game functions
# Saves time to local leaderboard
def save_time(difficulty, time_taken):
    global player_name
    with open("leaderboard.txt", "a") as f:
        f.write(f"{difficulty},{player_name},{time_taken}\n")

# Gets top 5 times for a given difficulty
def get_top_times(difficulty):
    times = []
    # Opening leaderboard file
    with open("leaderboard.txt", "r") as f:
        for line in f:
            line = line.strip()
            # Finding times associated with current difficulty
            if line.startswith(difficulty):
                _, name, time_taken = line.split(",")
                times.append((float(time_taken), name))
    # Ranking 5 lowest times
    top_times = sorted(times)[:5]
    ranked_times = [f"{i+1}. {name}: {time_taken:.2f}\n" for i, (time_taken, name) in enumerate(top_times)]
    return ranked_times

# Function to show Leaderboard
def show_leaderboard(difficulty):
    # Clears current frame
    for widget in root.winfo_children():
        widget.destroy()
    
    # Create a new frame
    leaderboard_frame = tk.Frame(root, bg=bg_color)
    leaderboard_frame.pack(expand=True, fill=tk.BOTH)
    leaderboard_frame.grid_rowconfigure(0, weight=1)
    leaderboard_frame.grid_rowconfigure(1, weight=3)
    leaderboard_frame.grid_rowconfigure(2, weight=1)
    leaderboard_frame.grid_rowconfigure(3, weight=1)

    leaderboard_frame.grid_columnconfigure(0, weight=1)
    leaderboard_frame.grid_columnconfigure(1, weight=1)
    leaderboard_frame.grid_columnconfigure(2, weight=1)

    # Creates a label
    leaderboard_label = tk.Label(leaderboard_frame, text=f"{difficulty}:", font=title_font, bg=bg_color, foreground=text_color)
    leaderboard_label.grid(row=0, column=1)

    # Top 5 fastest times label
    fastest_times = tk.Label(leaderboard_frame, text="".join(str(t) for t in get_top_times(difficulty)), font=default_font, bg=bg_color, foreground=text_color)
    fastest_times.grid(row=1, column=1)

    # Creating new name button
    new_name_button = tk.Button(leaderboard_frame, text="Enter New Name",font=small_font, command=enter_name, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    new_name_button.grid(row=3, column=2)

    # Creating play again button
    play_again_button = tk.Button(leaderboard_frame, text="Play Again",font=small_font, command=choose_difficulty, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    play_again_button.grid(row=3, column=1)

    # Creating Quit button
    quit_button = tk.Button(leaderboard_frame, text="Quit", font=small_font, command=root.quit, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.grid(row=3, column=0)

# Game over function
def game_over():
    # Stopping update_time function
    global timer_running
    timer_running = False

    # Clearing window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Create a new frame
    game_over_frame = tk.Frame(root, bg=bg_color)
    game_over_frame.pack(expand=True, fill=tk.BOTH)

    # Explosion animation
    explosion_canvas = tk.Canvas(game_over_frame, width=800, height=200, bg=bg_color, highlightthickness=0)
    explosion_canvas.pack(expand=True, fill=tk.BOTH)

    def explode(x, y, r, color):
        text_size = 50 + (10 // 50)
        explosion_canvas.create_text(100, 100, text="BOOM!", font=("Impact", text_size), fill="black")
        if r < 800:
            explosion_colors = ["orange", "yellow", "red", "white"]
            for i in range(4):
                explosion_canvas.create_oval(x-r, y-r, x+r, y+r, outline=explosion_colors[i], width=5)
                explosion_canvas.create_oval(x-r-i*5, y-r-i*5, x+r+i*5, y+r+i*5, outline=explosion_colors[i], width=5)
            for i in range(12):
                angle = math.radians(i*30)
                cx = x + (r-30) * math.cos(angle)
                cy = y - (r-30) * math.sin(angle)
                explosion_canvas.create_polygon(x, y, cx-15, cy-15, cx, cy, cx+15, cy-15, fill="yellow", outline="white", width=3)
            explosion_canvas.after(20, explode, x, y, r+20, color)

    
    explode(100, 100, 10, 'orange')

    # Game over label
    game_over_label = tk.Label(game_over_frame, text="Game Over", font=title_font, bg=bg_color, fg=text_color)
    game_over_label.pack(pady=50)

    # Play Again button
    play_again_button = tk.Button(game_over_frame, text="Play Again", font=small_font, command=lambda: choose_difficulty(),bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    play_again_button.pack(pady=10)

    # Quit button
    quit_button = tk.Button(game_over_frame, text="Quit", font=small_font, command=root.destroy, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.pack(pady=10)

# Victory function
def victory(frame, difficulty):
    # Stopping update_time function
    global timer_running
    timer_running = False

    # Saves time to leaderboard
    save_time(difficulty, elapsed_time)

    # Clearing frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Creating congratulations label
    congrats_label = tk.Label(frame, text="Congratulations, you won!", font=title_font, bg=bg_color, fg=text_color)
    congrats_label.pack(pady=10)

    # Creating time taken label
    time_label = tk.Label(frame, text=f"Time taken: {elapsed_time:.2f} seconds", font=default_font, bg=bg_color, fg=timer_color)
    time_label.pack(pady=10)

    # Creating new name button
    new_name_button = tk.Button(frame, text="Enter New Name",font=small_font, command=enter_name, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    new_name_button.pack(pady=10)

    # Creating play again button
    play_again_button = tk.Button(frame, text="Play Again",font=small_font, command=choose_difficulty, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    play_again_button.pack(pady=10)

    # Creating view leaderboard button
    leaderboard_button = tk.Button(frame, text="View Leaderboard",font=small_font, command=lambda: show_leaderboard(difficulty), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    leaderboard_button.pack(pady=10)

    # Creating Quit button
    quit_button = tk.Button(frame, text="Quit", font=small_font, command=root.quit, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.pack(pady=10)

# Creating game board
def create_board(rows, cols, mines, flags, frame, difficulty):
    global flags_left
    flags_left = flags
    global first_click
    first_click = True

    # Function for placing mines/assigning cell values
    def place_mines(board, rows, cols, mines, click_row, click_col):
        count = 0
        # Randomly placing mines
        while count < mines:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            # Will not allow mines to be placed within two cells of the first click or on another mine
            if (board[row][col] != "X") and ((abs(row - click_row) > 1) or (abs(col - click_col) > 1)):
                board[row][col] = "X"
                count += 1
        
        # Calculating each cells value
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != "X":
                    num_mines = 0
                    for r in range(max(0, row-1), min(rows, row+2)):
                        for c in range(max(0, col-1), min(cols, col+2)):
                            if board[r][c] == "X":
                                num_mines += 1
                    board[row][col] = num_mines
        # Starts timer and returns the board with each cell having a value or mine
        global start_timer
        start_timer()
        return board

    # Function for revealing cells
    def reveal_cells(row, col):
        button = buttons[row][col]
        global value
        value = values[row][col]
        button.config(text=value, bg=clicked_cell_color, fg=mine_text_colors[value])
        button.config(relief=tk.SUNKEN)

        # Stopping recursion if cell has a non-zero value
        if value != 0:
            return

        # recursively reveal adjacent cells with value 0
        for r in range(max(0, row-1), min(rows, row+2)):
            for c in range(max(0, col-1), min(cols, col+2)):
                if buttons[r][c]["text"] == "" and (r != row or c != col):
                    reveal_cells(r, c)
    
    # Left click function
    def left_click(event):
        button = event.widget
        # if the button has not been clicked before
        if button["text"] == "":
            row = int(button.grid_info()["row"])
            col = int(button.grid_info()["column"])

            # If it is the first click the program places mines
            global first_click
            if first_click == True:
                global values
                values = place_mines(board, rows, cols, mines, row, col)
                first_click = False 

            # Getting the value of the clicked cell
            value = values[row][col]

            # If the user clicked a mine
            if value == "X":
                button.config(text="X", bg="red")
                game_over()

            # If the user clicked an empty cell
            elif value == 0:
                reveal_cells(row, col)
            
            # If the user clicked a cell with adjacent mines
            else:
                button.config(text=value, bg=clicked_cell_color, fg=mine_text_colors[value])
                button.config(relief=tk.SUNKEN)
    
    # Function for checking if the user has flagged all mines
    def check_win(frame):
        # Iterates over each cell and finds if all mines have a flag over them
        for row in range(rows):
            for col in range(cols):
                button = buttons[row][col]
                value = values[row][col]
                if value == "X" and button["text"] != "F":
                    return False
                elif value != "X" and button["text"] == "F":
                    return False
                else:
                    victory(frame, difficulty)
                    return True
    
    # Right click function
    def right_click(event):
        global flags_left
        button = event.widget

        # If there is no flag program places one until the user is out of flags which triggers the check win function
        if (button["text"] == "") and (flags_left != 0):
            button["text"] = "F"
            button["foreground"] = flag_color
            flags_left = flags_left - 1
            if flags_left == 0:
                check_win(frame)

        # If a flag is present the program takes it away
        elif button["text"] == "F":
            button["text"] = ""
            button["foreground"] = mine_text_colors[value]
            flags_left = flags_left + 1

        # Program calls for the flag label to be updated
        update_flags_left()
  
    # Creating the board
    global board
    board = []
    for i in range(rows):
        row = [0] * cols
        board.append(row)

    # Creating a button for each cell which have a command for left and right clicks
    buttons = []
    for row in range(rows):
        row_buttons = []
        for col in range(cols):
            button = tk.Button(frame, text="", font=default_font, width=1, height=1, bg=unclicked_cell_color, highlightbackground=cell_highlight_color, relief=tk.RAISED)
            button.grid(row=row, column=col, sticky=tk.NSEW)
            button.bind("<Button-1>", left_click)
            button.bind("<Button-3>", right_click)
            row_buttons.append(button)
        buttons.append(row_buttons)

    # Configuring the frame so the cells are spread evenly
    for row in range(rows):
        frame.grid_rowconfigure(row, weight=1)

    for column in range(cols):
        frame.grid_columnconfigure(column, weight=1)

def game(rows, cols, mines, flags):
    # Program calculates what difficulty is being played
    if cols == 9:
        difficulty = "Easy"
    elif cols == 16:
        difficulty = "Medium"
    elif cols == 30:
        difficulty = "Hard"

    # Deleting previous frame
    for widget in root.winfo_children():
        widget.destroy()

    # Creating/placing top and game frame
    top_frame = tk.Frame(root, height=40, bg=bg_color)
    game_frame = tk.Frame(root, bg=bg_color)

    top_frame.pack(side="top", fill="x")
    game_frame.pack(side="bottom", fill="both", expand=True)

    # Creating widgets for top frame
    timer_label = tk.Label(top_frame, text="Time: 0", font=default_font, bg=bg_color, fg=timer_color)
    timer_label.pack(side="right")

    global flags_label
    flags_label = tk.Label(top_frame, text=f"Flags: {flags}", font=default_font, bg=bg_color, fg=flag_color)
    flags_label.pack(side="right", padx=10)

    quit_button = tk.Button(top_frame, text="Quit", font=default_font, command=root.destroy, bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.pack(side="left", padx=10)

    # Updating Flags label
    global update_flags_left
    def update_flags_left():
        flags_label.config(text=f"Flags left: {flags_left}")

    # Game timer functions
    timer_running = False
    # Updating timer every second
    def update_timer():
        global timer_running, elapsed_time
        if timer_running == True:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time / 60)
            seconds = int(elapsed_time % 60)
            timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            root.after(1000, update_timer)
        elif timer_running == False: 
            stop_timer()

    # Starting timer when game starts (after first click)
    global start_timer
    def start_timer():
        global timer_running
        timer_running = True
        global start_time
        start_time = time.time()
        timer_label.config(text="Time: 00:00")
        update_timer()

    # Stopping timer and storing total time taken upon victory
    global stop_timer
    def stop_timer():
        global elapsed_time, total_time
        total_time = elapsed_time
        root.after_cancel(update_timer)
        return total_time
    
    # Create and place game board
    create_board(rows, cols, mines, flags, game_frame, difficulty)

# Function to pull up enter name screen
def enter_name():
    # Function to save the name provided
    def save_name(name):
        global player_name
        player_name = name
        choose_difficulty()

    # Deleting previous widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    content_frame = tk.Frame(root, bg=bg_color)
    content_frame.pack(expand=True, fill=tk.BOTH)

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=1)

    # Creating label for name entry
    name_label = tk.Label(content_frame, text="Enter Your Name:", font=difficulty_font, bg=bg_color, fg=text_color)
    name_label.grid(row=0, column=1)

    # Creating entry box for name and storing it
    name_entry = tk.Entry(content_frame, font=default_font, bg=button_bg_color, foreground=text_color)
    name_entry.grid(row=1, column=1)

    # Creating submit button
    submit_button = tk.Button(content_frame, text="Submit", font=small_font, command=lambda: save_name(name_entry.get()), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    submit_button.grid(row=2, column=2)

    # Creating quit button
    quit_button = tk.Button(content_frame, text="Quit", font=small_font, command=lambda: root.destroy(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.grid(row=2, column=0)

# Next button (to difficulty screen)
def choose_difficulty():
    # Deleting previous widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    content_frame = tk.Frame(root, bg=bg_color)
    content_frame.pack(expand=True, fill=tk.BOTH)

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_rowconfigure(3, weight=1)
    content_frame.grid_rowconfigure(4, weight=1)
    content_frame.grid_rowconfigure(5, weight=1)

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=1)

    # Creating difficulty label
    difficulty_label = tk.Label(content_frame, text="Choose Your Difficulty:", font=difficulty_font, bg=bg_color, fg=text_color)
    difficulty_label.grid(row=0, column=1, pady=10)

    # Creating quit button
    quit_button = tk.Button(content_frame, text="Quit", font=small_font, command=lambda: root.destroy(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.grid(row=5, column=0, padx=20)

    # Creating the easy button
    easy_button = tk.Button(content_frame, text="Easy", font=default_font, command=lambda: game(easy_rows, easy_columns, easy_mines, easy_flags), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    easy_button.grid(row=2, column=1, sticky=tk.N, pady=10)

    # Creating the medium button
    medium_button = tk.Button(content_frame, text="Medium", font=default_font, command=lambda: game(medium_rows, medium_columns, medium_mines, medium_flags), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    medium_button.grid(row=3, column=1, sticky=tk.N, pady=10)

    # Creating the hard button
    hard_button = tk.Button(content_frame, text="Hard", font=default_font, command=lambda: game(hard_rows, hard_columns, hard_mines, hard_flags), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    hard_button.grid(row=4, column=1, sticky=tk.N, pady=10)

# Start Button
def start():
    # Deleting previous widgets
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Creating instructions label
    instructions_label = tk.Label(content_frame, text="Instructions:", font=title_font, bg=bg_color, fg=text_color)
    instructions_label.grid(row=0, column=0, columnspan=3, sticky=tk.N)

    # Creating instructions text box
    instructions_text = tk.Message(content_frame, text=instructions, font=small_font, bg=button_bg_color, fg=text_color)
    instructions_text.grid(row=1, column=1, rowspan=2)

    # Creating quit button
    quit_button = tk.Button(content_frame, text="Quit", font=small_font, command=lambda: root.destroy(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    quit_button.grid(row=3, column=0)

    # Creating next bitton
    next_button = tk.Button(content_frame, text="Next", font=small_font, command=lambda: enter_name(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
    next_button.grid(row=3, column=2)

# Creating content frame
content_frame = tk.Frame(root, bg=bg_color)
content_frame.pack(expand=True, fill=tk.BOTH)

content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_rowconfigure(1, weight=1)
content_frame.grid_rowconfigure(2, weight=1)
content_frame.grid_rowconfigure(3, weight=1)

content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)
content_frame.grid_columnconfigure(2, weight=1)

# Creating the title label
title_label = tk.Label(content_frame, text="Minesweeper", font=title_font, fg=text_color, bg=bg_color)
title_label.grid(row=0, column=1)

# Creating the start button
start_button = tk.Button(content_frame, text="Start", font=default_font, command=lambda: start(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
start_button.grid(row=2, column=1)

# Creating the quit button
quit_button = tk.Button(content_frame, text="Quit", font=small_font, command=lambda: root.destroy(), bg=button_bg_color, fg=text_color, highlightbackground=button_highlight_color)
quit_button.grid(row=3, column=0)

# Start the GUI event loop
root.mainloop()