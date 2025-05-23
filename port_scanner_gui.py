import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

def scan_ports_thread():
    target = target_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Ports must be integers!")
        return

    result_area.config(state='normal')  # Enable editing
    result_area.delete('1.0', tk.END)
    result_area.insert(tk.END, f"Scanning {target} from port {start_port} to {end_port}...\n\n", 'info')

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            result_area.insert(tk.END, f"✅ Port {port} is OPEN\n", 'open')
        else:
            result_area.insert(tk.END, f"❌ Port {port} is CLOSED\n", 'closed')
        s.close()

    result_area.insert(tk.END, "\nScan complete.\n", 'info')
    result_area.config(state='disabled')  # Make it read-only again

def start_scan():
    thread = threading.Thread(target=scan_ports_thread)
    thread.start()

# GUI setup
window = tk.Tk()
window.title("Port Scanner Tool")
window.geometry("600x600")
window.configure(bg="#f0f0f0")  # Light gray background

# Labels and entries
tk.Label(window, text="Target IP / Hostname:", bg="#f0f0f0").pack()
target_entry = tk.Entry(window, width=40)
target_entry.pack()
target_entry.insert(0, "127.0.0.1")

tk.Label(window, text="Start Port:", bg="#f0f0f0").pack()
start_port_entry = tk.Entry(window, width=20)
start_port_entry.pack()
start_port_entry.insert(0, "1")

tk.Label(window, text="End Port:", bg="#f0f0f0").pack()
end_port_entry = tk.Entry(window, width=20)
end_port_entry.pack()
end_port_entry.insert(0, "100")

tk.Button(window, text="Scan Ports", command=start_scan, bg="#4CAF50", fg="white").pack(pady=10)

# Styled result area
result_area = scrolledtext.ScrolledText(window, width=70, height=25, bg="#1e1e1e", fg="white", font=("Consolas", 11))
result_area.pack(pady=5)

# Tag styles for output
result_area.tag_config('open', foreground='lime')
result_area.tag_config('closed', foreground='red')
result_area.tag_config('info', foreground='cyan')
result_area.config(state='disabled')  # Start as read-only

window.mainloop()
