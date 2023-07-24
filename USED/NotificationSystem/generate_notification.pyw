import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def create_notification_file(summary, content):
    with open("Development/notification.html", "a") as file:
        file.write(f"<hr><span style=\"font-size:32px;text-align:center;display:block\">{summary}</span><br>")
        content_lines = content.split("\n")
        content_with_br = "<br>".join(content_lines)
        file.write(f"<span style=\"font-size:22px;text-align:center;display:block\">{content_with_br}</span><br><hr><br>\n")



def on_confirm_button_click():
    summary = summary_entry.get().replace("<", "&lt;").replace(">", "&gt;")
    content = content_text.get("1.0", tk.END).replace(">", "&gt;").replace("<", "&lt;")

    if len(summary) != 0 or len(content)-1 != 0 :
        create_notification_file(summary, content)
        messagebox.showinfo("確定", "記録しました。\nありがとうございます。")

        content_text.delete( 0., tk.END )
        summary_entry.delete(0,tk.END)

def on_cancel_button_click():
    root.destroy()

root = tk.Tk()
root.title("不具合・ご意見等連絡")

style = ttk.Style()
style.theme_use("clam")

window_width = 800
window_height = 350
root.geometry("{}x{}+{}+{}".format(window_width,window_height,int(root.winfo_screenwidth()/2 - window_width/2), int(root.winfo_screenheight()/2 - window_height/2)))
root.resizable(False, False)

title_label = ttk.Label(root, text="　　教えてください　　", font=("Helvetica", 24))
title_label.pack(pady=10)

summary_label = ttk.Label(root, text="　概要　", font=("Helvetica", 22))
summary_label.pack()
summary_entry = ttk.Entry(root, font=("Helvetica", 20),width=340)
summary_entry.pack(pady=5, padx=30)

content_label = ttk.Label(root, text="　内容　", font=("Helvetica", 22))
content_label.pack()
content_text = tk.Text(root, font=("Helvetica", 20), wrap=tk.WORD, height=5)
content_text.pack(pady=5, padx=30)

confirm_button = ttk.Button(root, text="確定", command=on_confirm_button_click)
confirm_button.pack(side=tk.LEFT, padx=30, pady=15, fill=tk.X, expand=True)

cancel_button = ttk.Button(root, text="閉じる", command=on_cancel_button_click)
cancel_button.pack(side=tk.LEFT, padx=30, pady=15, fill=tk.X, expand=True)

root.mainloop()