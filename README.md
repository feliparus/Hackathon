# Detecção de Imagens de Objetos Cortantes em Vídeos com YOLO

## Descrição
Este projeto visa detectar objetos cortantes em vídeos usando o modelo YOLO (You Only Look Once). O sistema realiza a análise de vídeos e, ao identificar um objeto cortante, envia um alerta por e-mail. O treinamento do modelo é feito com imagens divididas em três conjuntos: 80% para treinamento, 10% para validação e 10% para teste. A detecção é feita em tempo real, e o resultado final é um vídeo processado com as detecções e alertas enviados por e-mail.

## Estrutura do Projeto
A estrutura do projeto é organizada da seguinte forma:

```sh
├── arquivo/
│   ├── imagens/           # Imagens e rótulos para o treinamento YOLO
│   └── videos/            # Vídeos para análise e onde será salvo o vídeo processado
│
├── include/
│   └── utils.py           # Funções auxiliares utilizadas no projeto
│
├── 1_extracao.ipynb       # Notebook de extração e pré-processamento das imagens
├── 2_treinamento.ipynb    # Notebook de treinamento do modelo YOLO
├── 3_processamento_video.ipynb  # Notebook de processamento do vídeo
├── atualizar_imagens_padrao.bat  # Script BAT para atualizar as imagens e labels
├── requirements.txt       # Arquivo com as dependências do projeto
├── dataset.yaml           # Arquivo de configuração do dataset para o YOLO
```

## Requisitos
Para rodar o projeto, as dependências necessárias serão automaticamente instaladas ao executar o notebook 1_extracao.ipynb, que inclui a linha pip install -r requirements.txt na primeira célula.

Também é necessário gerar o token de acesso no Kaggle, sendo possível gerar no website do Kaggle: Seetings -> API -> Create a new token. Com isso, será baixado automaticamente o arquivo JSON com sua api key, salve-o na pasta .kaggle, localizada por padrão na pasta raiz de usuário.

## Como Rodar
#### 1.Instalar o Jupyter Lab

Se você ainda não tem o Jupyter Lab instalado, pode instalá-lo com o seguinte comando:

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

#### 3.Rodar o Script para Atualização de Imagens e Labels

Execute o script atualizar_imagens_padrao.bat. Ele organiza as imagens e os rótulos em uma sequência lógica, renomeando-os conforme necessário. A sequência de renomeação será: img_1.jpg, img_1.txt, etc.

#### 4.Rodar o Notebook de Treinamento

Após a preparação das imagens, abra e execute o notebook 2_treinamento.ipynb para treinar o modelo YOLO. O treinamento é realizado utilizando as imagens de treinamento, validação e teste.

#### 5.Rodar o Notebook de Processamento de Vídeo

Depois de treinar o modelo, abra o notebook 3_processamento_video.ipynb para processar o vídeo (video.mp4) e detectar os objetos cortantes. O vídeo processado será salvo em arquivo/videos/video_processado.mp4, e os alertas por e-mail serão enviados sempre que um objeto cortante for identificado.

## Detalhes dos Arquivos
arquivo/imagens: Contém as imagens e seus respectivos rótulos (no formato YOLO) utilizados no treinamento.

arquivo/videos: Contém o vídeo original para análise e o vídeo processado será gravado neste diretório.

include/utils.py: Arquivo com funções auxiliares, como processamento de imagem e envio de e-mails.

requirements.txt: Arquivo com as dependências necessárias para o projeto.

dataset.yaml: Arquivo de configuração para o YOLO que define os detalhes do dataset utilizado para o treinamento.

## Exemplo de Uso
1. Organize suas imagens e rótulos na pasta arquivo/imagens e seu vídeo na pasta arquivo/videos.
2. Execute o notebook 1_extracao.ipynb para preparar as imagens.
3. Atualize as imagens e rótulos utilizando o script atualizar_imagens_padrao.bat.
4. Treine o modelo executando 2_treinamento.ipynb.
5. Processando o vídeo e detectando objetos cortantes no arquivo 3_processamento_video.ipynb.
   
## Alerta por E-mail
O sistema envia um alerta por e-mail quando um objeto cortante é detectado no vídeo. Para configurar o envio de e-mails, edite o arquivo include/utils.py e forneça suas credenciais de e-mail no método de envio.
