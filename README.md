# Software para Identificar Pessoas - PDI

## Descrição

Projeto final desenvolvido na disciplina de PDI proposto pelo professo Ângelo Magno de Jesus do IFMG Campus Ouro branco, desenvolvido para detectar e contar pessoas e animais em tempo real usando uma câmera estática em um cenário aberto. O sistema utiliza técnicas de Processamento Digital de Imagens (PDI) para identificar e marcar os objetos detectados com bound boxes (retângulos coloridos) e classificar se são adultos, crianças ou animais com base na morfologia dos componentes encontrados.

## Funcionalidades

- **Detecção em Tempo Real**: Detecta e marca pessoas e animais no vídeo ao vivo.
- **Classificação e contagem Objetos**: Identifica e conta objetos como adultos, crianças ou animais.
- **Subtração de Fundo**: Isolamento de objetos em movimento para identificar mudanças no cenário.
- **Limpeza de Ruídos**: Utiliza operações morfológicas para remover ruídos da imagem e melhorar a precisão.
- **Suporte a Streaming**: Conexão com dispositivos móveis para receber e processar vídeo em tempo real.

## Tecnologias Utilizadas

- **Linguagem**: Python
- **IDE**: Visual Studio Code.

**Bibliotecas**:
  - [OpenCV](https://opencv.org/) - Processamento de imagens e visão computacional.
