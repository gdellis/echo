#!/bin/bash

# WhisperX Setup Script for Ubuntu
# Automates installation of WhisperX for high-accuracy transcription + speaker diarization

# Exit on error
set -e

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
    echo "Please do not run this script as root. Run as a regular user."
    exit 1
fi

# Update system and install dependencies
echo "Updating system and installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git

# Create and activate a Python virtual environment
echo "Creating Python virtual environment..."
test -d whisperx_env || python3 -m venv whisperx_env
source whisperx_env/bin/activate

# Install WhisperX and required packages
echo "Installing WhisperX and dependencies..."
pip install --upgrade pip
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118  # CUDA for NVIDIA GPUs
pip install whisperx huggingface-hub

# Prompt for Hugging Face token (required for diarization)
read -p "Enter your Hugging Face token (get it from https://huggingface.co/settings/tokens): " HF_TOKEN

# Export Hugging Face token for WhisperX
export HUGGINGFACE_TOKEN="$HF_TOKEN"

# Instructions for running WhisperX
echo ""
echo "WhisperX setup complete!"
echo ""
echo "To transcribe an audio file with speaker diarization, run:"
echo "source whisperx_env/bin/activate"
echo "whisperx your_audio_file.wav --model large-v2 --diarize --hf_token $HUGGINGFACE_TOKEN --output_format txt --output_dir ./output"
echo ""
echo "Replace 'your_audio_file.wav' with your audio file."
echo ""
echo "For CPU-only mode (slower), add '--device cpu' to the command."
echo ""
echo "Example:"
echo "whisperx example.wav --model large-v2 --diarize --hf_token $HUGGINGFACE_TOKEN --output_dir ./output"
