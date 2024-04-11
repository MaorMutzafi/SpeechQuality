<<<<<<< HEAD
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import os
import subprocess
import wave, json
    
def apply_noise_reduction_and_agc(audio_file_path):
    try:
        # Initialize recognizer and read audio file
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust based on the first 0.5 sec of audio for ambient noise
            audio_data = r.record(source)
            sample_rate = source.audio_reader.getframerate()
        
        # File paths
        denoised_file_path = audio_file_path.replace(".wav", "_denoised.wav")
        denoised_agc_file_path = denoised_file_path.replace(".wav", "_agc.wav")
        
        # Save the denoised audio; consider this as placeholder for actual noise reduction
        with wave.open(denoised_file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio_data.sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.get_wav_data())
        
        # Apply AGC using ffmpeg's dynaudnorm filter
        command = [
            'ffmpeg', '-y',  # -y option to overwrite output file if it exists
            '-i', denoised_file_path,  # Input file
            '-filter_complex', 'dynaudnorm=f=150:g=15',  # dynaudnorm filter for AGC
            denoised_agc_file_path  # Output file
        ]
        subprocess.run(command, check=True)
        os.remove(denoised_file_path)
        
        return denoised_agc_file_path
    except Exception as e:
        print(f"Error applying noise reduction and AGC: {e}")
        return None

def recognize_speech_vosk(audio_file_path, model_path):
    model = Model(model_path)
    with wave.open(audio_file_path, "rb") as wf:
        data = wf.readframes(wf.getnframes())
        sr = wf.getframerate()
    rec = KaldiRecognizer(model, sr)
    rec.SetWords(True)
        
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
    else:
        result = json.loads(rec.FinalResult())
    return result
=======
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import os
import subprocess
import wave, json
    
def apply_noise_reduction_and_agc(audio_file_path):
    try:
        # Initialize recognizer and read audio file
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust based on the first 0.5 sec of audio for ambient noise
            audio_data = r.record(source)
            sample_rate = source.audio_reader.getframerate()
        
        # File paths
        denoised_file_path = audio_file_path.replace(".wav", "_denoised.wav")
        denoised_agc_file_path = denoised_file_path.replace(".wav", "_agc.wav")
        
        # Save the denoised audio; consider this as placeholder for actual noise reduction
        with wave.open(denoised_file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio_data.sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.get_wav_data())
        
        # Apply AGC using ffmpeg's dynaudnorm filter
        command = [
            'ffmpeg', '-y',  # -y option to overwrite output file if it exists
            '-i', denoised_file_path,  # Input file
            '-filter_complex', 'dynaudnorm=f=150:g=15',  # dynaudnorm filter for AGC
            denoised_agc_file_path  # Output file
        ]
        subprocess.run(command, check=True)
        os.remove(denoised_file_path)
        
        return denoised_agc_file_path
    except Exception as e:
        print(f"Error applying noise reduction and AGC: {e}")
        return None

def recognize_speech_vosk(audio_file_path, model_path):
    model = Model(model_path)
    with wave.open(audio_file_path, "rb") as wf:
        data = wf.readframes(wf.getnframes())
        sr = wf.getframerate()
    rec = KaldiRecognizer(model, sr)
    rec.SetWords(True)
        
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
    else:
        result = json.loads(rec.FinalResult())
    return result
>>>>>>> speechquality/main
