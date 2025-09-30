import os
from dotenv import load_dotenv, find_dotenv
import pytest
import jiwer
from openai import OpenAI
import logging
import tempfile

load_dotenv(find_dotenv(), override=True)

logging.basicConfig(
    filename="../crisis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

AUDIO_DIR = "tests/audio_samples" 
TRANSCRIPT_DIR = "tests/transcripts"

def transcribe_audio(audio_data, reference_text):
    """Transcribe audio using OpenAI's Whisper model with language detection based on reference."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not client.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        language = "ar" if any(c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي" for c in reference_text) else "en"
        logging.info(f"Detected language for transcription: {language}")
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
            logging.info(f"Temporary audio file created: {temp_file_path}")
        
        with open(temp_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
        
        os.unlink(temp_file_path)
        logging.info(f"Transcription result: {transcript.text.strip()}")
        return transcript.text.strip()
    except Exception as e:
        logging.error(f"Transcription failed: {str(e)}")
        return ""

def read_transcript(file_path):
    """Read transcript file with UTF-8 encoding."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            logging.info(f"Reference transcript from {file_path}: {text}")
            return text
    except Exception as e:
        logging.error(f"Failed to read transcript {file_path}: {str(e)}")
        return ""

def test_wer_for_audio_transcript_pairs():
    """Test WER for each audio-transcript pair."""
    logging.info("Starting WER test for audio-transcript pairs")
    audio_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")])
    transcript_files = sorted([f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".txt")])
    
    logging.info(f"Found audio files: {audio_files}")
    logging.info(f"Found transcript files: {transcript_files}")
    
    assert len(audio_files) == 5, f"Expected 5 audio files, found {len(audio_files)}"
    assert len(transcript_files) == 5, f"Expected 5 transcript files, found {len(transcript_files)}"
    
    results = []
    
    for i, (audio_file, transcript_file) in enumerate(zip(audio_files, transcript_files), 1):
        logging.info(f"Processing pair {i}: {audio_file} vs {transcript_file}")
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
        
        reference = read_transcript(transcript_path)
        if not reference:
            logging.error(f"No reference transcript for {transcript_file}")
            pytest.fail(f"No reference transcript for {transcript_file}")
        
        try:
            with open(audio_path, "rb") as audio:
                audio_data = audio.read()
                if not audio_data:
                    logging.error(f"Empty audio file: {audio_file}")
                    pytest.fail(f"Empty audio file: {audio_file}")
                hypothesis = transcribe_audio(audio_data, reference)
            if not hypothesis:
                logging.error(f"Transcription failed for {audio_file}")
                pytest.fail(f"Transcription failed for {audio_file}")
        except Exception as e:
            logging.error(f"Transcription error for {audio_file}: {str(e)}")
            pytest.fail(f"Transcription error for {audio_file}: {str(e)}")
        
        # Compute WER
        try:
            wer = jiwer.wer(reference, hypothesis)
            logging.info(f"WER for {audio_file} vs {transcript_file}: {wer:.4f}")
            print(f"WER for {audio_file} vs {transcript_file}: {wer:.4f}")
            results.append((audio_file, transcript_file, wer))
        except Exception as e:
            logging.error(f"WER calculation failed for {audio_file}: {str(e)}")
            pytest.fail(f"WER calculation failed for {audio_file}: {str(e)}")
    
    logging.info(f"All WER results: {results}")
    if not results:
        logging.warning("No WER results collected")
        print("No WER results collected")
    else:
        print("Final WER Results:")
        for audio_file, transcript_file, wer in results:
            print(f"WER for {audio_file} vs {transcript_file}: {wer:.4f}")
    
    for audio_file, transcript_file, wer in results:
        if wer > 1.0:
            logging.warning(f"High WER {wer:.4f} for {audio_file} vs {transcript_file}. Check audio-transcript match.")

if __name__ == "__main__":
    pytest.main(["-v", __file__])
