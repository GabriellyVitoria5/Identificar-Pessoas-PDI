import cv2

# usar IP informado no aplicativo IP webcam
captura = cv2.VideoCapture('http://192.168.2.115:8080/video')

while(captura.isOpened()):

    sucesso, frame = captura.read()

    try:
        if not sucesso:
            print("Falha ao capturar o quadro")
            break

        # mostrar a janela com o vídeo sendo gravado
        cv2.imshow("Video", cv2.resize(frame, (600, 400)))

        # fechar janela ao clicar no 'X' ou apertando telca 'q'
        tecla = cv2.waitKey(1)
        if tecla == ord('q') or cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
            break

    except cv2.error:
        print("Transmissão encerrada...")
        break

captura.release()
cv2.destroyAllWindows()