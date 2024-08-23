import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np

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
    
    # subtrair fundo
    subtrator_fundo = cv2.createBackgroundSubtractorMOG2() 

    while captura.isOpened():
        sucesso, frame = captura.read()

        try:
            if not sucesso:
                break

            # com o frame capturado, temos:
            #
            # 1° problema: separar objetos (pessoas e animais) do fundo/cenário
            #   - solução 1: usar subtração para diferenciar mudanças de um frame para outro (movimento das pessoas)
            #   - solução 2: usar função de subtrator de fundo do opencv (usa distribuições gaussianas e é bom para lidar com sombra dos aobjetos)

            aplicar_subtrator_fundo = subtrator_fundo.apply(frame) 

            # 2° problema: ruídos no video
            #   - solução: usar operador morfológico de abertura

            elemento_estruturante = np.ones((5,5),np.uint8) # filtro 5x5
            operador_abertura = cv2.morphologyEx(aplicar_subtrator_fundo, cv2.MORPH_OPEN, elemento_estruturante)

            cv2.imshow("Video", cv2.resize(frame, (600, 400)))
            cv2.imshow('Video separando objetos do fundo', cv2.resize(aplicar_subtrator_fundo, (600, 400)))
            cv2.imshow('Video separando objetos do fundo sem ruido', cv2.resize(operador_abertura, (600, 400)))

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
