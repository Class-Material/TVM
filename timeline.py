import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate NPV
def calculate_npv(cash_flows, r):
    npv = 0
    for t, cf in enumerate(cash_flows, start=1):
        npv += cf / ((1 + r) ** t)
    return npv

# Function to calculate FV
def calculate_fv(cash_flows, r):
    fv = 0
    for t, cf in enumerate(cash_flows, start=1):
        fv += cf * ((1 + r) ** (len(cash_flows) - t))
    return fv

# Function to calculate the present value at each time period
def calculate_present_values(cash_flows, r):
    present_values = []
    for t, cf in enumerate(cash_flows, start=1):
        present_value = cf / ((1 + r) ** t)
        present_values.append(present_value)
    return present_values

# Function to update the timeline and display results
def update_timeline():
    try:
        periods = int(period_entry.get())
        rate = float(rate_entry.get())
        cash_flows = [float(cash_flows_entries[i].get()) for i in range(periods)]
        
        npv = calculate_npv(cash_flows, rate)
        fv = calculate_fv(cash_flows, rate)
        present_values = calculate_present_values(cash_flows, rate)
        
        npv_label.config(text=f"NPV: {npv:.2f}")
        fv_label.config(text=f"FV: {fv:.2f}")
        
        # Plot the timeline
        ax.clear()
        ax.plot(range(1, periods + 1), cash_flows, marker='o', label="Cash Flows")
        ax.set_title("Cash Flows Timeline")
        ax.set_xlabel("Periods")
        ax.set_ylabel("Cash Flows")

        # Plot the present values on the secondary y-axis
        ax2 = ax.twinx()
        ax2.plot(range(1, periods + 1), present_values, marker='x', color='red', label="Present Values")
        ax2.set_ylabel("Value at t")
        
        # Add NPV and FV text
        ax.text(1, min(cash_flows) - 0.1, f"NPV: {npv:.2f}", verticalalignment='top', horizontalalignment='left', transform=ax.get_xaxis_transform())
        ax.text(periods, min(cash_flows) - 0.1, f"FV: {fv:.2f}", verticalalignment='top', horizontalalignment='right', transform=ax.get_xaxis_transform())

        # Add Discount Factor and Compound Factor under each period
        for t in range(1, periods + 1):
            discount_factor = 1 / ((1 + rate) ** t)
            compound_factor = (1 + rate) ** t

            ax.text(t, min(cash_flows) - 0.2, f"DF: {discount_factor:.4f}", verticalalignment='top', horizontalalignment='center', transform=ax.get_xaxis_transform())
            ax.text(t, min(cash_flows) - 0.3, f"CF: {compound_factor:.4f}", verticalalignment='top', horizontalalignment='center', transform=ax.get_xaxis_transform())

        # Show the legend
        ax.legend(loc="upper left")
        ax2.legend(loc="upper right")

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
        for i in range(1, periods + 1):
            tk.Label(input_frame, text=f"Cash Flow for Period {i}:").grid(row=1+i, column=0, sticky="e")
            entry = tk.Entry(input_frame)
            entry.grid(row=1+i, column=1)
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
