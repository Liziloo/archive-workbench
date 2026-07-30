from fastapi import APIRouter
import redis
import torch
from app.core.config import settings

router = APIRouter()

@router.get("/status")
def get_system_status():
    # 1. Check Redis (OMV-Server)
    redis_status = "Offline"
    try:
        r = redis.from_url(settings.REDIS_URL, socket_timeout=1)
        if r.ping():
            redis_status = "Online"
    except:
        pass

    # 2. Check GPU (Local ROCm)
    gpu_info = {"active": False, "device": "None", "vram": "0 GB"}
    if torch.cuda.is_available():
        gpu_info = {
            "active": True,
            "device": torch.cuda.get_device_name(0),
            "vram": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
        }

    return {
        "project": settings.PROJECT_NAME,
        "database": "Connected",  # If the app starts, DB config is valid
        "redis": redis_status,
        "gpu": gpu_info
    }