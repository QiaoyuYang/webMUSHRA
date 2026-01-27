#!/bin/bash
#
# Create placeholder audio files for webMUSHRA testing
# Run this from your webMUSHRA directory: bash create_placeholder_audio.sh
#

set -e  # Exit on error

AUDIO_DIR="configs/resources/audio"
DURATION=5  # seconds
SAMPLE_RATE=48000

# Define conditions (filename and frequency in Hz for placeholder tones)
declare -A CONDITIONS=(
    ["reference"]=440
    ["anchor_opus"]=220
    ["yourcodec_7.5k"]=330
    ["yourcodec_4.5k"]=350
    ["dac_7.5k"]=370
    ["dac_4.5k"]=390
    ["encodec_6.0k"]=410
)

# Define trials
TRIALS=(
    "training"
    "trial01"
    "trial02"
    "trial03"
    "trial04"
    "trial05"
    "trial06"
    "trial07"
    "trial08"
    "trial09"
    "trial10"
    "trial11"
    "trial12"
)

echo "=========================================="
echo "Creating placeholder audio for MUSHRA test"
echo "=========================================="
echo ""

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: ffmpeg is not installed"
    echo "   Install with: sudo apt install ffmpeg"
    exit 1
fi

# Create base directory
mkdir -p "$AUDIO_DIR"

# Create audio files for each trial
for trial in "${TRIALS[@]}"; do
    echo "📁 Creating: $AUDIO_DIR/$trial/"
    mkdir -p "$AUDIO_DIR/$trial"
    
    for condition in "${!CONDITIONS[@]}"; do
        freq=${CONDITIONS[$condition]}
        output_file="$AUDIO_DIR/$trial/${condition}.wav"
        
        # Add slight frequency variation per trial to make them distinguishable
        trial_num=${trial#trial}  # Remove "trial" prefix
        if [[ "$trial_num" =~ ^[0-9]+$ ]]; then
            freq=$((freq + trial_num * 2))
        fi
        
        # Generate sine wave
        ffmpeg -f lavfi -i "sine=frequency=${freq}:duration=${DURATION}" \
               -ar $SAMPLE_RATE \
               -loglevel error \
               "$output_file" -y
        
        echo "   ✓ ${condition}.wav (${freq}Hz)"
    done
    echo ""
done

echo "=========================================="
echo "✅ Done! Created placeholder audio for ${#TRIALS[@]} trials"
echo ""
echo "Directory structure:"
echo "$AUDIO_DIR/"
for trial in "${TRIALS[@]}"; do
    echo "├── $trial/"
    for condition in "${!CONDITIONS[@]}"; do
        echo "│   ├── ${condition}.wav"
    done
done
echo ""
echo "Next steps:"
echo "1. git add configs/resources/audio/"
echo "2. git commit -m 'Add placeholder audio files'"
echo "3. git push origin master"
echo ""
echo "Then test at:"
echo "https://kaleidoscopic-flan-a22bd8.netlify.app/?config=codec_mushra_test.yaml"
echo "=========================================="