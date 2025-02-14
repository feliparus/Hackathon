# Detecção de Imagens de Objetos Cortantes em Vídeos com YOLO

## Descrição
Este projeto visa detectar objetos cortantes em vídeos usando o modelo YOLO (You Only Look Once). O sistema realiza a análise de vídeos e, ao identificar um objeto cortante, envia um alerta por e-mail. O treinamento do modelo é feito com imagens divididas em aproximadamente: 75% para treinamento, 15% para validação e 10% para teste. A detecção é feita com método 'predict()' da biblioteca Ultralytics, e o resultado final é um vídeo processado com as detecções e alertas enviados por e-mail.

## Estrutura do Projeto
A estrutura **base** do projeto é organizada da seguinte forma:

```sh
├── arquivo/
│   ├── imagens/           # Imagens e rótulos para o treinamento YOLO
       └── dataset-hackathon # Dataset principal com as imagens e labels de cada pasta (test, train, valid), será criada ao baixar o dataset do kaggle.
          └── test
          └── train
          └── valid
├── include/
│   └── utils.py    # Funções auxiliares utilizadas no projeto
├── modelo/
   └── best.pt      # Modelo treinado no código
   └── yolo11s.pt   # Modelo pré-treinado YOLO
├── videos/
   └── video.mp4
   └── video2.mp4
├── 1_extracao.ipynb       # Notebook de extração e pré-processamento das imagens
├── 2_treinamento.ipynb    # Notebook de treinamento do modelo YOLO
├── 3_processamento_video.ipynb  # Notebook de processamento do vídeo
├── requirements.txt       # Arquivo com as dependências do projeto
├── dataset.yaml           # Arquivo de configuração do dataset para o YOLO
```
Obs: As demais pastas presentes no projeto, são pastas auxiliares e/ou criadas na hora da execução.

## Requisitos
Para rodar o projeto, as dependências necessárias serão automaticamente instaladas ao executar o notebook 1_extracao.ipynb, que inclui a linha pip install -r requirements.txt na primeira célula.

Há também a necessidade de criar o arquivo .env contendo as informações:
diretorio_kaggle = ""
email = "email_remetente"
senha_email = "senha_remetente"

## Como Rodar
#### 1.Instalar IDE com suporte para arquivos .ipynb

Exemplo Jupyer Lab:

```sh
pip install jupyterlab
```

Para abrir o Jupyter Lab, execute o comando:

```sh
jupyter lab
```

Isso abrirá o Jupyter Lab em seu navegador.

#### 2.Rodar o Notebook de Extração de Imagens

No Jupyter Lab, abra o arquivo 1_extracao.ipynb e execute as células para realizar a extração e o pré-processamento das imagens.

#### 3.Rodar o Notebook de Treinamento

Após a preparação das imagens, abra e execute o notebook 2_treinamento.ipynb para treinar o modelo YOLO. O treinamento é realizado utilizando as imagens de treinamento, validação e teste para inferência. O modelo treinado será salvo em 'modelo/best.pt' e suas estatísticas do Ultralytics em 'runs/detect/train'.

#### 4.Rodar o Notebook de Processamento de Vídeo

Depois de treinar o modelo, abra o notebook 3_processamento_video.ipynb para processar o vídeo (video.mp4 e video2.mp4) e detectar os objetos cortantes. Os vídeos processados serão salvos nas pastas de 'predict, predict2, etc...' dentro da estrutura 'runs/detect/.../video.avi', e os alertas de e-mail serão enviados sempre que um objeto cortante for identificado, sendo enviado um primeiro e-mail para a primeira detecção, e em seguida um segundo e-mail contendo o relatório de detecções ao longo do vídeo.

## Exemplo de Uso
1. Baixe o dataset do kaggle através da variável de ambiente configurada no .env, executando o notebook 1_extracao.ipynb para preparar as imagens.
2. Treine o modelo executando 2_treinamento.ipynb.
3. Teste a inferência do modelo na célula de execução do predict() para as imagens de teste da pasta 'test'.
4. Processe o vídeo e detectando objetos cortantes no arquivo 3_processamento_video.ipynb.
   
## Alerta por E-mail
O sistema envia um alerta por e-mail quando um objeto cortante é detectado no vídeo. Para configurar o envio de e-mails, edite o arquivo .env e forneça suas credenciais de e-mail.
