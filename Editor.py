import tkinter
import tkinter.filedialog

def load_text():
    typ = [("Text","*.txt"),("Python","*.py")] 
    fn = tkinter.filedialog.askopenfilename(filetypes=typ)
    if fn != "":
        f = None
        try:
            f = open(fn, 'r', encoding= "utf-8")
            te.delete("1.0", "end")
            te.insert("1.0", f.read())
        except:
            f = open(fn, 'r', encoding= "shift-jis")
            te.delete("1.0", "end")
            te.insert("1.0", f.read())
        finally:
            if f != None:
                f.close()
                

def save_text():
    typ = [("Text", "*.txt")]
    fn = tkinter.filedialog.asksaveasfilename(filetypes=typ)
    if fn != "":
        if fn[-4:] != ".txt":
            fn = fn + ".txt"
        with open(fn, 'w', encoding="utf-8") as f:
            f.write(te.get("1.0","end-1c"))

def col_black():
    te.configure(bg="black", fg="white", insertbackground="white")

def col_white():
    te.configure(bg="white", fg="black", insertbackground="black")

HANKAKU = [
    "ｶﾞ", "ｷﾞ", "ｸﾞ", "ｹﾞ", "ｺﾞ",
    "ｻﾞ", "ｼﾞ", "ｽﾞ", "ｾﾞ", "ｿﾞ",
    "ﾀﾞ", "ﾁﾞ", "ﾂﾞ", "ﾃﾞ", "ﾄﾞ",
    "ﾊﾞ", "ﾋﾞ", "ﾌﾞ", "ﾍﾞ", "ﾎﾞ",
    "ﾊﾟ", "ﾋﾟ", "ﾌﾟ", "ﾍﾟ", "ﾎﾟ",
    "ｱ", "ｲ", "ｳ", "ｴ", "ｵ",
    "ｶ", "ｷ", "ｸ", "ｹ", "ｺ",
    "ｻ", "ｼ", "ｽ", "ｾ", "ｿ",
    "ﾀ", "ﾁ", "ﾂ", "ﾃ", "ﾄ",
    "ﾅ", "ﾆ", "ﾇ", "ﾈ", "ﾉ",
    "ﾊ", "ﾋ", "ﾌ", "ﾍ", "ﾎ",
    "ﾏ", "ﾐ", "ﾑ", "ﾒ", "ﾓ",
    "ﾔ", "ﾕ", "ﾖ",
    "ﾗ", "ﾘ", "ﾙ", "ﾚ", "ﾛ",
    "ﾜ", "ｦ", "ﾝ",
    "ｧ", "ｨ", "ｩ", "ｪ", "ｫ",
    "ｬ", "ｭ", "ｮ", "ｯ",
    "｡", "､", "ｰ", "｢", "｣"
    ]

ZENKAKU = [
    "ガ", "ギ", "グ", "ゲ", "ゴ",
    "ザ", "ジ", "ズ", "ゼ", "ゾ",
    "ダ", "ヂ", "ヅ", "デ", "ド",
    "バ", "ビ", "ブ", "ベ", "ボ",
    "パ", "ピ", "プ", "ペ", "ポ",
    "ア", "イ", "ウ", "エ", "オ",
    "カ", "キ", "ク", "ケ", "コ",
    "サ", "シ", "ス", "セ", "ソ",
    "タ", "チ", "ツ", "テ", "ト",
    "ナ", "ニ", "ヌ", "ネ", "ノ",
    "ハ", "ヒ", "フ", "ヘ", "ホ",
    "マ", "ミ", "ム", "メ", "モ",
    "ヤ", "ユ", "ヨ",
    "ラ", "リ", "ル", "レ", "ロ",
    "ワ", "ヲ", "ン",
    "ァ", "ィ", "ゥ", "ェ", "ォ",
    "ャ", "ュ", "ョ", "ッ",
    "。", "、", "ー", "「", "」"
    ]

def auto_proc():
    txt = te.get("1.0", "end-1c")
    for i in range(len(HANKAKU)):
        txt = txt.replace(HANKAKU[i], ZENKAKU[i])
    te.delete("1.0", "end")
    te.insert("1.0", txt)

root = tkinter.Tk()
root.title("スクロールバー")
fr = tkinter.Frame()
fr.pack(expand=True, fill=tkinter.BOTH)
te = tkinter.Text(fr, width=80, height=30)
sc = tkinter.Scrollbar(fr, orient = tkinter.VERTICAL, command=te.yview)
sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
te.pack(expand=True, fill=tkinter.BOTH)
te[ "yscrollcommand" ] = sc.set

mbar = tkinter.Menu()
mcom = tkinter.Menu(mbar, tearoff = 0)
mcom.add_command(label="読み込み", command=load_text)
mcom.add_separator()
mcom.add_command(label="書き込み", command=save_text)
mbar.add_cascade(label="ファイル", menu=mcom)
mcom2 = tkinter.Menu(mbar, tearoff = 0)
mcom2.add_command(label="黒", command=col_black)
mcom2.add_command(label="白", command=col_white)
mbar.add_cascade(label="背景色", menu=mcom2)
mcom3 = tkinter.Menu(mbar, tearoff = 0)
mcom3.add_command(label="半角ｶﾀｶﾅ→全角カタカナ", command=auto_proc)
mbar.add_cascade(label="自動処理", menu=mcom3)


root["menu"] = mbar

root.mainloop()

