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
