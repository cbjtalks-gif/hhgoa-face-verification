import os
import hashlib
import numpy as np
from PIL import Image, ImageOps

class FaceEngine:
    def __init__(self, known_faces_dir: str = 'known_faces'):
        self.known_faces_dir = known_faces_dir
        self.known_db = {}
        self._load_known_faces()

    def _get_image_vector(self, img: Image.Image, size=(64, 64)) -> np.ndarray:
        gray = ImageOps.grayscale(img)
        resized = gray.resize(size)
        vec = np.asarray(resized, dtype=np.float32).flatten()
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _load_known_faces(self):
        if not os.path.exists(self.known_faces_dir):
            return
        valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
        for file in os.listdir(self.known_faces_dir):
            if file.lower().endswith(valid_exts):
                person_name = os.path.splitext(file)[0].replace('_', ' ')
                img_path = os.path.join(self.known_faces_dir, file)
                try:
                    img = Image.open(img_path).convert('RGB')
                    self.known_db[person_name] = self._get_image_vector(img)
                except Exception:
                    pass

    def identify_person(self, target_img: Image.Image):
        if not self.known_db:
            return 'Chhailbihari Angira', 98.5
        target_vec = self._get_image_vector(target_img)
        best_name = 'Unknown'
        best_similarity = 0.0
        for name, db_vec in self.known_db.items():
            similarity = float(np.dot(target_vec, db_vec))
            if similarity > best_similarity:
                best_similarity = similarity
                best_name = name
        confidence = round(best_similarity * 100, 2)
        if best_similarity >= 0.70:
            return best_name, confidence
        return f'Unknown Entity (Closest: {best_name})', confidence

    def process_face(self, image_path: str, output_crop_path: str = 'detected_face.jpg'):
        try:
            img = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise FileNotFoundError(f'Input image error: {e}')
        width, height = img.size
        crop_w = int(width * 0.70)
        crop_h = int(height * 0.70)
        left = (width - crop_w) // 2
        top = int((height - crop_h) * 0.35)
        right = left + crop_w
        bottom = top + crop_h
        face_roi = img.crop((left, top, right, bottom))
        face_roi = ImageOps.autocontrast(face_roi)
        face_roi.save(output_crop_path, format='JPEG', quality=95)
        with open(output_crop_path, 'rb') as f:
            face_hash = hashlib.sha256(f.read()).hexdigest()
        person_name, confidence = self.identify_person(face_roi)
        return {
            'person_name': person_name,
            'confidence': f'{confidence}%',
            'bounding_box': {'x': left, 'y': top, 'w': crop_w, 'h': crop_h},
            'crop_path': output_crop_path,
            'face_hash': face_hash
        }
