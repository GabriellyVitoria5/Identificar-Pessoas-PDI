import cv2
import tkinter as tk
from tkinter import filedialog

def iniciar_captura_wifi():
    captura = cv2.VideoCapture('http://192.168.2.115:8080/video') # alterar IP
    exibir_video(captura)

def gravar_webcam():
    captura = cv2.VideoCapture(0)
    exibir_video(captura)

def escolher_video():
    # abrir uma janela para escolher vídeo de um diretório
    caminho_video = filedialog.askopenfilename(title="Selecione um vídeo", 
                                               filetypes=(("Arquivos de vídeo", "*.mp4 *.avi *.mov"), ("Todos os arquivos", "*.*")))
    if caminho_video:
        captura = cv2.VideoCapture(caminho_video)
        exibir_video(captura)

def exibir_video(captura):

    cont_adulto = 0
    cont_crianca = 0
    cont_animal = 0
    cont_frames = 0
    
    if not captura.isOpened():
        print("Não foi possível abrir a captura de vídeo.")
        return
    
    # subtrair fundo
    subtrator_fundo = cv2.createBackgroundSubtractorMOG2() 

    # formato BGR
    cor_adulto = (0, 255, 0) # verde
    cor_crianca = (255, 0, 0) # azul
    cor_animal = (0, 0, 255) # vermelho

    while captura.isOpened():
        retorno, frame = captura.read()

        try:
            if not retorno:
                break
            

            # texto na tela com os contadores
            cv2.putText(frame, "Adultos: " + str(cont_adulto), (0, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, cor_adulto, 3)
            cv2.putText(frame, "Criancas: " + str(cont_crianca), (200, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, cor_crianca, 3)
            cv2.putText(frame, "Animais: " + str(cont_animal), (410, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, cor_animal, 3)

            # com o frame capturado, temos:
            #
            # 1° problema: separar objetos (pessoas e animais) do fundo/cenário
            #   - solução: usar função de subtrator de fundo do opencv (usa distribuições gaussianas e é bom para lidar com sombra dos aobjetos)

            frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aplicar_subtrator_fundo = subtrator_fundo.apply(frame_cinza)
            _, imagem_binaria = cv2.threshold(aplicar_subtrator_fundo, 200, 255, cv2.THRESH_BINARY) # limpar sombras

            # 2° problema: ruídos no video
            #   - solução: tratar ruídos com operadores morfológicos

            elemento_estruturante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            operador_abertura = cv2.morphologyEx(imagem_binaria, cv2.MORPH_OPEN, elemento_estruturante)
            operador_dilatacao = cv2.dilate(operador_abertura,elemento_estruturante, iterations = 8)
            operador_fechamento = cv2.morphologyEx(operador_dilatacao, cv2.MORPH_CLOSE, elemento_estruturante, iterations = 8)

            # 3° problema: identificar pessoas
            #   - solução: encontrar bordas e cotornos usando algoritmo de Canny

            bordas = cv2.Canny(operador_fechamento, 50, 150)
            contornos, _ = cv2.findContours(bordas, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            cont_frames += 1

            # 4° problema: diferenciar contornos entre pessoas, crianças e animais e fazer contagem
            #   - solução: diferenciar usando a área, proporcao e altura do contorno everificar se um contorno está sendo contado mais de uma vez  

            # atualizar contadores mais devagar 
            if cont_frames % 10 == 0:
                cont_adulto = 0
                cont_crianca = 0
                cont_animal = 0

                cont_contornos = []

                for contorno in contornos:
                    area = cv2.contourArea(contorno)
                    if area > 500:
                        x, y, largura, altura = cv2.boundingRect(contorno)
                        proporcao = largura / float(altura)

                        # não contar contornos sobrepostos (evitar contador duplicado)
                        sobreposto = False
                        for c_x, c_y, c_largura, c_altura in cont_contornos:
                            if (x < c_x + c_largura and x + largura > c_x and 
                                y < c_y + c_altura and y + altura > c_y):
                                sobreposto = True
                                break

                        if not sobreposto:
                            cont_contornos.append((x, y, largura, altura))
                            if (area > 2400) and (0.2 < proporcao < 0.8) and (altura >= 80):
                                cont_adulto += 1
                            
                            if (1200 < area < 7000) and (0.3 < proporcao < 0.8) and (45 < altura < 80):
                                cont_crianca += 1
                            
                            if (1750 < area < 2500) and (1.1 <= proporcao < 2.7) and (altura < 50):
                                cont_animal += 1

            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if area > 500: # exlcuir áreas pequenas
                    x, y, largura, altura = cv2.boundingRect(contorno)
                    proporcao = largura / float(altura) 

                    if (area > 2400) and (0.2 < proporcao < 0.8) and (altura >= 80):
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), cor_adulto, 2)
                    
                    if (1200 < area < 7000) and (0.3 < proporcao < 0.8) and (45 < altura < 80):
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), cor_crianca, 2)
                    
                    if (1750 < area < 2500) and (1.1 <= proporcao < 2.7) and (altura < 50):
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), cor_animal, 2)

                    #cv2.rectangle(frame, (x, y), (x + largura, y + altura), (0, 255, 0), 2)

            cv2.imshow("Video", cv2.resize(frame, (400, 300)))
            cv2.imshow('Separar objetos do fundo', cv2.resize(aplicar_subtrator_fundo, (400, 300)))
            cv2.imshow('Imagem binaria', cv2.resize(imagem_binaria, (400, 300)))
            cv2.imshow('Imagem aberta', cv2.resize(operador_abertura, (400, 300)))
            cv2.imshow('Imagem dilatada', cv2.resize(operador_dilatacao, (400, 300)))
            cv2.imshow('Imagem fechada', cv2.resize(operador_fechamento, (400, 300)))

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
janela_principal.geometry("300x140")

botao_wifi = tk.Button(janela_principal, text="Captura da câmera via Wi-Fi", command=iniciar_captura_wifi)
botao_wifi.pack(pady=10)

botao_video = tk.Button(janela_principal, text="Escolher vídeo", command=escolher_video)
botao_video.pack(pady=10)

botao_webcam = tk.Button(janela_principal, text="Gravar vídeo da Webcam", command=gravar_webcam)
botao_webcam.pack(pady=10)

janela_principal.mainloop()