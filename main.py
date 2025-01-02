import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100
    progress_label.config(text=f"Progresso: {percent:.2f}%")

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira um link do YouTube.")
        return

    save_path = filedialog.askdirectory(title="Escolha a pasta para salvar o arquivo")
    if not save_path:
        messagebox.showerror("Erro", "Por favor, escolha uma pasta para salvar o arquivo.")
        return

    custom_name = filename_entry.get().strip()
    if not custom_name:
        messagebox.showerror("Erro", "Por favor, insira um nome para o arquivo.")
        return

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if format_var.get() == "video":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        elif format_var.get() == "audio":
            stream = yt.streams.filter(only_audio=True).first()
        else:
            messagebox.showerror("Erro", "Escolha um formato válido.")
            return

        if not stream:
            messagebox.showerror("Erro", "Nenhum fluxo compatível encontrado.")
            return

        stream.download(output_path=save_path, filename=custom_name)
        messagebox.showinfo("Sucesso", f"'{custom_name}' foi baixado com sucesso em {save_path}!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o vídeo: {e}")

# Configuração da janela principal
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x300")

# Campo para inserção do link
tk.Label(root, text="Link do YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Campo para inserção do nome do arquivo
tk.Label(root, text="Nome do arquivo (sem extensão):").pack(pady=5)
filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# Opções de formato
format_var = tk.StringVar(value="video")
tk.Label(root, text="Escolha o formato:").pack(pady=5)
tk.Radiobutton(root, text="Vídeo", variable=format_var, value="video").pack()
tk.Radiobutton(root, text="Áudio", variable=format_var, value="audio").pack()

# Label de progresso
progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.pack(pady=5)

# Botão de download
download_button = tk.Button(root, text="Baixar", command=download_video)
download_button.pack(pady=20)

# Inicia o loop da interface
root.mainloop()
