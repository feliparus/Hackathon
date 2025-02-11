import cv2
import json
import os
import shutil
import smtplib
import time
import yaml

from email.mime.text import MIMEText
from sklearn.model_selection import train_test_split


def atualizar_datasets_dir(novo_datasets_dir):
    """
    Atualiza o campo `datasets_dir` no arquivo settings.json da Ultralytics.

    Args:
        novo_datasets_dir (str): O novo caminho para o diretório dos datasets.
    """
    try:
        # Obtém o caminho para o diretório AppData\Roaming do usuário atual
        roaming_dir = os.path.join(os.getenv('APPDATA'), 'Ultralytics')
        json_path = os.path.join(roaming_dir, 'settings.json')

        if not os.path.exists(json_path):
            print("Arquivo settings.json não encontrado!")

        # Abre e carrega o conteúdo do JSON
        with open(json_path, 'r') as file:
            settings = json.load(file)

        # Atualiza o campo datasets_dir
        settings['datasets_dir'] = novo_datasets_dir

        # Salva as alterações no arquivo
        with open(json_path, 'w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        print(f"Erro ao atualizar o arquivo: {e}")


def baixar_dataset(api, diretorio_kaggle, diretorio_imagens):
    try:
        api.dataset_download_files(diretorio_kaggle, path=diretorio_imagens, unzip=True)
    except Exception as e:
        print(f"Erro ao baixar o dataset: {e}")


def detectar_video(caminho_video, modelo, conf, iou, imgsz, show, save,
                        save_txt, save_conf, save_crop, stream):

    '''
    Usa o predict para detectar os objetos cortantes no vídeo, os marcando com caixas delimitadoras e exibindo
    seus nomes anotados.
    '''

    results_video = modelo.predict(source=caminho_video,
                                   conf=conf,  # Confiança mínima para detecção
                                   iou=iou,  # Limite de IOU para supressão de caixas sobrepostas
                                   imgsz=imgsz,  # Tamanho da imagem usada pelo modelo
                                   show=show,  # Exibir ou não o vídeo com detecções
                                   save=save,  # Salvar ou não o vídeo com as detecções
                                   save_txt=save_txt,  # Salvar ou não os resultados em arquivos .txt
                                   save_conf=save_conf,  # Incluir ou não a confiança nos .txt
                                   save_crop=save_crop,  # Salvar apenas os objetos detectados recortados
                                   classes=[0],          # Classes a serem identificadas
                                   stream=stream  # Retornar um gerador de frames processados em tempo real
                                   )

    return results_video


def enviar_alerta(email_destino, mensagem):

    '''
    Função destinada a realizar o envio de email através de smtp. Utilizada para enviar relatório de alerta,
    aqui configura-se os dados de acesso do email remetente.
    '''

    remetente = "nome@gmail.com"
    senha = ""

    msg = MIMEText(mensagem)
    msg["Subject"] = "Alerta de Objeto Cortante Detectado"
    msg["From"] = remetente
    msg["To"] = ", ".join(email_destino)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, email_destino, msg.as_string())
        print("Alerta enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar o alerta: {e}")