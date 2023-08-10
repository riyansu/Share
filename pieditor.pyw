import tkinter as tk
from tkinter import scrolledtext,filedialog, messagebox
import sys
from io import StringIO
import platform
oskey = "Command" if platform.system()=="Darwin" else "Control"

class RedirectedText:
	def __init__(self, widget):
		self.widget = widget

	def write(self, text):
		self.widget.insert("end", text)
		self.widget.see("end")

class Main(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Pieditor - [Untitled]")

		menu_bar = tk.Menu(self)
		self.config(menu=menu_bar)
		
		self.code_text = scrolledtext.ScrolledText(self, width=30, height=20,font=('',24),bg="white",fg="black",wrap="none",insertbackground="black")
		self.code_text.pack(side="left", fill="both", expand=True)

		self.run_button = tk.Button(self, width=30,text="実行", command=self.run_code,font=('',24),fg="black")
		self.run_button.pack()

		self.console_text = scrolledtext.ScrolledText(self, width=30, height=20,font=('',24),bg="black",fg="white",wrap="none")
		self.console_text.pack(side="right", fill="both", expand=True)
		self.console_text.config(state="disabled")
		self.console_text.tag_configure("error", foreground="#faa")

		sys.stdout = RedirectedText(self.console_text)
		sys.stderr = RedirectedText(self.console_text)
		
		self.file_menu = tk.Menu(menu_bar, tearoff=0)
		self.edit_menu = tk.Menu(menu_bar, tearoff=0)
		self.view_menu = tk.Menu(menu_bar, tearoff=0)
		self.help_menu = tk.Menu(menu_bar, tearoff=0)
		menu_bar.add_cascade(label="ファイル", menu=self.file_menu)
		menu_bar.add_cascade(label="編集", menu=self.edit_menu)
		menu_bar.add_cascade(label="表示", menu=self.view_menu)
		menu_bar.add_cascade(label="ヘルプ", menu=self.help_menu)
		self.file_menu.add_command(label="新規", command=self.new_file, accelerator="{}+N".format(oskey))
		self.file_menu.add_command(label="開く", command=self.open_file, accelerator="{}+O".format(oskey))
		self.file_menu.add_command(label="保存", command=self.save_file, accelerator="{}+S".format(oskey))
		self.file_menu.add_command(label="名前をつけて保存", command=self.save_file_as, accelerator="{}+Shift+S".format(oskey))
		self.edit_menu.add_command(label="実行", command=self.run_code, accelerator="F5")
		self.view_menu.add_command(label="拡大", command=self.zoomin_font, accelerator="{}+]".format(oskey))
		self.view_menu.add_command(label="縮小", command=self.zoomout_font, accelerator="{}+[".format(oskey))
		self.view_menu.add_separator()
		self.view_menu.add_command(label="テーマ切替(白)", command=self.switch_theme, accelerator="{}+T".format(oskey))
		self.view_menu.add_command(label="折り返し(OFF)", command=self.switch_wrap, accelerator="{}+W".format(oskey))
		self.help_menu.add_command(label="Pieditorとは", command=self.show_help, accelerator="{}+I".format(oskey))
		self.bind("<{}-n>".format(oskey), lambda e: self.new_file())
		self.bind("<{}-o>".format(oskey), lambda e: self.open_file())
		self.bind("<{}-s>".format(oskey), lambda e: self.save_file())
		self.bind("<{}-S>".format(oskey), lambda e: self.save_file_as())
		self.bind("<F5>".format(oskey), lambda e: self.run_code())
		self.bind("<{}-t>".format(oskey), lambda e: self.switch_theme())
		self.bind("<{}-w>".format(oskey), lambda e: self.switch_wrap())
		self.bind("<{}-i>".format(oskey), lambda e: self.show_help())
		self.bind("<{}-]>".format(oskey), lambda e: self.zoomin_font())
		self.bind("<{}-[>".format(oskey), lambda e: self.zoomout_font())

		self.file_path = ""
		self.read_file = ""
		self.theme = ["white","black"]
		self.wrap = "none"
		self.fontsize = 24

	def new_file(self):
		if self.code_text.get("1.0", "end-1c") != self.read_file:
			isOK = messagebox.askyesno('保存されていない変更があります','保存されていない変更内容は破棄されます。')
			if not isOK : return
		self.title("Pieditor - [Untitled]")
		self.code_text.delete("1.0", "end")
		self.file_path = ""
		self.read_file = ""

	def open_file(self):
		if self.code_text.get("1.0", "end-1c") != self.read_file:
			isOK = messagebox.askyesno('保存されていない変更があります','保存されていない変更内容は破棄されます。')
			if not isOK : return
		self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py *.pyw")])
		if self.file_path:
			with open(self.file_path, "r") as file:
				self.code_text.delete("1.0", "end")
				self.read_file = file.read()
				self.code_text.insert("1.0", self.read_file)
			self.title("Pieditor - {}".format(self.file_path.split("/")[len(self.file_path.split("/"))-1]))

	def save_file(self):
		if self.file_path:
			with open(self.file_path, "w") as file:
					file.write(self.code_text.get("1.0", "end-1c"))
			self.read_file = self.code_text.get("1.0", "end-1c")
		else:
			self.save_file_as()

	def save_file_as(self):
		self.file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py *.pyw")])
		if self.file_path:
			with open(self.file_path, "w") as file:
				file.write(self.code_text.get("1.0", "end-1c"))
				messagebox.showinfo("保存", "保存が完了しました。")
			self.title("Pieditor - {}".format(self.file_path.split("/")[len(self.file_path.split("/"))-1]))
			self.read_file = self.code_text.get("1.0", "end-1c")

	def run_code(self):
		code = self.code_text.get("1.0", "end-1c")
		old_stdout = sys.stdout
		old_stderr = sys.stderr
		sys.stdout = StringIO()
		sys.stderr = StringIO()

		try:
			exec(code)
		except Exception as e:
			print(e, file=sys.stderr)

		output = sys.stdout.getvalue()
		error = sys.stderr.getvalue()

		sys.stdout = old_stdout
		sys.stderr = old_stderr

		self.console_text.config(state="normal")
		self.console_text.delete("1.0", "end")
		self.console_text.insert("end", output)
		self.console_text.insert("end", error, "error")
		self.console_text.config(state="disabled")

	def zoomin_font(self):
		self.fontsize += 3
		self.code_text.configure(font=('',self.fontsize))
		self.console_text.configure(font=('',self.fontsize))

	def zoomout_font(self):
		self.fontsize -= 3
		self.code_text.configure(font=('',self.fontsize))
		self.console_text.configure(font=('',self.fontsize))

	def view_switch(self):
		self.view_menu.delete(1,2)
		self.view_menu.add_command(label="テーマ切替({})".format("黒" if self.theme[0]=="black" else "白"), command=self.switch_theme, accelerator="{}+T".format(oskey))
		self.view_menu.add_command(label="折り返し({})".format("OFF" if self.wrap=="none" else "ON"), command=self.switch_wrap, accelerator="{}+W".format(oskey))

	def switch_wrap(self):
		self.wrap = "none" if self.wrap == "char" else "char"
		self.code_text.configure(wrap=self.wrap)
		self.view_switch()

	def switch_theme(self):
		self.code_text.configure(fg=self.theme[0],bg=self.theme[1],insertbackground=self.theme[0])
		self.theme.reverse()
		self.view_switch()

	def show_help(self):
		messagebox.showinfo("Pieditorとは？","超簡易テキストエディタ\n（Pythonファイル専用）\nファイルの読み書き、実行ができます。")

if __name__ == "__main__":
	app = Main()
	app.mainloop()
