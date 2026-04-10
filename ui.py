import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk


def build_ui(root):
    # ----- GUI SETUP -----
    #WINDOW
    root.geometry("1280x720")  
    root.title("Defuse Analyser")
    root.configure(bg="black")
    root.minsize(1200, 700) 


    # ----- FRAME FOR LOGO + TIMER -----
    timer_frame = tk.Frame(root, bg="black")
    timer_frame.pack(fill=tk.X, pady=20)

    # Configure columns
    timer_frame.grid_columnconfigure(0, minsize=300)
    timer_frame.grid_columnconfigure(1, weight=1) 
    timer_frame.grid_columnconfigure(2, minsize=300)


    #LOGO
    logo_img = Image.open("assets/defucelogo.png")
    logo_img = logo_img.resize((250, 250))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(timer_frame, image=logo_photo, bg="black")
    logo_label.image = logo_photo 
    logo_label.grid(row=0, column=0, rowspan=2, sticky='w', padx=(75,0), pady=0)  # spans both title+clock rows

    #TITLE
    timer_title = tk.Label(timer_frame, text="Timer", font=("Consolas", 20), fg="white", bg="black")
    timer_title.grid(row=0, column=1, sticky='n')  # title in center column, top

    #TIMER CLOCK
    timer_label = tk.Label(timer_frame, text="00:00", font=("Consolas", 100), fg="white", bg="black")
    timer_label.grid(row=1, column=1, sticky='n')  # clock under title
    
    # ----- BUTTONS ON RIGHT OF CLOCK -----
    button_frame = tk.Frame(timer_frame, bg="black")
    button_frame.grid(row=0, column=2, rowspan=2, sticky='ne', padx=(0, 100), pady=(80, 0))  # align top-right

    #Button 1
    btn1 = tk.Button(button_frame, text="Start", font=("Consolas", 30), width=10)
    btn1.pack(pady=(0, 40))  # 10px gap between buttons

    #Button 2
    btn2 = tk.Button(button_frame, text="Graph", font=("Consolas", 30), width=10)
    btn2.pack()



    # ----- TERMINAL TITLE -----
    terminal_title = tk.Label(root, text="Terminal", font=("Consolas", 20), fg="white", bg="black")
    terminal_title.pack(pady=(20, 0))


    #TERMINAL
    terminal = scrolledtext.ScrolledText(root, font=("Consolas", 12), fg="white", bg="black", height=5)
    terminal.pack(pady=10, fill=tk.BOTH, expand=True)
    terminal.configure(state='disabled')

    #INPUT
    input_frame = tk.Frame(root, bg="black")
    input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    prompt = tk.Label(input_frame, text="> ", fg="white", bg="black", font=("Consolas", 12))
    prompt.pack(side=tk.LEFT)

    user_input = tk.Entry(
        input_frame,
        font=("Consolas", 12),
        fg="white",
        bg="black",
        insertbackground="white"
    )
    user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

    return {
        "terminal": terminal, 
        "timer_label": timer_label, 
        "user_input": user_input, 
        "btn1": btn1,
        "btn2": btn2,
        "root": root
    }
