import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate NPV
def calculate_npv(cash_flows, r):
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + r) ** t)
    return npv

# Function to calculate FV
def calculate_fv(cash_flows, r):
    fv = 0
    for t, cf in enumerate(cash_flows):
        fv += cf * ((1 + r) ** (len(cash_flows) - t - 1))
    return fv

# Function to update the timeline and display results
def update_timeline():
    try:
        periods = int(period_entry.get())
        rate = float(rate_entry.get())
        cash_flows = [float(cash_flows_entries[i].get()) for i in range(periods)]
        
        npv = calculate_npv(cash_flows, rate)
        fv = calculate_fv(cash_flows, rate)
        
        npv_label.config(text=f"NPV: {npv:.2f}")
        fv_label.config(text=f"FV: {fv:.2f}")
        
        # Plot the timeline
        ax.clear()
        ax.plot(range(periods), cash_flows, marker='o')
        ax.set_title("Cash Flows Timeline")
        ax.set_xlabel("Periods")
        ax.set_ylabel("Cash Flows")

        # Add NPV text at the bottom left under the x-axis
        ax.text(0, min(cash_flows) - 0.1, f"NPV: {npv:.2f}", verticalalignment='top', horizontalalignment='left', transform=ax.get_xaxis_transform())

        # Add FV text at the bottom right under the x-axis
        ax.text(periods - 1, min(cash_flows) - 0.1, f"FV: {fv:.2f}", verticalalignment='top', horizontalalignment='right', transform=ax.get_xaxis_transform())

        canvas.draw()
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for periods, rate, and cash flows.")

# Initialize the main window
root = tk.Tk()
root.title("NPV and FV Calculator")

# Create frames to organize the layout
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

result_frame = tk.Frame(root)
result_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create input fields for number of periods and interest rate
tk.Label(input_frame, text="Number of Periods:").grid(row=0, column=0, sticky="e")
period_entry = tk.Entry(input_frame)
period_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Interest Rate (as decimal):").grid(row=1, column=0, sticky="e")
rate_entry = tk.Entry(input_frame)
rate_entry.grid(row=1, column=1)

# Create dynamic input fields for cash flows
cash_flows_entries = []
def create_cash_flow_entries():
    global cash_flows_entries
    for widget in cash_flows_entries:
        widget.destroy()
    cash_flows_entries = []
    try:
        periods = int(period_entry.get())
        for i in range(periods):
            tk.Label(input_frame, text=f"Cash Flow for Period {i}:").grid(row=2+i, column=0, sticky="e")
            entry = tk.Entry(input_frame)
            entry.grid(row=2+i, column=1)
            cash_flows_entries.append(entry)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of periods.")

tk.Button(input_frame, text="Set Periods", command=create_cash_flow_entries).grid(row=0, column=2, padx=5)

# Create button to update timeline and calculate NPV/FV
tk.Button(input_frame, text="Calculate NPV/FV", command=update_timeline).grid(row=1, column=2, padx=5)

# Display NPV and FV
npv_label = tk.Label(result_frame, text="NPV: ")
npv_label.grid(row=0, column=0, sticky="w")
fv_label = tk.Label(result_frame, text="FV: ")
fv_label.grid(row=1, column=0, sticky="w")

# Create a figure for the timeline
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the main loop
root.mainloop()
