import os
import redis
import torch
from app.core.config import settings

def check_infra():
    print("\n" + "="*60)
    print("🛠️  INFRASTRUCTURE DIAGNOSTIC")
    print("="*60)

    # 1. Check Redis (OMV-Server)
    print(f"📡 Testing Redis Connection: {settings.REDIS_URL}")
    try:
        r = redis.from_url(settings.REDIS_URL, socket_timeout=5)
        r.ping()
        print("✅ REDIS: Connected successfully to OMV-Server.")
    except Exception as e:
        print(f"❌ REDIS: Failed to connect. Error: {e}")

    # 2. Check ROCm / GPU (Local)
    print(f"\n🎮 Testing ROCm / GPU Detection...")
    if torch.cuda.is_available():
        # Even though it's AMD, ROCm-enabled Torch uses the 'cuda' namespace
        device_name = torch.cuda.get_device_name(0)
        print(f"✅ ROCm: GPU Detected!")
        print(f"   Device: {device_name}")
        print(f"   VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("❌ ROCm: No AMD GPU detected by Torch.")
        print("   Ensure ROCm drivers and 'torch-rocm' are installed.")

    print("="*60 + "\n")

if __name__ == "__main__":
    check_infra()