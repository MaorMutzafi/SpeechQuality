
# SpeechQuality

The SpeechQuality is designed as a modular, extensible software suite aimed at researchers, audio engineers, and hobbyists interested in detailed audio analysis and transcription. Leveraging cutting-edge speech recognition technology, audio signal processing, and machine learning algorithms, AAAT offers a range of tools for processing, analyzing, and visualizing audio files. The project prioritizes ease of use, flexibility, and the ability to handle large datasets efficiently.

## Core Features

- **Audio File Conversion**: Converts audio files between various formats, ensuring high fidelity in transformations.
- **Noise Reduction and Enhancement**: Implements advanced noise reduction algorithms to clean audio signals and automatic gain control (AGC) to normalize audio levels.
- **Speech Recognition**: Utilizes the Vosk model for accurate and efficient speech recognition in multiple languages.
- **Audio Visualization**: Creates detailed spectrograms segmented by time, including word annotations, to help visualize audio spectrum and speech components effectively.
- **Audio Quality Estimation**: Assesses audio quality based on noise level, volume, confidence scores, and words per minute.
- **Results Management**: Stores and manages speech recognition and audio quality estimates in various formats for easy integration with other data analysis tools.

## Project Structure

```
SpeechQuality/audio_processing_tools/
│
├── Add_sweep_to_speech.py     # Adds a sweep signal to speech for audio testing purposes
├── load_data_py.py            # Utility script for loading and preprocessing data sets├── main.py                    # Entry point for running audio analysis pipelines
├── audio_conversion.py        # Handles audio file format conversions
├── noise_reduction.py         # Applies noise reduction and audio enhancement techniques
├── speech_recognition.py      # Speech recognition and transcription functions
├── audio_visualization.py     # Generates visualizations for audio data
├── quality_estimation.py      # Estimates and reports on audio quality metrics
├── results_management.py      # Manages the output and storage of analysis results
└── config.py                  # Central configuration file for setting global parameters
```

## Installation

Clone this repository and navigate to the project directory:

```bash
git clone https://github.com/MaorMutzafi/SpeechQuality.git
cd SpeechQuality
```

Install the required dependencies:

```bash
pip install vosk pydub SpeechRecognition matplotlib librosa numpy wave json
```

## Usage

To run the toolkit, execute the following command from the root directory of the project:

```bash
python main.py
```

### Download and Setup Models

Download the Vosk model suitable for your language from [Vosk Models](https://alphacephei.com/vosk/models) and extract it to the `models` directory in your project folder. Or use the model in the GIT folder.

## Usage

1. **Prepare Audio Files**: Place your audio files in the `snds` directory.
2. **Update Configuration**: Modify the `audio_file_path` and `model_path` variables in the script to point to your audio file and the Vosk model directory, respectively.
3. **Run the Script**: Execute the script in your terminal or command prompt.

```bash
python main.py
