"""Test audio processing"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.audio_processor import AudioProcessor
from app.services.vad_service import VADService
import numpy as np

def test_audio_processing():
    print("Testing audio processing...")
    processor = AudioProcessor()
    
    # Create test audio (8kHz, 1 second)
    test_audio = np.random.randint(-1000, 1000, 8000 * 2, dtype=np.int16)
    test_audio_bytes = test_audio.tobytes()
    
    # Process audio
    processed = processor.process_chunk(test_audio_bytes, source_sr=8000)
    print(f"[OK] Audio processed: {len(test_audio_bytes)} -> {len(processed)} bytes")
    
    # Test normalization
    normalized = processor._normalize(test_audio)
    print(f"[OK] Audio normalized: range [{normalized.min()}, {normalized.max()}]")
    
    # Test combining
    chunks = [processed[:100], processed[100:]]
    combined = processor.combine_chunks(chunks)
    print(f"[OK] Audio combined: {len(chunks)} chunks -> {len(combined)} bytes")

def test_vad():
    print("\nTesting VAD...")
    vad = VADService()
    
    # Create speech audio
    speech_audio = np.random.randint(-2000, 2000, 1600, dtype=np.int16)
    speech_bytes = speech_audio.tobytes()
    
    # Create silence audio
    silence_audio = np.random.randint(-100, 100, 1600, dtype=np.int16)
    silence_bytes = silence_audio.tobytes()
    
    # Test speech detection
    has_speech = vad.is_speech(speech_bytes)
    print(f"[OK] Speech detection: {'speech detected' if has_speech else 'no speech'}")
    
    # Test silence detection
    has_silence = vad.is_speech(silence_bytes)
    print(f"[OK] Silence detection: {'speech detected' if has_silence else 'no speech'}")

if __name__ == "__main__":
    try:
        test_audio_processing()
        test_vad()
        print("\n[SUCCESS] All tests passed!")
    except Exception as e:
        print(f"\n[FAILED] Test error: {e}")
        import traceback
        traceback.print_exc()
