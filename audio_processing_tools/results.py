import json
import os


def save_results_to_text(output_folder, filename_prefix, result, noise_level, volume, confidence_percentile_10, words_per_minute, same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score):
    results_path = os.path.join(output_folder, f"{filename_prefix}_recognition_results.txt")
    with open(results_path, "w") as f:
        json.dump(result, f, indent=4)
    audio_quality_path = os.path.join(output_folder, f"{filename_prefix}_audio_quality.txt")
    with open(audio_quality_path, "w") as f:
        f.write(f"Noise Level: {noise_level}\nVolume: {volume}\nConfidence percentile 10: {confidence_percentile_10}\nWords per Minute: {words_per_minute}\nSame Word Score: {same_word_score}\nClose Word Score: {close_word_score}\nWrong Word Score: {wrong_word_score}\nMade-up Word Score: {made_up_word_score}\nMiss Word Score: {miss_score}")
    srt_path = os.path.join(output_folder, f"{filename_prefix}_subtitles.srt")
    with open(srt_path, "w") as srt_file:
        counter = 1
        for word_info in result.get('result', []):
            start_time, end_time = word_info['start'], word_info['end']
            start_srt = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
            end_srt = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"
            srt_file.write(f"{counter}\n{start_srt} --> {end_srt}\n{word_info['word']}\n\n")
            counter += 1
