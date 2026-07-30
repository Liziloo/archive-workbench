import torch
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
from sqlmodel import Session, select
from app.models.core import DigitalAsset
import pathlib
import gc

class VisionService:
    def __init__(self, session: Session, force_cpu: bool = False):
        self.session = session
        if force_cpu:
            print("🐌 Force Mode: Using CPU")
            self.device = "cpu"
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"🧠 Loading CLIP model onto {self.device.upper()}...")

        self.model = SentenceTransformer('clip-ViT-B-32', device=self.device)

    def generate_embeddings_for_all(self):
        statement = select(DigitalAsset).where(DigitalAsset.visual_embedding == None)
        assets = self.session.exec(statement).all()

        if not assets:
            print("✅ All assets already have visual embeddings.")
            return

        print(f"📸 Processing {len(assets)} images...")

        for i, asset in enumerate(assets):
            path = pathlib.Path(asset.file_path)
            print(f"[{i+1}/{len(assets)}] {path.name}...", end=" ", flush=True)

            if not path.exists():
                print("❌ Missing")
                continue

            try:
                # 1. Load on CPU and resize to CLIP's native size (224x224)
                # Doing the resize on CPU is MUCH safer for ROCm stability
                Image.MAX_IMAGE_PIXELS = None
                with Image.open(path) as img:
                    img = img.convert("RGB").resize((224, 224))
                    # Convert to NumPy array - this is the "Safe Handshake"
                    img_array = np.array(img)

                # 2. Encode
                with torch.no_grad():
                    embedding = self.model.encode(
                        img_array, # Pass NumPy instead of PIL
                        batch_size=1,
                        convert_to_numpy=True,
                        show_progress_bar=False
                    ).tolist()

                asset.visual_embedding = embedding
                self.session.add(asset)
                self.session.commit()
                print("✅")

                # 3. Aggressive Cleanup
                if i % 5 == 0:
                    gc.collect()
                    if self.device == "cuda":
                        torch.cuda.empty_cache()

            except Exception as e:
                print(f"❌ Error: {e}")
                self.session.rollback()
                continue