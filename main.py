import cv2
import tkinter as tk
from tkinter import filedialog

def iniciar_captura_wifi():
    # Inicia a captura via Wi-Fi
    captura = cv2.VideoCapture('http://192.168.2.115:8080/video')
    exibir_video(captura)

def escolher_video():
    # abre uma janela para escolher um vídeo de um diretório
    caminho_video = filedialog.askopenfilename(title="Selecione um vídeo", 
                                               filetypes=(("Arquivos de vídeo", "*.mp4 *.avi *.mov"), ("Todos os arquivos", "*.*")))
    if caminho_video:
        captura = cv2.VideoCapture(caminho_video)
        exibir_video(captura)

def exibir_video(captura):
    if not captura.isOpened():
        print("Não foi possível abrir a captura de vídeo.")
        return

    while captura.isOpened():
        sucesso, quadro = captura.read()

        try:
            if not sucesso:
                print("Falha ao capturar o quadro")
                break

            cv2.imshow("Video", cv2.resize(quadro, (600, 400)))

            tecla = cv2.waitKey(1)
            if tecla == ord('q') or cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
                break

        except cv2.error:
            print("Transmissão encerrada...")
            break

    captura.release()
    cv2.destroyAllWindows()

# configuração da interface gráfica
janela = tk.Tk()
janela.title("Escolha a Fonte de Vídeo")
janela.geometry("300x100")

# botão para iniciar captura via wi-Fi
botao_wifi = tk.Button(janela, text="Captura da câmera via Wi-Fi", command=iniciar_captura_wifi)
botao_wifi.pack(pady=10)

# botão para escolher vídeo de um diretório
botao_video = tk.Button(janela, text="Escolher Vídeo", command=escolher_video)
botao_video.pack(pady=10)

janela.mainloop()
