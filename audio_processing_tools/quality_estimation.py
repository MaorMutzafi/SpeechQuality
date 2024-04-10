import librosa
import numpy as np
import csv, os, json
from difflib import SequenceMatcher

def compare_words_with_scores(original_results_file, result, output_folder, threshold=.5, margins=.05, overlap_percentage=0.5):
    def compute_similarity_word_score(original_sequence, processed_sequence):
        """Computes similarity score based on word matches and start time differences."""
        score = 0
        time_diffs = [abs(orig['start'] - proc['start']) for orig, proc in zip(original_sequence, processed_sequence) if orig['word'] == proc['word']]
        score += len(time_diffs)
        time_penalty = sum(time_diffs) / len(time_diffs) if time_diffs else float('inf')
        return score, time_penalty

    def find_best_alignment(original_results, result, window_size=5):
        """Finds the best alignment between original and processed results with minimal time penalty."""
        max_word_score, min_time_penalty, best_offset = 0, float('inf'), 0
        for i in range(len(result) - window_size + 1):
            for j in range(len(original_results) - window_size + 1):
                score, time_penalty = compute_similarity_word_score(original_results[j:j+window_size], result[i:i+window_size])
                if score > max_word_score or (score == max_word_score and time_penalty < min_time_penalty):
                    max_word_score, min_time_penalty = score, time_penalty
                    best_offset = result[i]['start'] - original_results[j]['start']
        return best_offset, max_word_score, min_time_penalty

    def calculate_overlap(start1, end1, start2, end2):
        overlap = max(0, min(end1, end2) - max(start1, start2))
        duration1 = end1 - start1
        duration2 = end2 - start2
        return overlap / min(duration1, duration2)  # Use the smaller duration to ensure at least 90% overlap
    
    file_path = os.path.join(output_folder, 'comparison_results.csv')
    
    with open(original_results_file, 'r') as file:
        original_results = json.load(file)['result']
        
    best_offset, max_word_score, min_time_penalty = find_best_alignment(original_results, result['result'], window_size=5)
    
    adjusted_results = result.copy()
    adjusted_results = [{'word': res['word'], 'start': res['start'] - best_offset, 'end': res['end'] - best_offset, 'conf': res['conf']} for res in adjusted_results['result']]
    # Determine the overall time frame of original_results with margins
    original_start_time = min(original['start'] for original in original_results) - margins
    original_end_time = max(original['end'] for original in original_results) + margins
    # Filter adjusted_results to include only words within the timeframe of original_results
    adjusted_results = [processed for processed in adjusted_results if original_start_time <= processed['start'] <= original_end_time or original_start_time <= processed['end'] <= original_end_time]
    # Scores
    same_score, close_score, wrong_score, made_up_score, miss_score = 0, 0, 0, 0, 0

    all_entries = []  # For storing all entries before sorting and writing

    # Initial Matching for "same" and "close"
    used_adjusted_indices = set()
    for o_idx, original in enumerate(original_results):
        for p_idx, processed in enumerate(adjusted_results):
            if p_idx in used_adjusted_indices:  # Skip if already matched
                continue
            if calculate_overlap(original['start'], original['end'], processed['start'], processed['end']) >= overlap_percentage:
                similarity = SequenceMatcher(None, original['word'], processed['word']).ratio()
                if original['word'] == processed['word']:
                    conclusion = "same"
                    same_score += 1
                elif similarity > threshold:
                    conclusion = "close"
                    close_score += 1
                else:
                    continue  # Move to secondary matching if not same or close
                all_entries.append((original['start'], original['word'], processed['word'], conclusion))
                used_adjusted_indices.add(p_idx)
                break

    # Secondary Matching for "wrong"
    for o_idx, original in enumerate(original_results):
        if o_idx in {entry[0] for entry in all_entries}:  # Skip if this original word is already matched
            continue
        for p_idx, processed in enumerate(adjusted_results):
            if p_idx in used_adjusted_indices:  # Skip if already matched
                continue
            if calculate_overlap(original['start'], original['end'], processed['start'], processed['end']) >= overlap_percentage:
                wrong_score += 1
                all_entries.append((original['start'], original['word'], processed['word'], "wrong"))
                used_adjusted_indices.add(p_idx)
                break

    # Process "miss" and "made-up"
    matched_originals = {entry[1] for entry in all_entries}
    unmatched_originals = [original for original in original_results if original['word'] not in matched_originals]
    for original in unmatched_originals:
        miss_score += 1
        all_entries.append((original['start'], original['word'], 'N/A', "miss"))

    matched_processeds = {entry[2] for entry in all_entries}
    unmatched_processeds = [processed for processed in adjusted_results if processed['word'] not in matched_processeds]
    for processed in unmatched_processeds:
        made_up_score += 1
        all_entries.append((processed['start'], 'N/A', processed['word'], "made up"))

    # Sort all entries by start time and write to CSV
    all_entries.sort(key=lambda x: x[0])
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Original Word", "Adjusted Word", "Conclusion", "Original Time Slice", "Processed Time Slice"])
        for start, original_word, processed_word, conclusion in all_entries:
            original_time_slice = 'N/A' if original_word == 'N/A' else f"[{start:.2f}, {'N/A' if original_word == 'N/A' else next(original for original in original_results if original['word'] == original_word)['end']:.2f}]sec"
            processed_time_slice = 'N/A' if processed_word == 'N/A' else f"[{start:.2f}, {next(processed for processed in adjusted_results if processed['word'] == processed_word)['end']:.2f}]sec"
            writer.writerow([original_word, processed_word, conclusion, original_time_slice, processed_time_slice])

        # Write total scores
        writer.writerow([])
        writer.writerow(["Total Scores", "", "", "", ""])
        writer.writerow(["Same", same_score, "", "", ""])
        writer.writerow(["Close", close_score, "", "", ""])
        writer.writerow(["Wrong", wrong_score, "", "", ""])
        writer.writerow(["Made-up", made_up_score, "", "", ""])
        writer.writerow(["Miss", miss_score, "", "", ""])

    return same_score, close_score, wrong_score, made_up_score, miss_score


def estimate_audio_quality(audio_file_path, result, original_results_file, output_folder):
    signal, sr = librosa.load(audio_file_path, sr=None)
    non_word_signal, word_signal = np.array([]), np.array([])
    word_durations = [(word_info['start'], word_info['end']) for word_info in result.get('result', [])]
    for i, (start_time, end_time) in enumerate(word_durations):
        start_sample, end_sample = int(start_time * sr), int(end_time * sr)
        word_signal = np.concatenate((word_signal, signal[start_sample:end_sample]))
        if i == 0:
            non_word_signal = np.concatenate((non_word_signal, signal[:start_sample]))
        else:
            prev_end_sample = int(word_durations[i-1][1] * sr)
            non_word_signal = np.concatenate((non_word_signal, signal[prev_end_sample:start_sample]))
        if i == len(word_durations) - 1:
            non_word_signal = np.concatenate((non_word_signal, signal[end_sample:]))
    noise_level = np.std(non_word_signal) / np.sqrt(len(non_word_signal)) if len(non_word_signal) > 0 else 0
    volume = np.std(word_signal) / np.sqrt(len(word_signal)) if len(word_signal) > 0 else 0
    confidences = [word_info['conf'] for word_info in result.get('result', [])]
    confidence_percentile_10 = np.percentile(confidences, 10) if confidences else 0
    words_per_minute = len(word_durations) / (librosa.get_duration(y=signal, sr=sr) / 60)
    
    if len(result['text'])>0:
        same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score = compare_words_with_scores(original_results_file, result, output_folder)
    else:
        same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score = 0,0,0,0,0
    
    return noise_level, volume, confidence_percentile_10, words_per_minute, same_word_score, close_word_score, wrong_word_score, made_up_word_score, miss_score

# original_results_file = 'C:\\Users\\User\\Dropbox\\WorkResearch\\MafaatProjects\\Projects\\SpeechQ\\Git\\Data\\OriginalSig\\Original_sig8k_ch1\\Original_timing.txt'
# results_file ='C:/Users/User/Dropbox/WorkResearch/MafaatProjects/Projects/SpeechQ/Git/Res/POSITION_MOVING_SPEECH_06032024032156_Auto_0/sig_ch1/sig_ch1_recognition_results.txt'
# result={}
# with open(results_file, 'r') as file:
#     result = json.load(file)
# q=8/7.25
# for word_info in result['result']:
#     word_info['start'] *= q
#     word_info['end'] *= q

# output_folder = 'C:/Users/User/Dropbox/WorkResearch/MafaatProjects/Projects/SpeechQ/Git/Res/POSITION_MOVING_SPEECH_06032024032156_Auto_0/sig_ch1/'
# compare_words_with_scores(original_results_file, result, output_folder, threshold=.5)