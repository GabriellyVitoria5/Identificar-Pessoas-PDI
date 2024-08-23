import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np

def iniciar_captura_wifi():
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
            #   - solução: tratar ruídos com operador morfológico de abertura

            elemento_estruturante = np.ones((5,5),np.uint8) # filtro 5x5
            operador_abertura = cv2.morphologyEx(aplicar_subtrator_fundo, cv2.MORPH_OPEN, elemento_estruturante)

            # 3° problema: identificar pessoas
            #   - solução: encontrar bordar e cotornos usando algoritmo de Canny

            bordas = cv2.Canny(operador_abertura, 50, 150)
            contornos, _ = cv2.findContours(bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            frame_com_borda = frame

            # filtrar contornos com base na área
            for contorno in contornos:
                if cv2.contourArea(contorno) > 200:  
                    x, y, largura, altura = cv2.boundingRect(contorno)
                    cv2.rectangle(frame_com_borda, (x, y), (x + largura, y + altura), (0, 255, 0), 2)

            cv2.imshow("Video", cv2.resize(frame, (600, 400)))
            cv2.imshow('Video separando objetos do fundo', cv2.resize(aplicar_subtrator_fundo, (600, 400)))
            cv2.imshow('Video separando objetos do fundo sem ruido', cv2.resize(operador_abertura, (600, 400)))
            cv2.imshow('Video com borda', cv2.resize(frame_com_borda, (600, 400)))

            tecla = cv2.waitKey(1)
            if tecla == ord('q') or cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
                break

        except cv2.error:
            print("Transmissão encerrada...")
            break

    captura.release()
    cv2.destroyAllWindows()

# configuração da interface gráfica
janela_principal = tk.Tk()
janela_principal.title("Tipo de captura")
janela_principal.geometry("300x100")

# botão para iniciar captura via wi-Fi
botao_wifi = tk.Button(janela_principal, text="Captura da câmera via Wi-Fi", command=iniciar_captura_wifi)
botao_wifi.pack(pady=10)

# botão para escolher vídeo de um diretório
botao_video = tk.Button(janela_principal, text="Escolher Vídeo", command=escolher_video)
botao_video.pack(pady=10)

janela_principal.mainloop()