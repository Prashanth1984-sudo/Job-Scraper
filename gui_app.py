import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import pyperclip
from aggregator import scrape_all, save_jobs
import threading

current_jobs_df = None

def search_jobs():
    def task():
        global current_jobs_df
        keyword = keyword_entry.get().strip()
        location = location_entry.get().strip()
        pages = int(pages_entry.get().strip())
        if not keyword or not location:
            messagebox.showerror("Error", "Please enter keyword and location")
            return

        tree.delete(*tree.get_children())
        progress_bar['value'] = 0
        root.update_idletasks()

        current_jobs_df = scrape_all(keyword, location, pages)
        save_jobs(current_jobs_df)

        total = len(current_jobs_df)
        for idx, row in current_jobs_df.iterrows():
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=(row['title'], row['company'], row['location'], row['link']), tags=(tag,))
            progress_bar['value'] = (idx+1)/total*100 if total else 0
            root.update_idletasks()

        progress_bar['value'] = 100

    threading.Thread(target=task).start()

def open_link(event):
    selected_item = tree.selection()
    if selected_item:
        link = tree.item(selected_item, "values")[3]
        webbrowser.open(link)

def copy_all_links():
    if current_jobs_df is None or len(current_jobs_df) == 0:
        messagebox.showerror("Error", "No jobs available to copy")
        return
    all_links = "\n".join(current_jobs_df['link'])
    pyperclip.copy(all_links)
    messagebox.showinfo("Copied", "All apply links copied to clipboard!")

# ------------------------- GUI Setup -------------------------
root = tk.Tk()
root.title("Naukri Job Scraper (India)")
root.geometry("1000x600")
root.minsize(900,500)
root.configure(bg="#f5f5f5")

header_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 11, "bold")

header = tk.Label(root, text="Naukri Job Scraper (India)", font=header_font, bg="#4a90e2", fg="white", pady=10)
header.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0,10))

tk.Label(root, text="Job Keyword", font=label_font, bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="w")
keyword_entry = tk.Entry(root, width=30, font=label_font)
keyword_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Location", font=label_font, bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="w")
location_entry = tk.Entry(root, width=30, font=label_font)
location_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Pages", font=label_font, bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=5, sticky="w")
pages_entry = tk.Entry(root, width=10, font=label_font)
pages_entry.insert(0, "1")
pages_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

search_btn = tk.Button(root, text="Search Jobs", font=button_font, bg="#4a90e2", fg="white", relief="raised", command=search_jobs)
search_btn.grid(row=1, column=2, padx=10, pady=5)

copy_btn = tk.Button(root, text="Copy All Links", font=button_font, bg="#50e3c2", fg="white", relief="raised", command=copy_all_links)
copy_btn.grid(row=2, column=2, padx=10, pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

columns = ("Title", "Company", "Location", "Link")
tree_frame = tk.Frame(root)
tree_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_y.pack(side="right", fill="y")
tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
tree_scroll_x.pack(side="bottom", fill="x")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Link" else 300)
tree.pack(expand=True, fill="both")

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)
tree.bind("<Double-1>", open_link)

tree.tag_configure('evenrow', background="#f0f0f0")
tree.tag_configure('oddrow', background="white")

root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
