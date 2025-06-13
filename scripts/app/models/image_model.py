# scripts/app/models/image_model.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import cv2
import pandas as pd
from itertools import combinations
from scripts.app.config import MODEL_IMAGE_PATH, IMG_SIZE, EXCEL_PATH
from scripts.models.U_Net.unet_resnet34 import UNetResNet34# scripts/app/models/image_model.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import cv2
import pandas as pd
from itertools import combinations

from app.config import EXCEL_PATH, IMG_SIZE, MODEL_IMAGE_PATH
from scripts.models.U_Net.unet_resnet34 import UNetResNet34  # yolun doğru olduğundan emin ol

class ImageModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = UNetResNet34().to(self.device)
        state_dict = torch.load(MODEL_IMAGE_PATH, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize(IMG_SIZE),
            transforms.ToTensor()
        ])

    def predict(self, image_path: str) -> float:
        filename = os.path.basename(image_path)
        print(f"🖼️ Görüntü dosyası: {filename}")

        # 1️⃣ mm_per_px değerini al
        df = pd.read_excel(EXCEL_PATH)
        row = df[df['filename'] == filename]
        if row.empty:
            raise ValueError(f"'{filename}' dosyası için Excel'de mm_per_px değeri bulunamadı.")
        mm_per_px = row.iloc[0]['mm_per_px']
        print(f"📏 mm_per_px: {mm_per_px}")

        # 2️⃣ Görüntüyü hazırla
        img = Image.open(image_path).convert("L")
        original_size = img.size
        print(f"🖼️ Orijinal boyut: {original_size}")

        input_tensor = self.transform(img).unsqueeze(0).to(self.device)
        print(f"📦 Girdi tensörü shape: {input_tensor.shape}")

        # 3️⃣ Tahmin maskesi
        with torch.no_grad():
            pred_mask = self.model(input_tensor)
            pred_mask = torch.sigmoid(pred_mask).squeeze().cpu().numpy() * 255
            pred_mask = pred_mask.astype(np.uint8)

        # 4️⃣ Maskeyi yeniden boyutlandır
        pred_mask_resized = cv2.resize(pred_mask, original_size[::-1])

        # 5️⃣ Binary maske ve çizgi uzunluğu
        _, binary = cv2.threshold(pred_mask_resized, 200, 255, cv2.THRESH_BINARY)
        yx = np.argwhere(binary == 255)

        if len(yx) < 2:
            print("⚠️ Yeterli beyaz piksel yok, çap: 0.0 mm")
            return 0.0

        max_dist = max(np.linalg.norm(p1 - p2) for p1, p2 in combinations(yx, 2))
        est_diameter_mm = max_dist * mm_per_px

        print(f"📏 Tahmini çap (mm): {est_diameter_mm:.2f}")
        return est_diameter_mm
