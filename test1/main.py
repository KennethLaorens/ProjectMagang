from TTS.api import TTS
import torch
import PyPDF2

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading Tacotron2-DDC model...")
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)
print("✅ Model loaded successfully!")

# --- fungsi baca teks PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

pdf_text = extract_text_from_pdf(
    r"F:\Kuliah\Sem 6\project_magang\main mila ghina\ilovepdf_merged.pdf"
)

# --- generate suara ---
tts.tts_to_file(
    text=pdf_text,
    file_path="output.wav"
)

print("🎙️ Selesai! Hasil disimpan di output.wav")
