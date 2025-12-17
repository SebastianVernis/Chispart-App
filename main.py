#!/usr/bin/env python3
"""
Chispart AI - Plataforma de IA multiagente
Servidor FastAPI para la plataforma de creación con múltiples agentes IA
"""

import os
import json
import logging
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uuid
from multi_agent_workflow.models import (
    DevelopmentCycle,
    ChatMessage,
    GitHubLink,
)
from multi_agent_workflow.state import app_state
from blackbox_hybrid_tool.core.ai_client import AIOrchestrator
from blackbox_hybrid_tool.utils.patcher import apply_unified_diff
from blackbox_hybrid_tool.utils.self_repo import ensure_embedded_snapshot

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

MODEL_CATALOG = {
    "Video": [
        "blackboxai/google/veo-3",
        "blackboxai/google/veo-3-fast",
    ],
    "Image": [
        "blackboxai/black-forest-labs/flux-1.1-pro-ultra",
        "blackboxai/black-forest-labs/flux-schnell",
        "blackboxai/bytedance/hyper-flux-8step",
        "blackboxai/stability-ai/stable-diffusion",
        "blackboxai/prompthero/openjourney",
    ],
    "Text": [
        "blackboxai/google/gemma-2-9b-it:free",
        "blackboxai/mistralai/mistral-7b-instruct:free",
        "blackboxai/meta-llama/llama-3.1-8b-instruct",
    ],
}

# Configuración de límites por modelo para imágenes
IMAGE_MODEL_LIMITS = {
    # Modelos que permiten 1 imagen por solicitud
    "blackboxai/salesforce/blip": 1,
    "blackboxai/andreasjansson/blip-2": 1,
    "blackboxai/philz1337x/clarity-upscaler": 1,
    "blackboxai/krthr/clip-embeddings": 1,
    "blackboxai/sczhou/codeformer": 1,
    "blackboxai/jagilley/controlnet-scribble": 1,
    "blackboxai/fofr/face-to-many": 1,
    "blackboxai/black-forest-labs/flux-1.1-pro": 1,
    "blackboxai/black-forest-labs/flux-1.1-pro-ultra": 1,
    "blackboxai/black-forest-labs/flux-kontext-pro": 1,
    "blackboxai/black-forest-labs/flux-pro": 1,
    "blackboxai/prunaai/flux.1-dev": 1,
    "blackboxai/tencentarc/gfpgan": 1,
    "blackboxai/xinntao/gfpgan": 1,
    "blackboxai/adirik/grounding-dino": 1,
    "blackboxai/pengdaqian2020/image-tagger": 1,
    "blackboxai/allenhooo/lama": 1,
    "blackboxai/yorickvp/llava-13b": 1,
    "blackboxai/google/nano-banana": 1,
    "blackboxai/falcons-ai/nsfw_image_detection": 1,
    "blackboxai/nightmareai/real-esrgan": 1,
    "blackboxai/daanelson/real-esrgan-a100": 1,
    "blackboxai/abiruyt/text-extract-ocr": 1,
    # Modelos que permiten 4 imágenes por solicitud
    "blackboxai/black-forest-labs/flux-dev": 4,
    "blackboxai/black-forest-labs/flux-schnell": 4,
    "blackboxai/bytedance/hyper-flux-8step": 4,
    "blackboxai/ai-forever/kandinsky-2.2": 4,
    "blackboxai/datacte/proteus-v0.2": 4,
    "blackboxai/stability-ai/sdxl": 4,
    "blackboxai/fofr/sdxl-emoji": 4,
    "blackboxai/bytedance/sdxl-lightning-4step": 4,
    "blackboxai/stability-ai/stable-diffusion": 4,
    "blackboxai/stability-ai/stable-diffusion-inpainting": 4,
    # Modelos con más capacidad
    "blackboxai/prompthero/openjourney": 10,
}

# Valor por defecto para modelos no listados
DEFAULT_IMAGE_LIMIT = 1

# Branding configurable por variables de entorno
APP_NAME = os.getenv("APP_NAME", "Blackbox Hybrid Tool")
APP_TAGLINE = os.getenv("APP_TAGLINE", "API para herramienta híbrida de modelos AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Crear aplicación FastAPI con branding configurable
app = FastAPI(
    title=f"{APP_NAME} API",
    description=APP_TAGLINE,
    version=APP_VERSION,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("Middleware CORS configurado con allow_origins=['*']")

# Servir archivos estáticos (playground y frontend principal)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info(f"Directorio static montado desde: {os.path.abspath('static')}")

    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
    logger.info(f"Directorio frontend montado desde: {os.path.abspath('frontend')}")
except Exception as e:
    # Si no existe el directorio, omitir sin fallar
    logger.error(f"Error al montar directorios estáticos: {e}")
    pass


# Modelo de datos para las solicitudes
class ChatRequest(BaseModel):
    prompt: str
    model_type: Optional[str] = None
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    analyze_directory: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    response: str
    model_used: str
    status: str = "success"


class SwitchModelRequest(BaseModel):
    model: str


class WriteFileRequest(BaseModel):
    path: str
    content: str
    overwrite: bool = False


class ApplyPatchRequest(BaseModel):
    patch: str
    root: Optional[str] = None


class ListDirectoryRequest(BaseModel):
    path: str = "."
    show_hidden: bool = False


class ReadFileRequest(BaseModel):
    path: str


class CreateDirectoryRequest(BaseModel):
    path: str


class DeleteFileRequest(BaseModel):
    path: str


class AnalyzeDirectoryRequest(BaseModel):
    path: str = "."
    max_files: int = 50
    include_content: bool = True


class ChangeRootRequest(BaseModel):
    new_root: str


# Instancia global del orquestador
orchestrator = None


@app.on_event("startup")
async def startup_event():
    """Inicializar el orquestador al iniciar la aplicación"""
    global orchestrator
    try:
        config_file = os.getenv("CONFIG_FILE")
        if not config_file or not os.path.exists(config_file):
            config_file = os.getenv(
                "CONFIG_FILE", os.path.join("config", "models.json")
            )
            if not os.path.exists(config_file):
                config_file = os.path.join(
                    "blackbox_hybrid_tool", "config", "models.json"
                )
        orchestrator = AIOrchestrator(config_file)
        if os.getenv("AUTO_SNAPSHOT", "true").lower() in ("1", "true", "yes"):
            try:
                changed, meta = ensure_embedded_snapshot(Path(".").resolve())
                if changed:
                    logger.info(
                        f"Snapshot embebido actualizado (files={meta.get('file_count')}, hash={meta.get('sha256')[:8]}...)"
                    )
                else:
                    logger.info("Snapshot embebido al día")
            except Exception:
                logger.warning("No se pudo generar/verificar snapshot embebido")
        csv_path = os.getenv(
            "BLACKBOX_MODELS_CSV",
            "modelos_blackbox.csv",
        )
        try:
            if os.path.exists(csv_path):
                count = orchestrator.import_available_models_from_csv(csv_path)
                if count:
                    logger.info(f"Modelos disponibles importados desde CSV: {count}")
        except Exception as _:
            pass

        logger.info("Orquestador AI inicializado correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar el orquestador: {str(e)}")
        raise


# ===================================
# Multi-Agent Development Cycle API
# ===================================


class CreateCycleRequest(BaseModel):
    title: str
    initial_prompt: Optional[str] = None


class AddMessageRequest(BaseModel):
    prompt: str
    model_type: Optional[str] = None
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7


@app.get("/cycles", response_model=List[DevelopmentCycle])
async def get_all_cycles():
    """Get all active development cycles."""
    return app_state.get_all_cycles()


@app.post("/cycles", response_model=DevelopmentCycle)
async def create_cycle(request: CreateCycleRequest):
    """Create a new development cycle."""
    new_id = str(uuid.uuid4())
    blackbox_agent = app_state.available_agents.get("blackbox")
    new_cycle = DevelopmentCycle(
        id=new_id,
        title=request.title,
        active_agents=[blackbox_agent] if blackbox_agent else [],
    )
    if request.initial_prompt:
        user_message = ChatMessage(sender="user", text=request.initial_prompt)
        new_cycle.messages.append(user_message)
        if orchestrator and blackbox_agent:
            response_data = orchestrator.generate_response(
                prompt=request.initial_prompt, model_type=blackbox_agent.model
            )
            if isinstance(response_data, dict):
                response_text = response_data.get("content", "")
            else:
                response_text = str(response_data)
            bot_message = ChatMessage(sender=blackbox_agent.id, text=response_text)
            new_cycle.messages.append(bot_message)
    app_state.add_cycle(new_cycle)
    return new_cycle


@app.get("/cycles/{cycle_id}", response_model=DevelopmentCycle)
async def get_cycle(cycle_id: str):
    """Get a specific development cycle by its ID."""
    cycle = app_state.get_cycle(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Development cycle not found")
    return cycle


@app.post("/cycles/{cycle_id}/messages", response_model=ChatMessage)
async def add_message_to_cycle(cycle_id: str, request: AddMessageRequest):
    """Add a message to a cycle and get a response from an agent."""
    cycle = app_state.get_cycle(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    user_message = ChatMessage(sender="user", text=request.prompt)
    cycle.messages.append(user_message)
    if not cycle.active_agents:
        raise HTTPException(status_code=500, detail="No active agents in cycle.")
    primary_agent = cycle.active_agents[0]
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")
    response_data = orchestrator.generate_response(
        prompt=request.prompt,
        model_type=request.model_type or primary_agent.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    if isinstance(response_data, dict):
        response_text = response_data.get("content", "")
    else:
        response_text = str(response_data)
    bot_message = ChatMessage(sender=primary_agent.id, text=response_text)
    cycle.messages.append(bot_message)
    return bot_message


@app.post("/cycles/{cycle_id}/github")
async def link_github_to_cycle(cycle_id: str, link: GitHubLink):
    """Link a GitHub issue/PR to a development cycle."""
    cycle = app_state.get_cycle(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    cycle.github_link = link
    return {"status": "success", "cycle": cycle}


@app.get("/health")
async def health_check():
    """Health check endpoint para verificar el estado del servicio."""
    try:
        if orchestrator is None:
            return {"status": "unhealthy", "error": "Orchestrator not initialized"}
        
        # Verificar que el orquestador esté funcionando
        config_status = "ok" if orchestrator.models_config else "error"
        
        return {
            "status": "healthy",
            "orchestrator": config_status,
            "version": APP_VERSION,
            "app_name": APP_NAME
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/models")
async def get_models():
    """Obtener lista de modelos disponibles."""
    try:
        if orchestrator is None:
            raise HTTPException(status_code=500, detail="Orchestrator not initialized")
        
        # Obtener configuración de modelos
        models_config = orchestrator.models_config.get("models", {})
        default_model = orchestrator.models_config.get("default_model", "auto")
        available_models = orchestrator.models_config.get("available_models", [])
        
        # Formatear respuesta
        models_list = []
        for name, config in models_config.items():
            models_list.append({
                "name": name,
                "model": config.get("model", ""),
                "enabled": config.get("enabled", False)
            })
        
        return {
            "models": models_list,
            "default_model": default_model,
            "available_models": available_models
        }
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/models/switch")
async def switch_model(request: SwitchModelRequest):
    """Cambiar el modelo por defecto."""
    try:
        if orchestrator is None:
            raise HTTPException(status_code=500, detail="Orchestrator not initialized")
        
        # Actualizar el modelo por defecto
        orchestrator.models_config["default_model"] = request.model
        
        # Guardar configuración si es posible
        config_file = orchestrator.config_file
        try:
            with open(config_file, "w") as f:
                json.dump(orchestrator.models_config, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save config: {str(e)}")
        
        return {
            "status": "success",
            "message": f"Model switched to {request.model}",
            "current_model": request.model
        }
    except Exception as e:
        logger.error(f"Error switching model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal de chat con IA."""
    try:
        if orchestrator is None:
            raise HTTPException(status_code=500, detail="Orchestrator not initialized")
        
        logger.info(f"Chat request: prompt='{request.prompt[:50]}...', model={request.model_type}")
        
        # Generar respuesta usando el orquestador
        response_data = orchestrator.generate_response(
            prompt=request.prompt,
            model_type=request.model_type,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Extraer contenido de la respuesta
        if isinstance(response_data, dict):
            response_text = response_data.get("content", str(response_data))
            model_used = response_data.get("model", request.model_type or "auto")
        else:
            response_text = str(response_data)
            model_used = request.model_type or "auto"
        
        return ChatResponse(
            response=response_text,
            model_used=model_used,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/files/write")
async def write_file_endpoint(request: WriteFileRequest):
    """Crear o escribir un archivo de texto."""
    try:
        # Obtener el directorio raíz permitido
        write_root = os.getenv("WRITE_ROOT", "/app")
        
        # Construir ruta absoluta
        target_path = os.path.join(write_root, request.path.lstrip("/"))
        target_path = os.path.abspath(target_path)
        
        # Verificar que la ruta esté dentro del directorio permitido
        if not target_path.startswith(os.path.abspath(write_root)):
            raise HTTPException(
                status_code=403,
                detail="Access denied: path outside allowed directory"
            )
        
        # Verificar si el archivo existe
        if os.path.exists(target_path) and not request.overwrite:
            raise HTTPException(
                status_code=409,
                detail="File already exists. Use overwrite=true to replace."
            )
        
        # Crear directorios intermedios si no existen
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Escribir el archivo
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(request.content)
        
        return {
            "status": "success",
            "path": target_path,
            "size": len(request.content),
            "message": "File written successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error writing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/patch/apply")
async def apply_patch_endpoint(request: ApplyPatchRequest):
    """Aplicar un parche unified diff."""
    try:
        # Obtener el directorio raíz
        root_dir = request.root or os.getenv("WRITE_ROOT", "/app")
        root_path = Path(root_dir).resolve()
        
        # Aplicar el parche
        result = apply_unified_diff(
            patch_content=request.patch,
            root_dir=root_path,
            dry_run=False
        )
        
        return {
            "status": "success",
            "result": result,
            "message": "Patch applied successfully"
        }
    except Exception as e:
        logger.error(f"Error applying patch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/playground")
async def playground():
    """Servir la interfaz de playground."""
    playground_path = os.path.join("static", "playground.html")
    if os.path.exists(playground_path):
        return FileResponse(
            playground_path,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    # Intentar con playground mejorado
    playground_improved = os.path.join("static", "playground_improved.html")
    if os.path.exists(playground_improved):
        return FileResponse(
            playground_improved,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    raise HTTPException(status_code=404, detail="Playground not found")


@app.get("/")
async def read_root():
    """Sirve la interfaz de chat principal."""
    frontend_path = os.path.join("frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(
            frontend_path,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    playground_path = os.path.join("static", "playground.html")
    if os.path.exists(playground_path):
        return FileResponse(
            playground_path,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    return HTMLResponse(
        "<html><body><h1>Error: No se encontró la interfaz</h1></body></html>"
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8006))
    uvicorn.run(app, host="0.0.0.0", port=port)
