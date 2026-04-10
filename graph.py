import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def open_popup(parent, data_buffer):
    popup = tk.Toplevel(parent)
    popup.title("Graph")

    # Simple label
    label = tk.Label(popup, text="Value:", fg="white", bg="black")  # make label visible on black bg
    label.pack()

    # Basic matplotlib figure with black background
    fig, ax = plt.subplots(facecolor='black')  # set figure background to black
    ax.set_facecolor('black')  # set axes background to black
    line, = ax.plot([], [], color='white')  # white line

    # Set tick colors to white for visibility
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')

    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def update():
        if data_buffer:
            y = list(data_buffer)
            x = list(range(len(y)))

            line.set_data(x, y)
            ax.set_xlim(0, len(y))
            ax.set_ylim(0, 1023)

            label.config(text=f"Value: {y[-1]}")
            canvas.draw()

        popup.after(100, update)
    update()
    
    return popup