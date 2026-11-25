import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "entries.json")

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Journal")
        self.root.geometry("400x700")
        self.root.configure(bg="#F9F9FB")

        self.entries = self.load_entries()

        # Header Frame
        header_frame = tk.Frame(root, bg="#F9F9FB")
        header_frame.pack(fill="x", padx=20, pady=15)

        title_lbl = tk.Label(header_frame, text="Journal", font=("Arial", 24, "bold"), bg="#F9F9FB", fg="#000000")
        title_lbl.pack(side="left")

        # Stats Frame (Clickable for Insights)
        stats_frame = tk.Frame(root, bg="#F9F9FB", cursor="hand2")
        stats_frame.pack(fill="x", padx=20, pady=10)
        stats_frame.bind("<Button-1>", lambda e: self.open_insights_window())

        self.lbl_entries = tk.Label(stats_frame, text="0\nEntry This Year", font=("Arial", 9), bg="#F9F9FB", fg="#8E8E93", justify="left", cursor="hand2")
        self.lbl_entries.grid(row=0, column=0, sticky="w", padx=5)
        self.lbl_entries.bind("<Button-1>", lambda e: self.open_insights_window())

        self.lbl_words = tk.Label(stats_frame, text="0\nWord Written", font=("Arial", 9), bg="#F9F9FB", fg="#8E8E93", justify="left", cursor="hand2")
        self.lbl_words.grid(row=0, column=1, sticky="w", padx=5)
        self.lbl_words.bind("<Button-1>", lambda e: self.open_insights_window())

        self.lbl_days = tk.Label(stats_frame, text="0\nDay Journaled", font=("Arial", 9), bg="#F9F9FB", fg="#8E8E93", justify="left", cursor="hand2")
        self.lbl_days.grid(row=0, column=2, sticky="w", padx=5)
        self.lbl_days.bind("<Button-1>", lambda e: self.open_insights_window())

        # Section Label
        section_lbl = tk.Label(root, text="Today", font=("Arial", 16, "bold"), bg="#F9F9FB", fg="#000000")
        section_lbl.pack(anchor="w", padx=20, pady=10)

        # List Frame
        self.list_frame = tk.Frame(root, bg="#F9F9FB")
        self.list_frame.pack(fill="both", expand=True, padx=20)

        # FAB (+)
        fab = tk.Button(
            root, 
            text="+", 
            font=("Arial", 22, "bold"), 
            fg="#5856D6", 
            bg="#FFFFFF", 
            bd=1, 
            relief="raised",
            command=self.add_entry_dialog
        )
        fab.place(relx=0.5, rely=0.92, anchor="center", width=56, height=56)

        self.refresh_ui()

    def load_entries(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        
        default_data = [{"title": "Gym", "body": "Worked out today", "date": datetime.now().strftime("%A, %b %d")}]
        self.save_entries_direct(default_data)
        return default_data

    def save_entries_direct(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def save_entries(self):
        self.save_entries_direct(self.entries)

    def refresh_ui(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        total_entries = len(self.entries)
        total_words = sum(len(f"{e.get('title', '')} {e.get('body', '')}".split()) for e in self.entries)
        unique_days = len(set(e.get('date', '') for e in self.entries))

        self.lbl_entries.config(text=f"{total_entries}\nEntry This Year")
        self.lbl_words.config(text=f"{total_words}\nWord Written")
        self.lbl_days.config(text=f"{unique_days}\nDay Journaled")

        for entry in self.entries:
            card = tk.Frame(self.list_frame, bg="#FFFFFF", bd=1, relief="solid")
            card.pack(fill="x", pady=6, ipady=6, ipadx=8)

            t_lbl = tk.Label(card, text=entry.get('title', ''), font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#000000")
            t_lbl.pack(anchor="w")

            if entry.get('body'):
                b_lbl = tk.Label(card, text=entry.get('body', ''), font=("Arial", 10), bg="#FFFFFF", fg="#3C3C43")
                b_lbl.pack(anchor="w", pady=(2, 0))

            d_lbl = tk.Label(card, text=entry.get('date', ''), font=("Arial", 9), bg="#FFFFFF", fg="#8E8E93")
            d_lbl.pack(anchor="w", pady=(6, 0))

    def open_insights_window(self):
        win = tk.Toplevel(self.root)
        win.title("Insights")
        win.geometry("360x600")
        win.configure(bg="#F2F2F7")

        # Insights Header
        h_frame = tk.Frame(win, bg="#F2F2F7")
        h_frame.pack(fill="x", padx=15, pady=15)

        title = tk.Label(h_frame, text="Insights", font=("Arial", 20, "bold"), bg="#F2F2F7", fg="#000000")
        title.pack(side="left")

        close_btn = tk.Button(h_frame, text="✕", font=("Arial", 10, "bold"), bg="#E5E5EA", fg="#8E8E93", bd=0, command=win.destroy)
        close_btn.pack(side="right")

        # Streaks Card
        s_card = tk.Frame(win, bg="#232A45", bd=0)
        s_card.pack(fill="x", padx=15, pady=10, ipady=10, ipadx=10)

        s_tag = tk.Label(s_card, text="Streaks", font=("Arial", 9), bg="#232A45", fg="#8E8E93")
        s_tag.pack(anchor="w")

        s_title = tk.Label(s_card, text="No Current Streak", font=("Arial", 14, "bold"), bg="#232A45", fg="#FFFFFF")
        s_title.pack(pady=(4, 2))

        s_desc = tk.Label(s_card, text="Journal at least once a week to build a streak.", font=("Arial", 9), bg="#232A45", fg="#A0A5BA")
        s_desc.pack(pady=(0, 10))

        s_btn = tk.Button(s_card, text="Set Schedule", font=("Arial", 10, "bold"), bg="#3E4768", fg="#FFFFFF", bd=0)
        s_btn.pack()

        # Stats Card
        st_card = tk.Frame(win, bg="#5856D6")
        st_card.pack(fill="x", padx=15, pady=10, ipady=10, ipadx=10)

        c_lbl = tk.Label(st_card, text=f"{len(self.entries)}\nEntry\nThis Year", font=("Arial", 16, "bold"), bg="#5856D6", fg="#FFFFFF", justify="left")
        c_lbl.pack(side="left")

        # Calendar Card
        cal_card = tk.Frame(win, bg="#FFFFFF")
        cal_card.pack(fill="x", padx=15, pady=10, ipady=10, ipadx=10)

        cal_title = tk.Label(cal_card, text="October 2026 >", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#000000")
        cal_title.pack(anchor="w", pady=(0, 10))

        days_frame = tk.Frame(cal_card, bg="#FFFFFF")
        days_frame.pack(fill="x")

        days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for idx, d in enumerate(days):
            lbl = tk.Label(days_frame, text=d, font=("Arial", 8, "bold"), bg="#FFFFFF", fg="#C7C7CC")
            lbl.grid(row=0, column=idx, padx=5)

    def add_entry_dialog(self):
        title = simpledialog.askstring("New Entry", "Enter Title:")
        if title:
            body = simpledialog.askstring("New Entry", "Enter Thoughts/Body (Optional):") or ""
            today_str = datetime.now().strftime("%A, %b %d")
            self.entries.insert(0, {"title": title, "body": body, "date": today_str})
            self.save_entries()
            self.refresh_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()