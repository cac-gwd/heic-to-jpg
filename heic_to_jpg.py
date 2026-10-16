from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()


def convert(source, destination, quality=92):
    source, destination = Path(source), Path(destination)
    with Image.open(source) as original:
        picture = ImageOps.exif_transpose(original)
        if picture.mode in ('RGBA', 'LA') or 'transparency' in picture.info:
            rgba = picture.convert('RGBA')
            rgb = Image.new('RGB', rgba.size, 'white')
            rgb.paste(rgba, mask=rgba.getchannel('A'))
        else:
            rgb = picture.convert('RGB')
        # Exclusive creation prevents overwriting any existing file.
        index = 0
        while True:
            suffix = '' if index == 0 else f'_{index}'
            target = destination / f'{source.stem}{suffix}.jpg'
            try:
                handle = target.open('xb')
                break
            except FileExistsError:
                index += 1
        try:
            with handle:
                rgb.save(handle, 'JPEG', quality=quality, optimize=True)
        except Exception:
            target.unlink(missing_ok=True)
            raise
    return target


class App:
    def __init__(self, root):
        self.root = root
        self.files = []
        self.events = queue.Queue()
        root.title('HEIC → JPG 変換')
        root.geometry('680x500')
        root.minsize(580, 430)
        panel = ttk.Frame(root, padding=20)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='HEIC → JPG', font=('Yu Gothic UI', 22, 'bold')).pack(anchor='w')
        ttk.Label(panel, text='画像はこのPC内で変換します。元のファイルは変更しません。').pack(anchor='w', pady=(4, 16))
        self.choose = ttk.Button(panel, text='HEIC画像を選択（複数可）', command=self.select)
        self.choose.pack(anchor='w')
        self.listbox = tk.Listbox(panel, height=8)
        self.listbox.pack(fill='both', expand=True, pady=10)
        self.folder = tk.StringVar()
        row = ttk.Frame(panel)
        row.pack(fill='x')
        ttk.Label(row, text='保存先:').pack(side='left')
        ttk.Entry(row, textvariable=self.folder).pack(side='left', fill='x', expand=True, padx=8)
        self.browse = ttk.Button(row, text='選択', command=self.directory)
        self.browse.pack(side='right')
        row2 = ttk.Frame(panel)
        row2.pack(fill='x', pady=12)
        ttk.Label(row2, text='JPG品質 (1〜100):').pack(side='left')
        self.quality = tk.StringVar(value='92')
        ttk.Spinbox(row2, from_=1, to=100, textvariable=self.quality, width=5).pack(side='left', padx=8)
        self.go = ttk.Button(row2, text='JPGに変換', command=self.start)
        self.go.pack(side='right')
        self.progress = ttk.Progressbar(panel)
        self.progress.pack(fill='x')
        self.status = tk.StringVar(value='画像を選択してください。同名ファイルがある場合は連番で保存します。')
        ttk.Label(panel, textvariable=self.status, wraplength=620).pack(anchor='w', pady=(10, 0))
        root.after(100, self.poll)

    def select(self):
        files = filedialog.askopenfilenames(filetypes=[('HEIC / HEIF', '*.heic *.heif *.HEIC *.HEIF'), ('すべて', '*.*')])
        if files:
            self.files = list(files)
            self.listbox.delete(0, 'end')
            for path in files:
                self.listbox.insert('end', path)
            if not self.folder.get():
                self.folder.set(str(Path(files[0]).parent / 'JPG'))
            self.status.set(f'{len(files)}件の画像を選択しました。')

    def directory(self):
        value = filedialog.askdirectory()
        if value:
            self.folder.set(value)

    def start(self):
        try:
            quality = int(self.quality.get())
            if not 1 <= quality <= 100:
                raise ValueError()
        except ValueError:
            messagebox.showerror('入力を確認', '品質は1〜100の整数を指定してください。')
            return
        if not self.files or not self.folder.get().strip():
            messagebox.showerror('入力を確認', '画像と保存先を指定してください。')
            return
        destination = Path(self.folder.get())
        try:
            destination.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            messagebox.showerror('保存先エラー', str(error))
            return
        for button in (self.choose, self.browse, self.go):
            button.configure(state='disabled')
        self.progress.configure(maximum=len(self.files), value=0)
        threading.Thread(target=self.worker, args=(list(self.files), destination, quality), daemon=True).start()

    def worker(self, files, destination, quality):
        failures = []
        for index, file in enumerate(files, 1):
            try:
                convert(file, destination, quality)
            except Exception as error:
                failures.append(f'{Path(file).name}: {error}')
            self.events.put(('progress', index, len(files)))
        self.events.put(('done', len(files) - len(failures), failures))

    def poll(self):
        try:
            while True:
                kind, value, detail = self.events.get_nowait()
                if kind == 'progress':
                    self.progress.configure(value=value)
                    self.status.set(f'変換中: {value} / {detail}件')
                else:
                    for button in (self.choose, self.browse, self.go):
                        button.configure(state='normal')
                    self.status.set(f'完了: 成功 {value}件 / 失敗 {len(detail)}件')
                    if detail:
                        messagebox.showwarning('変換結果', '\n'.join(detail))
                    else:
                        messagebox.showinfo('変換完了', f'{value}件をJPGで保存しました。')
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


if __name__ == '__main__':
    window = tk.Tk()
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == '--verify':
        convert(sys.argv[2], sys.argv[3])
        window.destroy()
    else:
        App(window)
        window.mainloop()
