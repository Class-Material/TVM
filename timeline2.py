import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate NPV
def calculate_npv(cash_flows, rate, compounding_frequency):
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + rate / compounding_frequency) ** (t * compounding_frequency))
    return npv

# Function to calculate FV
def calculate_fv(cash_flows, rate, compounding_frequency):
    fv = 0
    n = len(cash_flows) - 1
    for t, cf in enumerate(cash_flows):
        fv += cf * ((1 + rate / compounding_frequency) ** ((n - t) * compounding_frequency))
    return fv

# Function to calculate the present value at each time period
def calculate_present_values(cash_flows, rate, compounding_frequency):
    present_values = []
    for t, cf in enumerate(cash_flows):
        present_value = cf / ((1 + rate / compounding_frequency) ** (t * compounding_frequency))
        present_values.append(present_value)
    return present_values

# Function to reset the application
def reset_app():
    for widget in cash_flows_entries:
        widget.destroy()
    cash_flows_entries.clear()
    period_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)
    comp_freq_entry.delete(0, tk.END)
    npv_label.config(text="NPV: ")
    fv_label.config(text="FV: ")
    ax.clear()
    ax2.clear()
    canvas.draw()

# Function to update the timeline and display results
def update_timeline():
    try:
        periods = int(period_entry.get())
        rate = float(rate_entry.get())
        compounding_frequency = int(comp_freq_entry.get())
        cash_flows = [float(entry.get()) for entry in cash_flows_entries]

        if cash_flows[-1] == "":
            # Solve for FV
            fv = calculate_fv(cash_flows[:-1], rate, compounding_frequency)
            cash_flows[-1] = fv
            fv_label.config(text=f"FV: {fv:.2f}")
        elif cash_flows[0] == "":
            # Solve for PV at t=0
            pv = calculate_npv(cash_flows, rate, compounding_frequency)
            cash_flows[0] = pv
            npv_label.config(text=f"NPV: {pv:.2f}")
        else:
            # Calculate NPV and FV normally
            npv = calculate_npv(cash_flows, rate, compounding_frequency)
            fv = calculate_fv(cash_flows, rate, compounding_frequency)
            npv_label.config(text=f"NPV: {npv:.2f}")
            fv_label.config(text=f"FV: {fv:.2f}")

        present_values = calculate_present_values(cash_flows, rate, compounding_frequency)

        # Plot the timeline
        ax.clear()
        ax.plot(range(0, periods), cash_flows, marker='o', label="Cash Flows")
        ax.set_title("Cash Flows and Present Values Timeline")
        ax.set_xlabel("Periods")
        ax.set_ylabel("Cash Flows")

        # Plot the present values on the secondary y-axis
        ax2.clear()
        ax2 = ax.twinx()
        ax2.plot(range(0, periods), present_values, marker='x', color='red', label="Present Values")
        ax2.set_ylabel("Present Values")

        # Show the legend outside of the graph area
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
        ax2.legend(loc="upper right", bbox_to_anchor=(1, 0.9))

        canvas.draw()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

# Function to create cash flow entries
def create_cash_flow_entries():
    try:
        periods = int(period_entry.get())  # Set up for periods excluding t=0
        reset_app()  # Reset before creating new entries
        for i in range(0, periods):
            label_text = "FV at t=T:" if i == periods - 1 else f"CF at t={i}:"
            tk.Label(input_frame, text=label_text).grid(row=3+i, column=0, sticky="e")
            entry = tk.Entry(input_frame)
            entry.grid(row=3+i, column=1)
            cash_flows_entries.append(entry)
        tk.Label(input_frame, text="PV at t=0:").grid(row=3+periods, column=0, sticky="e")
        cash_flows_entries.insert(0, tk.Entry(input_frame))
        cash_flows_entries[0].grid(row=3+periods, column=1)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of periods.")

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

# Create input fields for number of periods, interest rate, and compounding frequency
tk.Label(input_frame, text="Number of Periods:").grid(row=0, column=0, sticky="e")
period_entry = tk.Entry(input_frame)
period_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Interest Rate (as decimal):").grid(row=1, column=0, sticky="e")
rate_entry = tk.Entry(input_frame)
rate_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Compounding Frequency per Period:").grid(row=2, column=0, sticky="e")
comp_freq_entry = tk.Entry(input_frame)
comp_freq_entry.grid(row=2, column=1)

# Create dynamic input fields for cash flows
cash_flows_entries = []
tk.Button(input_frame, text="Set Periods", command=create_cash_flow_entries).grid(row=0, column=2, padx=5)

# Create button to calculate the missing field (PV, FV, or a CF)
tk.Button(input_frame, text="Calculate", command=update_timeline).grid(row=1, column=2, padx=5)

# Create a reset button to clear everything
tk.Button(input_frame, text="Reset", command=reset_app).grid(row=1, column=3, padx=5)

# Display NPV and FV
npv_label = tk.Label(result_frame, text="NPV: ")
npv_label.grid(row=0, column=0, sticky="w")
fv_label = tk.Label(result_frame, text="FV: ")
fv_label.grid(row=1, column=0, sticky="w")

# Create a figure for the timeline
fig, ax = plt.subplots()
ax2 = ax.twinx()  # Secondary y-axis for Present Values
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the main loop
root.mainloop()
