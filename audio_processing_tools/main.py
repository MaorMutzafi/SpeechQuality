from audio_utils import process_folders
from settings import ROOT_PATH, MODEL_PATH, ORIGINAL_RESULTS_FILE

if __name__ == "__main__":
    process_folders(ROOT_PATH, MODEL_PATH, ORIGINAL_RESULTS_FILE)
