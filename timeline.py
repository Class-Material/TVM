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
        canvas.draw()
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for periods, rate, and cash flows.")

# Initialize the main window
root = tk.Tk()
root.title("NPV and FV Calculator")

# Create input fields for number of periods and interest rate
tk.Label(root, text="Number of Periods:").grid(row=0, column=0)
period_entry = tk.Entry(root)
period_entry.grid(row=0, column=1)

tk.Label(root, text="Interest Rate (as decimal):").grid(row=1, column=0)
rate_entry = tk.Entry(root)
rate_entry.grid(row=1, column=1)

# Create dynamic input fields for cash flows
cash_flows_entries = []
def create_cash_flow_entries():
    global cash_flows_entries
    for entry in cash_flows_entries:
        entry.destroy()
    cash_flows_entries = []
    try:
        periods = int(period_entry.get())
        for i in range(periods):
            tk.Label(root, text=f"Cash Flow for Period {i}:").grid(row=2+i, column=0)
            entry = tk.Entry(root)
            entry.grid(row=2+i, column=1)
            cash_flows_entries.append(entry)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of periods.")

tk.Button(root, text="Set Periods", command=create_cash_flow_entries).grid(row=0, column=2)

# Create button to update timeline and calculate NPV/FV
tk.Button(root, text="Calculate NPV/FV", command=update_timeline).grid(row=1, column=2)

# Display NPV and FV
npv_label = tk.Label(root, text="NPV: ")
npv_label.grid(row=2, column=2)
fv_label = tk.Label(root, text="FV: ")
fv_label.grid(row=3, column=2)

# Create a figure for the timeline
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=3)

# Run the main loop
root.mainloop()
