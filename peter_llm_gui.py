import os
import threading
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI()

system_prompt = """
You are a bartender creating a drink for someone based on their mood, how the day went, the time of day and year and other factors that might be relevant. You ask questions to get the information you need to create the perfect drink for them. You also ask about their preferences and dietary restrictions. You then create a drink recipe based on the information you have gathered. You also give the drink a name that reflects the mood and ingredients of the drink. You also give a short description of the drink that explains why you chose the ingredients and how they relate to the person's mood and preferences.
When you have enough information, give the final recipe and end with the exact phrase: "Cheers!"
"""

messages = [{"role": "system", "content": system_prompt}]


class BartenderApp:
    def __init__(self, root):
        root.title("AI Bartender")
        root.configure(bg="#1e1e2e")
        root.geometry("620x700")

        header = tk.Label(
            root, text="🍸 AI Bartender", font=("Segoe UI", 18, "bold"),
            bg="#1e1e2e", fg="#f5c542",
        )
        header.pack(pady=(12, 4))

        subtitle = tk.Label(
            root, text="Tell me about your day and I'll craft the perfect drink!",
            font=("Segoe UI", 10), bg="#1e1e2e", fg="#a0a0b0",
        )
        subtitle.pack(pady=(0, 8))

        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED,
            font=("Segoe UI", 11), bg="#2a2a3c", fg="#e0e0e0",
            insertbackground="#e0e0e0", relief=tk.FLAT, padx=10, pady=10,
        )
        self.chat_area.pack(padx=14, pady=(0, 8), fill=tk.BOTH, expand=True)
        self.chat_area.tag_config("user", foreground="#7ec8e3")
        self.chat_area.tag_config("bot", foreground="#f5c542")
        self.chat_area.tag_config("label", font=("Segoe UI", 11, "bold"))

        input_frame = tk.Frame(root, bg="#1e1e2e")
        input_frame.pack(padx=14, pady=(0, 14), fill=tk.X)

        self.entry = tk.Entry(
            input_frame, font=("Segoe UI", 12), bg="#2a2a3c", fg="#e0e0e0",
            insertbackground="#e0e0e0", relief=tk.FLAT,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.entry.focus()

        self.send_btn = tk.Button(
            input_frame, text="Send", font=("Segoe UI", 11, "bold"),
            bg="#f5c542", fg="#1e1e2e", activebackground="#d4a732",
            relief=tk.FLAT, padx=16, command=self.send_message,
        )
        self.send_btn.pack(side=tk.RIGHT, ipady=4)

    def append_message(self, sender, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: ", ("label", "user" if sender == "You" else "bot"))
        self.chat_area.insert(tk.END, f"{text}\n\n", "user" if sender == "You" else "bot")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self.append_message("You", user_text)
        messages.append({"role": "user", "content": user_text})

        self.send_btn.config(state=tk.DISABLED)
        threading.Thread(target=self._get_reply, daemon=True).start()

    def _get_reply(self):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = f"[Error: {e}]"

        self.chat_area.after(0, lambda: self.append_message("Bartender", reply))
        self.chat_area.after(0, lambda: self.send_btn.config(state=tk.NORMAL))


if __name__ == "__main__":
    root = tk.Tk()
    BartenderApp(root)
    root.mainloop()
