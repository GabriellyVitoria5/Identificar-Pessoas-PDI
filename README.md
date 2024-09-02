# Software para Identificar Pessoas - PDI

## Descrição

Projeto final desenvolvido na disciplina de PDI proposto pelo professo Ângelo Magno de Jesus do IFMG Campus Ouro branco, desenvolvido para detectar e contar pessoas e animais em tempo real usando uma câmera estática em um cenário aberto. O sistema utiliza técnicas de Processamento Digital de Imagens (PDI) para identificar e marcar os objetos em movimento detectados com bound boxes (retângulos coloridos) e classificar se são adultos, crianças ou animais com base na morfologia dos componentes encontrados. 

## Funcionalidades

- **Captura de vídeo**:
  - Capturar o vídeo em tempo real com câmera conectada à rede via Wi-Fi
  - Capturar diretamente da webcam padrão do dispositivo
  - Escolher um vídeo salvo em um diretório
- **Processamento de Imagem**:
  - Subtração de fundo para separar os objetos em movimento do cenário
  - Aplicação de operações morfológicas para eliminar ruídos
  - Detecção de bordas e contornos usando o algoritmo de Canny
  - Contagem e diferenciação com base em proporção, área e altura dos contornos
- **Visualização**: Exibe o vídeo processado com retângulos coloridos ao redor dos objetos detectados, além de mostrar os contadores de adultos, crianças e animais na tela

## Requisitos

- Python 3.11
- [OpenCV](https://opencv.org/) - Processamento de imagens e visão computacional
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interface gráfica para seleção da fonte de vídeo

## Instalação

Certifique-se de ter o Python 3.11 instalado em seu sistema.

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/projeto-identificacao-pdi.git
    ```
2. Execute o script principal:

    ```bash
    python main.py
    ```

## Uso

1. Ao iniciar o programa, uma janela gráfica será exibida com três botões:
   - **Captura da câmera via Wi-Fi**: Para capturar o vídeo de uma câmera conectada via Wi-Fi (substitua o IP no código para a sua configuração).
   - **Escolher vídeo**: Para selecionar um arquivo de vídeo do seu computador.
   - **Gravar vídeo da Webcam**: Para capturar vídeo diretamente da sua webcam.

2. O vídeo será processado em tempo real, e o sistema exibirá a contagem de adultos, crianças e animais identificados no vídeo.

3. Para sair da visualização do vídeo, pressione a tecla `q` ou feche a janela do vídeo.

## Personalização

- **Alterar IP da câmera Wi-Fi**: Edite a linha `captura = cv2.VideoCapture('http://192.168.2.115:8080/video')` na função `iniciar_captura_wifi()` para o IP da sua câmera.
  - Instale o aplicativo IP Webcam, ecolha a opção Start Server e copie o IP informado na tela para a linha de código
- **Ajustar parâmetros de detecção**: Modifique os valores de área, proporção e altura nas condições dentro da função `exibir_video()` para adaptar o sistema ao seu cenário específico.

