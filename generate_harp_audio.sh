#!/bin/bash
#
# Generate directory structure and placeholder audio for HARP MUSHRA tests
# Based on paper: 12 items (4 music, 4 speech, 4 general audio)
# Two bitrate conditions: 4.3 kbps and 7.7 kbps
# Conditions: reference, anchor (3.5kHz LP), HARP, DAC, BSCodec
#

set -e

AUDIO_DIR="configs/resources/audio"
DURATION=10  # 10 seconds as per paper
SAMPLE_RATE=44100  # 44.1 kHz as per paper

# Trial directories matching paper's stimuli selection
TRIALS=(
    "training"
    "trial01_music_classical"      # Music - Classical (Orchestra)
    "trial02_music_jazz"           # Music - Jazz (Vocal Trio)
    "trial03_music_pop"            # Music - Pop (Vocal-heavy)
    "trial04_music_electronic"     # Music - Electronic (EDM)
    "trial05_speech_male1"         # Speech - Male Speaker 1
    "trial06_speech_male2"         # Speech - Male Speaker 2
    "trial07_speech_female1"       # Speech - Female Speaker 1
    "trial08_speech_female2"       # Speech - Female Speaker 2
    "trial09_audio_environmental"  # General Audio - Environmental (Rain with Thunder)
    "trial10_audio_mechanical"     # General Audio - Mechanical (Engine Sounds)
    "trial11_audio_animal"         # General Audio - Animal (Birdsong)
    "trial12_audio_mixed"          # General Audio - Mixed (Crowd Ambience with Music)
)

# Conditions for each bitrate
# Reference and anchor are same for both tests
# Codec outputs differ by bitrate
CONDITIONS_COMMON=(
    "reference:440"           # Original (440 Hz tone as placeholder)
    "anchor_3.5khz_lp:220"    # 3.5 kHz lowpass anchor (220 Hz - sounds "muffled")
)

CONDITIONS_4_3KBPS=(
    "harp_4.3kbps:350"
    "dac_4.3kbps:300"
    "bscodec_4.3kbps:280"
)

CONDITIONS_7_7KBPS=(
    "harp_7.7kbps:400"
    "dac_7.7kbps:380"
    "bscodec_7.7kbps:360"
)

echo "=========================================="
echo "HARP MUSHRA Test - Audio Directory Setup"
echo "=========================================="
echo ""
echo "Paper specs:"
echo "  - 12 trials (4 music, 4 speech, 4 general audio)"
echo "  - 10 seconds per clip"
echo "  - 44.1 kHz sample rate"
echo "  - Two bitrate conditions: 4.3 kbps and 7.7 kbps"
echo "  - Conditions: Reference, Anchor (3.5kHz LP), HARP, DAC, BSCodec"
echo ""

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: ffmpeg not found. Please install ffmpeg."
    exit 1
fi

# Create directories and audio files
for trial in "${TRIALS[@]}"; do
    echo "📁 Creating: $AUDIO_DIR/$trial/"
    mkdir -p "$AUDIO_DIR/$trial"
    
    # Add trial-specific frequency offset for variety
    trial_num=${trial#trial}
    trial_num=${trial_num%%_*}
    # Use 10# to force base-10 interpretation (fixes octal issue with 08, 09)
    if [[ "$trial_num" =~ ^[0-9]+$ ]]; then
        freq_offset=$((10#$trial_num * 5))
    else
        freq_offset=0
    fi
    
    # Common conditions (reference and anchor)
    for cond in "${CONDITIONS_COMMON[@]}"; do
        name="${cond%%:*}"
        base_freq="${cond##*:}"
        freq=$((base_freq + freq_offset))
        
        ffmpeg -f lavfi -i "sine=frequency=${freq}:duration=${DURATION}" \
               -acodec pcm_s16le -ar $SAMPLE_RATE -ac 1 \
               -loglevel error \
               "$AUDIO_DIR/$trial/${name}.wav" -y
        echo "   ✓ ${name}.wav (${freq}Hz)"
    done
    
    # 4.3 kbps conditions
    for cond in "${CONDITIONS_4_3KBPS[@]}"; do
        name="${cond%%:*}"
        base_freq="${cond##*:}"
        freq=$((base_freq + freq_offset))
        
        ffmpeg -f lavfi -i "sine=frequency=${freq}:duration=${DURATION}" \
               -acodec pcm_s16le -ar $SAMPLE_RATE -ac 1 \
               -loglevel error \
               "$AUDIO_DIR/$trial/${name}.wav" -y
        echo "   ✓ ${name}.wav (${freq}Hz)"
    done
    
    # 7.7 kbps conditions
    for cond in "${CONDITIONS_7_7KBPS[@]}"; do
        name="${cond%%:*}"
        base_freq="${cond##*:}"
        freq=$((base_freq + freq_offset))
        
        ffmpeg -f lavfi -i "sine=frequency=${freq}:duration=${DURATION}" \
               -acodec pcm_s16le -ar $SAMPLE_RATE -ac 1 \
               -loglevel error \
               "$AUDIO_DIR/$trial/${name}.wav" -y
        echo "   ✓ ${name}.wav (${freq}Hz)"
    done
    
    echo ""
done

echo "=========================================="
echo "✅ Done! Created ${#TRIALS[@]} trial directories"
echo ""
echo "Directory structure:"
echo "$AUDIO_DIR/"
for trial in "${TRIALS[@]}"; do
    echo "├── $trial/"
    echo "│   ├── reference.wav"
    echo "│   ├── anchor_3.5khz_lp.wav"
    echo "│   ├── harp_4.3kbps.wav"
    echo "│   ├── harp_7.7kbps.wav"
    echo "│   ├── dac_4.3kbps.wav"
    echo "│   ├── dac_7.7kbps.wav"
    echo "│   ├── bscodec_4.3kbps.wav"
    echo "│   └── bscodec_7.7kbps.wav"
done
echo ""
echo "=========================================="
echo "AUDIO FILE CHECKLIST"
echo "=========================================="
echo ""
echo "Replace placeholder files with actual audio:"
echo ""
echo "For each trial directory, you need:"
echo "  1. reference.wav         - Original uncompressed audio (44.1kHz, 10s)"
echo "  2. anchor_3.5khz_lp.wav  - Reference lowpass filtered at 3.5 kHz"
echo "  3. harp_4.3kbps.wav      - HARP codec output (stages 1-5)"
echo "  4. harp_7.7kbps.wav      - HARP codec output (all stages)"
echo "  5. dac_4.3kbps.wav       - DAC baseline (stages 1-5)"
echo "  6. dac_7.7kbps.wav       - DAC baseline (all stages)"
echo "  7. bscodec_4.3kbps.wav   - BSCodec baseline (reduced codebooks)"
echo "  8. bscodec_7.7kbps.wav   - BSCodec baseline (full codebooks)"
echo ""
echo "To create the 3.5 kHz lowpass anchor:"
echo "  ffmpeg -i reference.wav -af 'lowpass=f=3500' anchor_3.5khz_lp.wav"
echo ""
echo "=========================================="
echo "Next steps:"
echo "1. Replace placeholder audio with real files"
echo "2. Copy config files to configs/ directory:"
echo "   cp mushra_test_a.yaml configs/"
echo "   cp mushra_test_b.yaml configs/"
echo "3. git add configs/"
echo "4. git commit -m 'Add HARP MUSHRA test configs and audio'"
echo "5. git push origin master"
echo ""
echo "Test URLs:"
echo "  Test A (4.3 kbps): ?config=mushra_test_a.yaml"
echo "  Test B (7.7 kbps): ?config=mushra_test_b.yaml"
echo "=========================================="