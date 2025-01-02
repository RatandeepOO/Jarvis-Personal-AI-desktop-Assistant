from vosk import Model

model_path = "FINAL\\Models\\vosk-model-en-in-0.5"
try:
    model = Model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print("Error:", e)
