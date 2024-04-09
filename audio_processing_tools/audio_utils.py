import os
from pydub import AudioSegment
from speech_processing import apply_noise_reduction_and_agc, recognize_speech_vosk
from quality_estimation import estimate_audio_quality
from results import save_results_to_text
from visualization import visualize_with_words_segmented

def convert_wav_to_mp3(wav_file_path, file_specific_res_folder):
    mp3_file_path = file_specific_res_folder + '\\snd.mp3'
    if not os.path.exists(mp3_file_path):
        sound = AudioSegment.from_wav(wav_file_path)
        sound.export(mp3_file_path, format="mp3", bitrate="192k")
    
def process_folders(root_path, model_path, original_results_file):
    res_base_folder = os.path.join(root_path, "Res")
    if not os.path.exists(res_base_folder):
        os.makedirs(res_base_folder)
    for subdir, dirs, files in os.walk(root_path):
        # if "POSITION_MOVING_SPEECH_06032024032156_Auto_0" not in subdir:
        #     continue
        if 'Data' in subdir:
            res_folder = os.path.join(res_base_folder, os.path.relpath(subdir, start=root_path).replace("Data" + os.sep, ""))
                        
            for filename in files:
                if filename.endswith(".wav"):
                    audio_file_path = os.path.join(subdir, filename)
                    name = audio_file_path.split('\\')[-2]

                    # Check if filename is 'sig.wav' and process each channel
                    if filename == "sig.wav":
                        sound = AudioSegment.from_file(audio_file_path)
                        channels = sound.split_to_mono()
                        
                        for i, channel in enumerate(channels, start=1):
                            channel_filename = f"{os.path.splitext(os.path.basename(audio_file_path))[0]}_ch{i}.wav"
                            channel_path = os.path.join(subdir, channel_filename)
                            channel.export(channel_path, format="wav")
                            
                            file_specific_res_folder = os.path.join(res_folder, os.path.splitext(channel_filename)[0])
                            if not os.path.exists(file_specific_res_folder):
                                os.makedirs(file_specific_res_folder)
                            
                            # Convert channel WAV to MP3 and check if MP3 exists before converting
                            convert_wav_to_mp3(channel_path, file_specific_res_folder)
                            
                            print(f"Processing {name}: channel {i} of {filename}")
                            
                            # Adjust and denoise audio for each channel
                            denoised_file_path = apply_noise_reduction_and_agc(channel_path)
                            
                            # Recognize speech for each channel
                            result = recognize_speech_vosk(denoised_file_path, model_path)
                            
                            # Estimate audio quality for each channel
                            noise_level, volume, confidence_percentile_10, words_per_minute, same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score = estimate_audio_quality(denoised_file_path, result, original_results_file, file_specific_res_folder)
                            
                            # Delete the denoised file after its use
                            os.remove(denoised_file_path)
                                                        
                            # Save results for each channel
                            filename_prefix = os.path.splitext(channel_filename)[0]
                            save_results_to_text(file_specific_res_folder, filename_prefix, result, noise_level, volume, confidence_percentile_10, words_per_minute, same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score)
                            visualize_with_words_segmented(channel_path, result, file_specific_res_folder)
                            
                            # Optionally, delete the channel-specific WAV file to clean up
                            os.remove(channel_path)
                    else:
                        # Process other wav files as usual (if you have any specific processing for them)
                        pass
