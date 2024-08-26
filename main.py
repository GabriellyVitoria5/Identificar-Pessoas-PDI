import cv2
import tkinter as tk
from tkinter import filedialog
import time

def iniciar_captura_wifi():
    captura = cv2.VideoCapture('http://192.168.2.115:8080/video')
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

    contAdulto = 0
    contCrianca = 0
    contAnimal = 0
    
    if not captura.isOpened():
        print("Não foi possível abrir a captura de vídeo.")
        return
    
    # subtrair fundo
    subtrator_fundo = cv2.createBackgroundSubtractorMOG2() 

    while captura.isOpened():
        retorno, frame = captura.read()

        try:
            if not retorno:
                break
            
            # formato BGR
            corAdulto = (0, 255, 0) # verde
            corCrianca = (255, 0, 0) # azul
            corAnimal = (0, 0, 255) # vermelho

            # texto na tela com os contadores
            cv2.putText(frame, "Adultos: " + str(contAdulto), (0, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, corAdulto, 1)
            cv2.putText(frame, "Criancas: " + str(contCrianca), (200, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, corCrianca, 1)
            cv2.putText(frame, "Animais: " + str(contAnimal), (410, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 1, corAnimal, 1)

            # com o frame capturado, temos:
            #
            # 1° problema: separar objetos (pessoas e animais) do fundo/cenário
            #   - solução: usar função de subtrator de fundo do opencv (usa distribuições gaussianas e é bom para lidar com sombra dos aobjetos)

            imagem_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aplicar_subtrator_fundo = subtrator_fundo.apply(imagem_cinza)
            retorno_th, imagem_binaria = cv2.threshold(aplicar_subtrator_fundo, 200, 255, cv2.THRESH_BINARY) # limpar sombras

            # 2° problema: ruídos no video
            #   - solução: tratar ruídos com operadores morfológicos

            elemento_estruturante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            operador_abertura = cv2.morphologyEx(imagem_binaria, cv2.MORPH_OPEN, elemento_estruturante, iterations = 2)
            operador_dilatacao = cv2.dilate(operador_abertura,elemento_estruturante, iterations = 8)
            operador_fechamento = cv2.morphologyEx(operador_dilatacao, cv2.MORPH_CLOSE, elemento_estruturante, iterations = 8)

            # 3° problema: identificar pessoas
            #   - solução: encontrar bordas e cotornos usando algoritmo de Canny

            bordas = cv2.Canny(operador_fechamento, 50, 150)
            contornos, _ = cv2.findContours(bordas, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            for contorno in contornos:

                #atualizar contadores
                contAdulto = 0
                contCrianca = 0
                contAnimal = 0

                # 4° problema: diferenciar contornos entre pessoas, crianças e animais
                #   - solução: usar a área, altura e largura (proporcao) do contorno

                area = cv2.contourArea(contorno)
                if area > 200: # exlcuir áreas de valores muito pequenos
                    x, y, largura, altura = cv2.boundingRect(contorno)
                    proporcao = largura / float(altura) 
                    #print(largura, altura)
                    #print(proporcao)
                    #print(area)

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
                        contAdulto +=1
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), corAdulto, 2)
                    
                    if (area > 400) and (0.65 <= proporcao < 0.7):
                        contCrianca +=1
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), corCrianca, 2)
                    
                    if (area < 400) and (1 < proporcao < 2.5):
                        contAnimal +=1
                        cv2.rectangle(frame, (x, y), (x + largura, y + altura), corAnimal, 2)

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

botao_video = tk.Button(janela_principal, text="Escolher Vídeo", command=escolher_video)
botao_video.pack(pady=10)

botao_webcam = tk.Button(janela_principal, text="Gravar vídeo da Webcam", command=gravar_webcam)
botao_webcam.pack(pady=10)

janela_principal.mainloop()