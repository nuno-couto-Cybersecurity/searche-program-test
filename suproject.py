import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import subprocess
import sys
import shutil
import time

# Define a pasta base dentro da pasta dist
if getattr(sys, 'frozen', False):  # Quando rodando como .exe
    pasta_base = os.path.join(os.path.dirname(sys.executable), "documentos_utentes")
else:  # Quando rodando como script .py
    pasta_base = os.path.join(os.path.dirname(__file__), "documentos_utentes")

# Define a pasta correta de origem dos documentos digitalizados
pasta_origem = os.path.join(pasta_base, "scanner_teste")

def organizar_documentos():
    """Verifica novos arquivos na pasta de digitalização e os organiza automaticamente."""
    if not os.path.exists(pasta_origem):
        print(f"⚠️ A pasta de origem '{pasta_origem}' não existe.")
        return

    arquivos = os.listdir(pasta_origem)
    print(f"📂 Arquivos detectados na pasta: {arquivos}")

    for arquivo in arquivos:
        if arquivo.endswith(".pdf") or arquivo.endswith(".jpg"):  # Filtrar apenas documentos digitalizados
            nome_utente = arquivo.split("_")[0].replace(" ", "")  # Remove espaços para garantir correspondência correta
            caminho_pasta_utente = os.path.join(pasta_base, nome_utente)

            # Criar pasta do utente se não existir
            if not os.path.exists(caminho_pasta_utente):
                os.makedirs(caminho_pasta_utente)
                print(f"✅ Criada pasta: {caminho_pasta_utente}")

            # Mover arquivo para a pasta correspondente
            shutil.move(os.path.join(pasta_origem, arquivo), os.path.join(caminho_pasta_utente, arquivo))
            print(f"📄 Movido {arquivo} para {caminho_pasta_utente}")

def pesquisar():
    # Limpar botões anteriores antes de adicionar novos
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    nome = entry_nome.get().strip().lower().replace(" ", "")  # Remove espaços da pesquisa
    data_nascimento = entry_data.get().strip()
    processo = entry_processo.get().strip()
    sns = entry_sns.get().strip()

    if nome or data_nascimento or processo or sns:
        encontrados = []

        for pasta in os.listdir(pasta_base):
            caminho_pasta = os.path.join(pasta_base, pasta)
            if not os.path.isdir(caminho_pasta):  # Garantir que só pastas sejam processadas
                continue

            pasta_lower = pasta.lower().replace(" ", "")  # Remove espaços da pasta antes de comparar
            if (nome and nome in pasta_lower) or (data_nascimento and data_nascimento in pasta) or \
                    (processo and processo in pasta) or (sns and sns in pasta):
                encontrados.append(pasta)

        if len(encontrados) > 1:
            messagebox.showwarning("Múltiplos utentes encontrados",
                                   "Foram encontrados vários utentes. Refine a pesquisa.")
        elif encontrados:
            pasta = encontrados[0]
            caminho_pasta = os.path.join(pasta_base, pasta)

            documentos = os.listdir(caminho_pasta)

            if documentos:
                resultado = f"Documentos encontrados para '{pasta}':\n" + "\n".join(documentos)

                for doc in documentos:
                    caminho_doc = os.path.join(pasta_base, pasta, doc)
                    tk.Button(frame_resultados, text=f"Abrir {doc}",
                              command=lambda c=caminho_doc: abrir_documento(c)).pack()

                # Criar botão para abrir a pasta no Explorer
                tk.Button(frame_resultados, text="Abrir Pasta",
                          command=lambda p=os.path.join(pasta_base, pasta): abrir_pasta(p)).pack(pady=5)
            else:
                resultado = f"Nenhum documento encontrado para '{pasta}'."

            messagebox.showinfo("Resultado da Pesquisa", resultado)
        else:
            messagebox.showinfo("Nenhum utente encontrado", "Nenhum utente corresponde aos critérios fornecidos.")
    else:
        messagebox.showerror("Erro", "Insira pelo menos um critério de pesquisa.")

def abrir_documento(caminho):
    try:
        webbrowser.open(caminho)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o documento.\n{str(e)}")

def abrir_pasta(pasta):
    try:
        subprocess.Popen(f'explorer "{pasta}"')  # Abre a pasta no Windows Explorer
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a pasta.\n{str(e)}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Consulta de Documentos de Utentes")
janela.geometry("400x450")

tk.Label(janela, text="Nome do Utente:").pack()
entry_nome = tk.Entry(janela, width=50)
entry_nome.pack()

tk.Label(janela, text="Data de Nascimento (DD-MM-AAAA):").pack()
entry_data = tk.Entry(janela, width=50)
entry_data.pack()

tk.Label(janela, text="Número de Processo:").pack()
entry_processo = tk.Entry(janela, width=50)
entry_processo.pack()

tk.Label(janela, text="Número SNS:").pack()
entry_sns = tk.Entry(janela, width=50)
entry_sns.pack()

tk.Button(janela, text="Pesquisar Documentos", command=pesquisar).pack(pady=10)

# Criar um frame onde os botões de documentos serão adicionados
frame_resultados = tk.Frame(janela)
frame_resultados.pack(pady=10)

# Iniciar monitoramento automático da pasta de digitalização
janela.after(10000, organizar_documentos)  # Chama a função a cada 10 segundos

janela.mainloop()
