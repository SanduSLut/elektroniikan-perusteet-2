import tkinter as tk
import serial
from sequence_cont import sequence, correct_pot, correct_rgb, wrong_pot, wrong_rgb, device_info, profile1, profile2, profile3
from ui import build_ui   
from graph import open_popup
from collections import deque
from task1 import check_pot_value
from task2 import start_rgb_game, handle_input_rgb
import webbrowser

#----- TIMER SETUP AND PROFILE -----
time = 12 # seconds
profile = 1 #SELECT 1, 2, 3

#----- GLOBAL VARIABLES -----
time_left = 0
popup_window = None
timer_running = True
ten_counter = False
exploded = False
hide_timer_display = False

task1_done = False
task2_done = False
final_task = False

current_pot_value = 0
pot_data = deque([0]*100, maxlen=100)
url = "https://www.youtube.com/watch?v=Aq5WXmQQooo"

ser = None
root = None
ui = None
terminal = None
timer_label = None
user_input = None

profile_correct_wires = {
    1: "WHITE",
    2: "GRAY",
    3: "WHITE"
}


# ----- FUNCTIONS -----

#TERMINAL OUTPUT
def log(msg):
    terminal.configure(state='normal')
    terminal.insert(tk.END, msg + "\n")
    terminal.yview(tk.END)
    terminal.configure(state='disabled')
    
#TERMINAL IMPUT
def handle_input(event=None):
    text = user_input.get().strip()
    if text:
        log(f"> {text}")
        process_command(text)
    user_input.delete(0, tk.END)
    
# ----- TERMINAL COMMAND HANDLER -----
def process_command(command):
    command = command.strip()
    if command == "":
        return

    if command == "sudo ddefuser get-device --info model":

        # Map global profile number to the correct device info
        if profile == 1:
            selected_profile = profile1
        elif profile == 2:
            selected_profile = profile2
        elif profile == 3:
            selected_profile = profile3
        else:
            log(f"[ERROR] Profile {profile} not found. Using profile 1 by default.")
            selected_profile = profile1

        # Combine device_info with the selected profile
        full_output = device_info + selected_profile

        # Non-blocking print using after()
        def print_line(index=0):
            if index < len(full_output):
                msg, delay = full_output[index]
                log(msg)
                terminal.after(delay, lambda: print_line(index + 1))

        print_line()

    else:
        log("Unknown command")


#GRAPH BUTTON
def btn2_pressed():
    global popup_window
    
    if ser:
        ser.write(b'StartGraph\n')
        ser.write(b'OpenGraph\n')
    
    #AVOIDS REOPENING MULTIPLE ONES
    if popup_window is not None:
        if popup_window.winfo_exists():
            popup_window.lift()  # bring to front
            return


    popup_window = open_popup(root, pot_data)
    
    #DETECTS IF USER CLOSES THE POPUP -> STOPS THE POTENTIOMETTER REQUEST
    def on_popup_close():
        global popup_window
        try:
            popup_window.destroy()
            if ser:
                ser.write(b'EndGraph\n')
                ser.write(b'CloseGraph\n')
        except:
            pass
        popup_window = None
        print("Popup closed by user")

    popup_window.protocol("WM_DELETE_WINDOW", on_popup_close)
  
#CONSTAT SERIAL READER
def read_serial():
    global timer_running, current_pot_value, popup_window, exploded, hide_timer_display
    global task1_done ,time_left, task2_done, final_task, profile
    
    if ser:
        while ser.in_waiting > 0:

            line = ser.readline().decode(errors='ignore').strip()
            print(line)
            
            # ---------------- BUTTON 1 ----------------
            if line == "1":
                print("Button pressed!")
                ser.write(b'Comp\n')  # turn green ON
                timer_running = False
                ui["btn2"].config(text="Again?", state="normal", bg=None, fg=None, command=start_app)
            
            # ---------------- POT CHECK ----------------    
            elif line == "P":
                print("Pot value: "+ str(current_pot_value))
                POTresult = check_pot_value(current_pot_value, profile) # ADD PROFILE
                print("__________")
                print("Pot check result: "+ str(POTresult) + "\n")
                
                ser.write(b'EndGraph\n')
        
                if POTresult in (0, 1) and popup_window and popup_window.winfo_exists():
                    task1_done = True
                    
                    popup_window.destroy()
                    popup_window = None
                    ui["btn2"].config(state="disabled",bg="gray", fg="white")
                    
                    result_ans(POTresult) 
                    
                    if POTresult == 1:
                        ser.write(b'Correct1\n')
                        start_rgb_game(root, ser, str(profile))
                    elif POTresult == 0:

                        time_left = max(0, time_left - 60) 
                        start_rgb_game(root, ser, str(profile))
                        ser.write(b'Wrong1\n')
                        
                print("Second task starts!")   
                
            # ---------------- RGB BUTTON INPUT ----------------
            elif line in ["PRESS", "HOLD"]:                 
                RGBresult = handle_input_rgb(line)

                if RGBresult == 1:
                    task2_done = True
                    if task1_done:
                        final_task = True
                        
                    ser.write(b'Correct2\n')
                    result_ans(2)

                elif RGBresult == 0:
                    task2_done = True
                    hide_timer_display = True               
                    if task1_done:
                        final_task = True
                    
                    ser.write(b'Wrong2\n')  # fail LED
                    result_ans(3)  
                    
                    
            # ---------------- WIRE EVENTS ----------------
            elif line in ["WHITE_CUT", "GRAY_CUT", "BLACK_CUT"]:
                print("Wire event:", line)
                wire = line.replace("_CUT", "")

                #Cut too early → FAIL
                if not (task1_done and task2_done):
                    print("CUT TOO EARLY → FAIL")
                    log("You cut a wire too early!")
                    exploded = True
                    timer_running = False
                    ser.write(b'Explode\n')
                    return

                #Final task active
                if final_task:
                    correct_wire = profile_correct_wires.get(profile)  # default to WHITE
                    if wire == correct_wire:
                        print("CORRECT WIRE!")
                        log(f"Congratulations, you successfully defused the objective.")

                        ser.write(b'Comp\n')  # turn green ON
                        timer_running = False
                        ui["btn1"].config(text="Again?", state="normal", bg=None, fg=None, command=start_app)

                    else:
                        print("WRONG WIRE!")
                        log(f"Wrong wire! Expected {correct_wire}, but cut {wire}.")

                        exploded = True
                        timer_running = False
                        ser.write(b'Explode\n')

            else:
                #POTENTIOMETER VALUE
                try:
                    value = int(line)
                    current_pot_value = value
                    pot_data.append(value) 
                except:
                    pass

    root.after(50, read_serial)


#TIMER COUNDDOWN AND CONFIG
def update_timer():
    global time_left, ten_counter, timer_running, exploded, hide_timer_display

    # Display current time
    if hide_timer_display:
        timer_label.config(text="XX:XX")
    else:
        minutes = time_left // 60
        seconds = time_left % 60
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    # Arduino sync
    if ser:
        if not ten_counter and time_left == 10:
            ser.write(b'TenSec\n')  # start countdown on Arduino
            timer_label.config(fg="red")
            ten_counter = True
            print("Sent '3' to Arduino: countdown started")
        elif not ten_counter:
            ser.write(b'RedTimer\n')  # blink before countdown

    # Check if countdown finished
    if time_left <= 0 and not exploded:
        exploded = True
        timer_running = False
        ui["btn1"].config(bg="red", fg="white", text="FAILED!")
        ui["btn2"].config(text="Again?", state="normal", bg=None, fg=None, command=start_app)
        timer_label.config(fg="red")
        log("Countdown finished! Explosion triggered!")
        webbrowser.open(url)
        return

    if not timer_running:
        return  # timer stopped for other reason

    # Decrease timer after display
    time_left -= 1
    root.after(1000, update_timer)
        
        
#TIMER BLINK BEFORE START
def blink_timer(times=6, on=True ):
    if times <= 0:
        timer_label.config(fg="white")  # end visible
        terminal.insert(tk.END,"\n")
        terminal.configure(state='disabled')
        update_timer()  
        read_serial()
        return
    timer_label.config(fg="white" if on else "black")
    root.after(700, blink_timer, times-1, not on)
    
    
#TERMINAL AWNSER INPUT
def result_ans(result, index=0):
    if result == 1:
        messages = correct_pot
    elif result == 0:
        messages = wrong_pot
    elif result == 2:
        messages = correct_rgb
    elif result == 3:
        messages = wrong_rgb 
    else:
        return 

    if index < len(messages):
        content, delay = messages[index]
        log(content)
        root.after(delay, result_ans, result, index + 1)
     

#TERMINAL LOG PRINT
def run_terminal(index=0):
    
    if index < len(sequence):
        type, content, delay = sequence[index]  
        
        if type == "msg":
            log(content)
        elif type == "bar":
            lenght = 50
            step = content
            bar = "[" + "#" * step + " " * (lenght - step) + "]"
            percent = int((step / lenght) * 100)
            
            # Update the same loading bar line
            terminal.configure(state='normal')
            if step > 1:
                terminal.delete("end-2l", "end-1l")
            terminal.insert(tk.END, f"{bar} {percent}%\n")
        
        # Schedule next step
        root.after(delay, run_terminal, index + 1)
    else:
        # This runs only when the sequence is fully done
        blink_timer()
        
def start_app():
    global time_left, timer_running, popup_window, current_pot_value, pot_data, ten_counter
    global exploded, task1_done, task2_done, final_task

    # Reset global state
    time_left = time
    timer_running = True
    ten_counter = False
    exploded = False
    task1_done = False
    task2_done = False
    final_task = False
    current_pot_value = 0
    pot_data = deque([0]*100, maxlen=100)
    
    # Close popup if it exists
    if popup_window and popup_window.winfo_exists():
        popup_window.destroy()
        popup_window = None
    
    #Makes time white again
    timer_label.config(fg="white")
    
    # Reset UI elements

    ui["btn1"].config(state="disabled", text="Analyzing", bg="gray", fg=None)
    ui["btn2"].config(state="normal", bg=None, fg=None)
    
    
    # Clear terminal if needed
    terminal.configure(state='normal')
    terminal.delete(1.0, tk.END)
    terminal.configure(state='disabled')
    
    # Resets LED's
    ser.write(b'R\n')
    
    # *MAIN STAR*
    run_terminal()
    
    # *THIS ARE FOR TESTING*
    #update_timer()
    #read_serial()

# ----- MAIN FUNCTION -----
def main():
    global ser, root, ui, terminal, timer_label, user_input

    # SERIAL SETUP
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
    except:
        ser = None
        print("Arduino not connected!")

    # UI SETUP
    root = tk.Tk()
    ui = build_ui(root)

    terminal = ui["terminal"]
    timer_label = ui["timer_label"]
    user_input = ui["user_input"]

    # Bindings
    user_input.bind("<Return>", handle_input)
    ui["btn1"].config(command=start_app)
    ui["btn2"].config(command=btn2_pressed)

    root.mainloop()


if __name__ == "__main__":
    main()