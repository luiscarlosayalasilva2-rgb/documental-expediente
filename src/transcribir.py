"""Transcribe la voz final con tiempos por palabra (faster-whisper small, CPU)."""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
# PyAV instalado no acepta metadata_errors: se decodifica con ffmpeg y se pasa el array
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                     capture_output=True).stdout
model = WhisperModel('small', device='cpu', compute_type='int8')
segments, info = model.transcribe(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0,
                                  language='es', word_timestamps=True, vad_filter=False, beam_size=5)
words = []
for seg in segments:
    for w in seg.words:
        words.append({'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)})
    print(f'{seg.end:7.1f}s  {seg.text.strip()[:80]}', flush=True)
json.dump(words, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('palabras:', len(words))
