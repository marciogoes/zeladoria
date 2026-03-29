import os
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_image(file: UploadFile):
    # Verificar extensão
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Apenas imagens são permitidas")
    
    # Verificar tipo MIME
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Arquivo não é uma imagem")
    
    return True

async def save_upload_file(file: UploadFile) -> str:
    # Validar
    validate_image(file)
    
    # Criar diretório se não existir
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Gerar nome único
    ext = file.filename.split(".")[-1].lower()
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Salvar arquivo
    contents = await file.read()
    
    # Verificar tamanho
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "Arquivo muito grande (máximo 5MB)")
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Otimizar imagem
    try:
        img = Image.open(file_path)
        img.thumbnail((1200, 1200))
        img.save(file_path, optimize=True, quality=85)
    except:
        pass
    
    return f"/{UPLOAD_DIR}/{unique_filename}"

def delete_upload_file(file_path: str):
    try:
        if file_path and os.path.exists(file_path.lstrip("/")):
            os.remove(file_path.lstrip("/"))
    except:
        pass
