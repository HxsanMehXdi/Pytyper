import tkinter as tk
import threading
import time
import random
import pyautogui
import keyboard

typing_active = False

def type_text():
    global typing_active

    text = text_box.get("1.0", "end-1c")
    cps = cps_var.get()
    mode = mode_var.get()

    base_delay = 1 / cps if cps > 0 else 0.01

    typing_active = True

    # Countdown
    for i in range(3, 0, -1):
        if not typing_active:
            return
        status_label.config(text=f"Starting in {i}...")
        time.sleep(1)

    status_label.config(text="Typing... Press F9 to stop.")

    i = 0
    while i < len(text):
        if not typing_active:
            break

        char = text[i]

        if mode == "realistic":
            # Chance to make a typo (~8%)
            if random.random() < 0.08 and char.isalpha():
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                pyautogui.write(wrong_char)
                time.sleep(base_delay * random.uniform(0.3, 1.0))

                # Backspace to fix
                pyautogui.press("backspace")
                time.sleep(base_delay * random.uniform(0.2, 0.6))

            # Type correct character
            if char == "\n":
                pyautogui.press("enter")
            elif char == "\t":
                pyautogui.press("tab")
            else:
                pyautogui.write(char)

            delay = base_delay * random.uniform(0.4, 1.3)

        else:
            # Fast mode (chunk typing)
            chunk_size = 20
            chunk = text[i:i+chunk_size]
            pyautogui.write(chunk)
            i += chunk_size
            time.sleep(base_delay * 0.2)
            continue

        i += 1
        time.sleep(delay)

    typing_active = False
    status_label.config(text="Stopped.")


def start_typing():
    global typing_active
    if typing_active:
        return

    threading.Thread(target=type_text, daemon=True).start()


def stop_typing():
    global typing_active
    typing_active = False
    status_label.config(text="Stopped.")


# UI setup
root = tk.Tk()
root.title("Auto Typer")
root.geometry("550x620")
root.configure(bg="#1e1e1e")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(fill="both", expand=True)

# Title
tk.Label(frame, text="Text to type exactly as written:",
         bg="#1e1e1e", fg="white").pack(pady=5)

# Text box
text_box = tk.Text(frame, height=12, width=60,
                   bg="#2b2b2b", fg="white", insertbackground="white")
text_box.pack(padx=10, pady=5)

# CPS slider
cps_var = tk.IntVar(value=120)
tk.Label(frame, text="Typing Speed (CPS):",
         bg="#1e1e1e", fg="white").pack()

tk.Scale(frame, from_=10, to=500, orient="horizontal",
         variable=cps_var, bg="#1e1e1e", fg="white",
         highlightthickness=0).pack()

# Mode toggle
mode_var = tk.StringVar(value="realistic")

tk.Label(frame, text="Mode:",
         bg="#1e1e1e", fg="white").pack(pady=5)

tk.Radiobutton(frame, text="⌨️ Realistic (Human-like + Typos)",
               variable=mode_var, value="realistic",
               bg="#1e1e1e", fg="white", selectcolor="#2b2b2b").pack()

tk.Radiobutton(frame, text="⚡ Fast (Max speed)",
               variable=mode_var, value="fast",
               bg="#1e1e1e", fg="white", selectcolor="#2b2b2b").pack()

# Buttons
tk.Button(frame, text="Start Typing (F8)",
          command=start_typing,
          bg="#3c3f41", fg="white").pack(pady=5)

tk.Button(frame, text="Stop Typing (F9)",
          command=stop_typing,
          bg="#3c3f41", fg="white").pack(pady=5)

# Status
status_label = tk.Label(frame,
                        text="Ready. Press F8 to start, F9 to stop.",
                        bg="#1e1e1e", fg="lightgreen")
status_label.pack(pady=10)

# Credit
credit_label = tk.Label(root,
                        text="Made by Hasan Mehdili",
                        font=("Arial", 9),
                        bg="#1e1e1e", fg="gray")
credit_label.pack(side="bottom", pady=1)

# Hotkeys
keyboard.add_hotkey("F8", start_typing)
keyboard.add_hotkey("F9", stop_typing)

root.mainloop()
