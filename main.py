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
    subtrator_fundo = cv2.createBackgroundSubtractorKNN() 

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

                # 4° problema: diferenciar contornos entre pessoas, crianças e animais
                #   - solução: usar a área, altura e largura (proporcao) do contorno

                area = cv2.contourArea(contorno)
                if area > 200: # exlcuir áreas de valores muito pequenos
                    x, y, largura, altura = cv2.boundingRect(contorno)
                    proporcao = largura / float(altura) 
                    #print(largura, altura)
                    #print(proporcao)
                    #print(area)
                    #print("\n")

                    # verificar as proposções e áreas (principalmente a área)!!!!!!!!!!!

                    # Tabela de proporções: 
                    #
                    # 1° caso: proporcao entre 0 e 1 -> altura é maior, valores altos indicam altura e largula próximos
                    # 2° caso: proporcao maior igual que 1 -> largura é maior, valores altos indicam larguras grandes
                    #
                    # adultos: tendem ao 1° caso com valores baixos para médios
                    # crianças: temdem ao 1° caso com valores médios para altos
                    # animais: tendem ao 2° caso com valores baixos
                    # 
                    # 1° caso:
                    #   - proporção para adultos será: 0.2 < prop. < 0.65, e area > 1000
                    #   - proporção para crianças será: 0.66 < prop. < 0.8, e 800 < area > 1000
                    #
                    # 2° caso:
                    #   - proporção para animais será: 1 < prop. < 2.5, e 200 < area < 400

                    if (area > 400) and (0.2 < proporcao < 0.65):
                        print("Adulto")
                        label = "Adulto"
                        cor = (0, 255, 0)  # Verde
                        cv2.rectangle(frame_com_borda, (x, y), (x + largura, y + altura), cor, 2)
                    elif (area > 400) and (0.65 <= proporcao < 0.7):
                        print("Criança")
                        label = "Criança"
                        cor = (255, 255, 0)  # Amarelo
                        cv2.rectangle(frame_com_borda, (x, y), (x + largura, y + altura), cor, 2)
                    elif (area < 200 and area < 400) and (1 < proporcao < 2.5):
                        print("Animal")
                        label = "Animal"
                        cor = (255, 0, 0)  # Azul
                        cv2.rectangle(frame_com_borda, (x, y), (x + largura, y + altura), cor, 2)

                    cv2.rectangle(frame_com_borda, (x, y), (x + largura, y + altura), (0, 255, 0), 2)

            cv2.imshow("Video", cv2.resize(frame, (600, 400)))
            cv2.imshow('Video separando objetos do fundo', cv2.resize(aplicar_subtrator_fundo, (600, 400)))
            cv2.imshow('Video tratado com operador aberto', cv2.resize(operador_abertura, (600, 400)))
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