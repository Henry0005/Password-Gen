import random
import string
import os
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def gerar_senha(tamanho=12, usar_maiusculas=True, usar_numeros=True, usar_simbolos=True):
    caracteres = string.ascii_lowercase
    if usar_maiusculas:
        caracteres += string.ascii_uppercase
    if usar_numeros:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation
    if not caracteres:
        raise ValueError("Nenhuma opção de caractere foi selecionada.")
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

def gerar_nome_arquivo():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"senha_{timestamp}.txt"
    return os.path.join(SCRIPT_DIR, filename)

def salvar_em_log(senha):
    path = os.path.join(SCRIPT_DIR, "senhas_log.txt")
    with open(path, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {senha}\n")
    return path

def interface_terminal():
    print("=== Gerador de Senhas ===")
    try:
        tamanho = int(input("Tamanho da senha: "))
        usar_maiusculas = input("Incluir letras maiúsculas? (s/n): ").strip().lower() == 's'
        usar_numeros = input("Incluir números? (s/n): ").strip().lower() == 's'
        usar_simbolos = input("Incluir símbolos? (s/n): ").strip().lower() == 's'

        senha = gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos)
        print(f"\nSenha gerada: {senha}")

        salvar = input("Deseja salvar a senha? (s/n): ").strip().lower()
        if salvar == 's':
            opcao = input("Salvar em (1) Arquivo único (log) ou (2) Arquivo separado? ").strip()
            if opcao == '1':
                path = salvar_em_log(senha)
                print(f"Senha salva no log: {path}")
            elif opcao == '2':
                path = gerar_nome_arquivo()
                with open(path, "w") as f:
                    f.write(senha)
                print(f"Senha salva em: {path}")
            else:
                print("Opção inválida. Senha não foi salva.")
    except Exception as e:
        print(f"Erro: {e}")

def gerar_senha_gui():
    try:
        tamanho = int(entry_tamanho.get())
        senha = gerar_senha(
            tamanho,
            var_maiusculas.get(),
            var_numeros.get(),
            var_simbolos.get()
        )
        entry_resultado.delete(0, ttk.END)
        entry_resultado.insert(0, senha)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def salvar_senha_gui():
    senha = entry_resultado.get()
    if senha:
        resposta = messagebox.askquestion(
            "Salvar Senha",
            "Deseja salvar no arquivo de log (múltiplas senhas)?\n\n"
            "Clique em 'Sim' para salvar no log (senhas_log.txt)\n"
            "Clique em 'Não' para gerar um arquivo separado"
        )
        if resposta == 'yes':
            path = salvar_em_log(senha)
            messagebox.showinfo("Sucesso", f"Senha salva no log:\n{os.path.basename(path)}")
        else:
            path = gerar_nome_arquivo()
            with open(path, "w") as f:
                f.write(senha)
            messagebox.showinfo("Sucesso", f"Senha salva como:\n{os.path.basename(path)}")
    else:
        messagebox.showwarning("Aviso", "Nenhuma senha para salvar.")

def interface_grafica_moderna():
    global entry_tamanho, entry_resultado, var_maiusculas, var_numeros, var_simbolos

    app = ttk.Window(title="Gerador de Senhas", themename="darkly", size=(420, 350))

    frame = ttk.Frame(app, padding=20)
    frame.pack(fill=BOTH, expand=True)

    ttk.Label(frame, text="Tamanho da senha", font=("Segoe UI", 10, "bold")).pack(pady=5, anchor=CENTER)

    entry_tamanho = ttk.Entry(frame, justify="center", font=("Segoe UI", 10))
    entry_tamanho.insert(0, "12")
    entry_tamanho.pack(fill=X, padx=40)

    var_maiusculas = ttk.BooleanVar(value=True)
    var_numeros = ttk.BooleanVar(value=True)
    var_simbolos = ttk.BooleanVar(value=True)

    ttk.Checkbutton(frame, text="Incluir letras maiúsculas", variable=var_maiusculas).pack(anchor=CENTER, pady=2)
    ttk.Checkbutton(frame, text="Incluir números", variable=var_numeros).pack(anchor=CENTER, pady=2)
    ttk.Checkbutton(frame, text="Incluir símbolos", variable=var_simbolos).pack(anchor=CENTER, pady=2)

    ttk.Button(frame, text="Gerar Senha", bootstyle=INFO, command=gerar_senha_gui, takefocus=0).pack(pady=10, ipadx=10)

    entry_resultado = ttk.Entry(frame, font=("Consolas", 12), justify="center")
    entry_resultado.pack(fill=X, padx=40, pady=5)

    ttk.Button(frame, text="Salvar Senha", bootstyle=SUCCESS, command=salvar_senha_gui, takefocus=0).pack(pady=5, ipadx=10)

    app.mainloop()

if __name__ == "__main__":
    print("=== Gerador de Senhas ===")
    print("1 - Executar no terminal")
    print("2 - Executar com interface gráfica")
    escolha = input("Escolha o modo (1 ou 2): ").strip()

    if escolha == '1':
        interface_terminal()
    elif escolha == '2':
        interface_grafica_moderna()
    else:
        print("Opção inválida.")
