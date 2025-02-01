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


def carregar_classes_yaml(caminho_yaml):
    """
    Carrega as classes interessadas a partir de um arquivo YAML.
    
    Args:
        caminho_yaml (str): Caminho para o arquivo YAML.
        
    Returns:
        list: Lista com os nomes das classes.
    """
    try:
        with open(caminho_yaml, 'r') as f:
            yaml_data = yaml.safe_load(f)
        classes_interessadas = yaml_data.get('names', [])
        if not classes_interessadas:
            raise ValueError("O arquivo YAML não contém a chave 'names' ou está vazio.")
        return classes_interessadas
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo YAML '{caminho_yaml}' não foi encontrado.")


def detectar_video_yaml(caminho_video, caminho_yaml, caminho_video_processado,
                         model, confidence_threshold=0.1, nms_threshold=0.1, imgsz=640):
    classes_interessadas = carregar_classes_yaml(caminho_yaml)

    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        caminho_video_processado, fourcc, cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )

    time.sleep(1)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Realiza a detecção no frame, ajustando a confiança e o NMS
        results = model.predict(frame_rgb, imgsz=imgsz, conf=confidence_threshold, iou=nms_threshold)

        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    # Coordenadas das caixas de detecção
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf.cpu().numpy())  # Conversão explícita
                    class_id = int(box.cls.cpu().numpy())

                    if confidence >= confidence_threshold:
                        label = classes_interessadas[class_id] if class_id < len(classes_interessadas) else "Desconhecido"

                        # Ajuste da caixa para garantir que não saia dos limites da imagem
                        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(frame.shape[1], x2), min(frame.shape[0], y2)

                        # Desenhar a caixa de detecção no vídeo
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label} {confidence:.2f}", 
                                    (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Redimensiona a janela para 60% do tamanho original
        scale_percent = 60
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        frame_resized = cv2.resize(frame, (width, height))

        # Mostrar e salvar o frame processado
        out.write(frame)
        cv2.imshow('Detection', frame_resized)  # Exibir o vídeo processado com redimensionamento

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Vídeo processado salvo em: {caminho_video_processado}")


def dividir_dataset(diretorio_imagens, train_dir, val_dir, test_dir):
    # Obter todas as imagens no diretório de imagens (não precisamos mais das classes)
    imagens = [
        f for f in os.listdir(diretorio_imagens)
        if f.endswith(('.jpg', '.png')) and os.path.exists(os.path.join(diretorio_imagens, f"{os.path.splitext(f)[0]}.txt"))
    ]

    # Dividir as imagens em treino, validação e teste com embaralhamento
    train_imgs, val_imgs = train_test_split(imagens, test_size=0.2, random_state=42, shuffle=True)
    val_imgs, test_imgs = train_test_split(val_imgs, test_size=0.5, random_state=42, shuffle=True)

    # Mover as imagens e seus rótulos para as pastas de treino, validação e teste
    mover_labels_imagens(train_imgs, diretorio_imagens, train_dir)
    mover_labels_imagens(val_imgs, diretorio_imagens, val_dir)
    mover_labels_imagens(test_imgs, diretorio_imagens, test_dir)

    print(f"Divisão do dataset concluída: {len(train_imgs)} imagens para treino, {len(val_imgs)} para validação, {len(test_imgs)} para teste.")


def enviar_alerta(email_destino, mensagem):
    remetente = "remetente@mail.com"
    senha = "sua_senha"

    msg = MIMEText(mensagem)
    msg["Subject"] = "Alerta de Objeto Cortante Detectado"
    msg["From"] = remetente
    msg["To"] = email_destino

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, email_destino, msg.as_string())
        print("Alerta enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar o alerta: {e}")


def mover_labels_imagens(imagens, src_dir, dest_dir):
    # Certificar-se de que o diretório de destino existe
    os.makedirs(dest_dir, exist_ok=True)

    for imagem in imagens:
        imagem_src = os.path.join(src_dir, imagem)
        imagem_dest = os.path.join(dest_dir, imagem)

        # Copiar imagem se ela existir
        if os.path.exists(imagem_src):
            shutil.copy(imagem_src, imagem_dest)

        # Mover o arquivo de label correspondente
        label_nome = imagem.replace('.jpg', '.txt').replace('.png', '.txt')
        label_src = os.path.join(src_dir, label_nome)
        label_dest = os.path.join(dest_dir, label_nome)

        # Copiar o label se ele existir
        if os.path.exists(label_src):
            shutil.copy(label_src, label_dest)