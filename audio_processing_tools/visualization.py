<<<<<<< HEAD
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os, math

def visualize_with_words_segmented(audio_file_path, result, output_folder):
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    signal, sr = librosa.load(audio_file_path, sr=None)
    total_duration = librosa.get_duration(y=signal, sr=sr)
    segment_duration = 10
    segments = math.ceil(total_duration / segment_duration)
    for segment in range(segments):
        start_time = segment * segment_duration
        end_time = min((segment + 1) * segment_duration, total_duration)
        start_sample = librosa.time_to_samples(start_time, sr=sr)
        end_sample = librosa.time_to_samples(end_time, sr=sr)
        S = librosa.feature.melspectrogram(y=signal[start_sample:end_sample], sr=sr, n_mels=64, fmax=4000, win_length=np.int0(sr*.2), hop_length=np.int0(sr*.1))
        S_dB = librosa.power_to_db(S, ref=np.max)
        plt.figure(figsize=(16, 8))
        librosa.display.specshow(S_dB, sr=sr, hop_length=np.int0(sr*.1), x_axis='time', y_axis='mel', fmax=4000, x_coords = np.linspace(segment*segment_duration, (segment+1)*segment_duration,S.shape[1]))
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Mel-frequency spectrogram: Segment {segment + 1}')

        # Adjust the time axis to start from segment start time
        times = librosa.times_like(S, sr=sr, hop_length=np.int0(sr*.18))
        times = times + start_time  # Shift times to start from the segment's start time
        plt.xticks(np.arange(start_time, end_time, 1), labels=np.arange(start_time, end_time, 1).astype(int))

        if 'result' in result:
            for word_info in result['result']:
                word_start = word_info['start']
                word_end = word_info['end']
                # Plot words that start or end within the segment
                if start_time <= word_start <= end_time or start_time <= word_end <= end_time:
                    # adjusted_start = word_start
                    # adjusted_end = min(word_end, segment_duration)  # Ensure word_end doesn't exceed segment
                    conf = word_info['conf']
                    plt.annotate(f"{word_info['word']}\n{conf:.2f}", (word_start + 0.05, 2000), color='white', fontsize=8, ha='center')
                    plt.plot([word_start, word_end], [1900, 1900], color=np.random.rand(3,) * 0.8 + 0.2, linewidth=2)
        plt.xlim((segment*segment_duration, (segment+1)*segment_duration))
        plt.tight_layout()
        fig_file_path = os.path.join(output_folder, f"{base_name}_spectrogram_segment_{segment + 1}.png")
        plt.savefig(fig_file_path, bbox_inches='tight')
        plt.close()

=======
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os, math

def visualize_with_words_segmented(audio_file_path, result, output_folder):
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    signal, sr = librosa.load(audio_file_path, sr=None)
    total_duration = librosa.get_duration(y=signal, sr=sr)
    segment_duration = 10
    segments = math.ceil(total_duration / segment_duration)
    for segment in range(segments):
        start_time = segment * segment_duration
        end_time = min((segment + 1) * segment_duration, total_duration)
        start_sample = librosa.time_to_samples(start_time, sr=sr)
        end_sample = librosa.time_to_samples(end_time, sr=sr)
        S = librosa.feature.melspectrogram(y=signal[start_sample:end_sample], sr=sr, n_mels=64, fmax=4000, win_length=np.int0(sr*.2), hop_length=np.int0(sr*.1))
        S_dB = librosa.power_to_db(S, ref=np.max)
        plt.figure(figsize=(16, 8))
        librosa.display.specshow(S_dB, sr=sr, hop_length=np.int0(sr*.1), x_axis='time', y_axis='mel', fmax=4000, x_coords = np.linspace(segment*segment_duration, (segment+1)*segment_duration,S.shape[1]))
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Mel-frequency spectrogram: Segment {segment + 1}')

        # Adjust the time axis to start from segment start time
        times = librosa.times_like(S, sr=sr, hop_length=np.int0(sr*.18))
        times = times + start_time  # Shift times to start from the segment's start time
        plt.xticks(np.arange(start_time, end_time, 1), labels=np.arange(start_time, end_time, 1).astype(int))

        if 'result' in result:
            for word_info in result['result']:
                word_start = word_info['start']
                word_end = word_info['end']
                # Plot words that start or end within the segment
                if start_time <= word_start <= end_time or start_time <= word_end <= end_time:
                    # adjusted_start = word_start
                    # adjusted_end = min(word_end, segment_duration)  # Ensure word_end doesn't exceed segment
                    conf = word_info['conf']
                    plt.annotate(f"{word_info['word']}\n{conf:.2f}", (word_start + 0.05, 2000), color='white', fontsize=8, ha='center')
                    plt.plot([word_start, word_end], [1900, 1900], color=np.random.rand(3,) * 0.8 + 0.2, linewidth=2)
        plt.xlim((segment*segment_duration, (segment+1)*segment_duration))
        plt.tight_layout()
        fig_file_path = os.path.join(output_folder, f"{base_name}_spectrogram_segment_{segment + 1}.png")
        plt.savefig(fig_file_path, bbox_inches='tight')
        plt.close()

>>>>>>> speechquality/main
