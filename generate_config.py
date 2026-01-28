#!/usr/bin/env python3
"""
Generate MUSHRA test configuration files for audio codec evaluation.

Based on ITU-R BS.1534 (MUSHRA) standard.
Generates configs for webMUSHRA: https://github.com/audiolabs/webMUSHRA

Usage:
    python generate_mushra_config.py
    
Output:
    - mushra_test_a.yaml (low bitrate test)
    - mushra_test_b.yaml (high bitrate test)
"""

import yaml
from dataclasses import dataclass
from typing import List, Dict


# =============================================================================
# CONFIGURATION - Edit these settings for your experiment
# =============================================================================

@dataclass
class BitrateCondition:
    """Defines a bitrate condition for testing."""
    name: str           # e.g., "Test A"
    suffix: str         # e.g., "4.3kbps" (used in filenames)
    test_id: str        # e.g., "mushra_test_a"


@dataclass 
class Codec:
    """Defines a codec/method to evaluate."""
    name: str           # Display name in results (e.g., "HARP")
    file_prefix: str    # Filename prefix (e.g., "harp")


@dataclass
class Trial:
    """Defines a single trial/audio item."""
    id: str             # e.g., "trial01"
    directory: str      # e.g., "trial01_music_classical"
    category: str       # e.g., "Music"
    description: str    # e.g., "Classical (Orchestra)"


# -----------------------------------------------------------------------------
# EXPERIMENT SETTINGS - Modify these for your study
# -----------------------------------------------------------------------------

# Test metadata
EXPERIMENT_NAME = "Audio Codec Evaluation"
AUDIO_BASE_PATH = "configs/resources/audio"

# Bitrate conditions (creates separate test files for each)
BITRATE_CONDITIONS = [
    BitrateCondition(
        name="Test A",
        suffix="4.3kbps",
        test_id="mushra_test_a"
    ),
    BitrateCondition(
        name="Test B",
        suffix="7.7kbps",
        test_id="mushra_test_b"
    ),
]

# Codecs/methods to evaluate (order will be randomized in test)
CODECS = [
    Codec(name="HARP", file_prefix="harp"),
    Codec(name="DAC", file_prefix="dac"),
    Codec(name="BSCodec", file_prefix="bscodec"),
]

# Reference and anchor settings
REFERENCE_FILENAME = "reference.wav"
ANCHOR_FILENAME = "anchor_3.5khz_lp.wav"
HIDDEN_REF_LABEL = "hidden_ref"
ANCHOR_LABEL = "anchor"

# Trial definitions (12 items as per paper)
TRIALS = [
    # Music (4 items) - from MUSDB18-HQ
    Trial("trial01", "trial01_music_classical", "Music", "Classical (Orchestra)"),
    Trial("trial02", "trial02_music_jazz", "Music", "Jazz (Vocal Trio)"),
    Trial("trial03", "trial03_music_pop", "Music", "Pop (Vocal-heavy)"),
    Trial("trial04", "trial04_music_electronic", "Music", "Electronic (EDM)"),
    
    # Speech (4 items) - from LibriTTS
    Trial("trial05", "trial05_speech_male1", "Speech", "Male Speaker 1"),
    Trial("trial06", "trial06_speech_male2", "Speech", "Male Speaker 2"),
    Trial("trial07", "trial07_speech_female1", "Speech", "Female Speaker 1"),
    Trial("trial08", "trial08_speech_female2", "Speech", "Female Speaker 2"),
    
    # General Audio (4 items) - from AudioSet
    Trial("trial09", "trial09_audio_environmental", "General Audio", "Environmental (Rain/Thunder)"),
    Trial("trial10", "trial10_audio_mechanical", "General Audio", "Mechanical (Engine)"),
    Trial("trial11", "trial11_audio_animal", "General Audio", "Animal (Birdsong)"),
    Trial("trial12", "trial12_audio_mixed", "General Audio", "Mixed (Crowd/Music)"),
]

# Training trial (practice, not scored)
TRAINING_TRIAL = Trial("training", "training", "Practice", "Training Item")

# UI Settings
SHOW_WAVEFORM = True
ENABLE_LOOPING = True
BUFFER_SIZE = 2048


# =============================================================================
# CONFIG GENERATION - Usually no need to modify below
# =============================================================================

def get_audio_path(trial_dir: str, filename: str) -> str:
    """Generate full audio file path."""
    return f"{AUDIO_BASE_PATH}/{trial_dir}/{filename}"


def get_codec_filename(codec: Codec, bitrate: BitrateCondition) -> str:
    """Generate codec audio filename."""
    return f"{codec.file_prefix}_{bitrate.suffix}.wav"


def generate_stimuli(trial: Trial, bitrate: BitrateCondition) -> Dict[str, str]:
    """Generate stimuli dictionary for a trial."""
    stimuli = {}
    
    # Hidden reference (same as reference, for quality control)
    stimuli[HIDDEN_REF_LABEL] = get_audio_path(trial.directory, REFERENCE_FILENAME)
    
    # Low anchor (3.5 kHz lowpass)
    stimuli[ANCHOR_LABEL] = get_audio_path(trial.directory, ANCHOR_FILENAME)
    
    # Test codecs
    for codec in CODECS:
        filename = get_codec_filename(codec, bitrate)
        stimuli[codec.name] = get_audio_path(trial.directory, filename)
    
    return stimuli


def generate_config(bitrate: BitrateCondition) -> Dict:
    """Generate complete MUSHRA config for a bitrate condition."""
    
    num_trials = len(TRIALS)
    
    pages = []
    
    # === INTRODUCTION ===
    pages.append({
        "type": "generic",
        "id": "introduction",
        "name": "Welcome",
        "content": f"""<h2>Audio Codec Listening Test - {bitrate.name}</h2>
<p>Thank you for participating in this study evaluating audio codec quality.</p>
<h3>Instructions:</h3>
<ul>
<li>Please use <strong>high-quality headphones</strong> in a quiet environment</li>
<li>You will hear multiple versions of the same audio clip</li>
<li>Rate each version from 0 (Bad) to 100 (Excellent) compared to the Reference</li>
<li>The Reference represents the original, uncompressed audio</li>
<li>You can replay and switch between samples as many times as needed</li>
<li>There is no time limit</li>
</ul>
<h3>Rating Scale:</h3>
<ul>
<li><strong>80-100:</strong> Excellent - Imperceptible difference from reference</li>
<li><strong>60-80:</strong> Good - Perceptible but not annoying</li>
<li><strong>40-60:</strong> Fair - Slightly annoying</li>
<li><strong>20-40:</strong> Poor - Annoying</li>
<li><strong>0-20:</strong> Bad - Very annoying</li>
</ul>
<p>The test contains <strong>{num_trials} trials</strong> and takes approximately <strong>20-25 minutes</strong>.</p>"""
    })
    
    # === EQUIPMENT CHECK ===
    pages.append({
        "type": "generic",
        "id": "headphone_check",
        "name": "Equipment Check",
        "content": """<h2>Before You Begin</h2>
<p>Please confirm the following:</p>
<ul>
<li>I am wearing <strong>high-quality headphones</strong> (not earbuds or speakers)</li>
<li>I am in a <strong>quiet environment</strong></li>
<li>I have adjusted my <strong>volume to a comfortable level</strong></li>
<li>I will <strong>not adjust the volume</strong> during the test</li>
</ul>
<p>Click <strong>Next</strong> to proceed to a training trial.</p>"""
    })
    
    # === TRAINING TRIAL ===
    pages.append({
        "type": "mushra",
        "id": "training",
        "name": "Training Trial (Practice)",
        "content": """This is a <strong>practice trial</strong> to familiarize yourself with the interface. Your ratings will NOT be recorded. Try clicking on different samples and adjusting the sliders. The "Reference" button always plays the original uncompressed audio.""",
        "showWaveform": SHOW_WAVEFORM,
        "enableLooping": ENABLE_LOOPING,
        "reference": get_audio_path(TRAINING_TRIAL.directory, REFERENCE_FILENAME),
        "createAnchor35": False,
        "createAnchor70": False,
        "stimuli": generate_stimuli(TRAINING_TRIAL, bitrate)
    })
    
    # === TEST TRIALS ===
    for i, trial in enumerate(TRIALS, start=1):
        pages.append({
            "type": "mushra",
            "id": trial.id,
            "name": f"Trial {i} of {num_trials}",
            "content": "Rate the audio quality of each sample compared to the Reference.",
            "showWaveform": SHOW_WAVEFORM,
            "enableLooping": ENABLE_LOOPING,
            "reference": get_audio_path(trial.directory, REFERENCE_FILENAME),
            "createAnchor35": False,
            "createAnchor70": False,
            "stimuli": generate_stimuli(trial, bitrate)
        })
    
    # === FINISH PAGE ===
    pages.append({
        "type": "finish",
        "id": "finish",
        "name": "Thank You",
        "content": f"""<h2>{bitrate.name} Complete</h2>
<p>Thank you for completing the listening test!</p>
<p><strong>Important:</strong> Please click the <strong>Send Results</strong> button below to submit your responses.</p>
<p>If the button does not work, please download your results and email them to the researcher.</p>""",
        "showResults": True,
        "writeResults": True
    })
    
    # Complete config
    config = {
        "testname": f"{EXPERIMENT_NAME} - {bitrate.name}",
        "testId": bitrate.test_id,
        "bufferSize": BUFFER_SIZE,
        "stopOnErrors": True,
        "showButtonPrevious": True,
        "remoteService": None,
        "pages": pages
    }
    
    return config


def save_config(config: Dict, filename: str):
    """Save config to YAML file."""
    with open(filename, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  ✓ {filename}")


def main():
    """Generate all MUSHRA config files."""
    
    print()
    print("=" * 60)
    print("MUSHRA Config Generator")
    print("=" * 60)
    print()
    print(f"  Experiment:  {EXPERIMENT_NAME}")
    print(f"  Trials:      {len(TRIALS)}")
    print(f"  Codecs:      {', '.join(c.name for c in CODECS)}")
    print(f"  Conditions:  {len(BITRATE_CONDITIONS)}")
    print()
    
    # Generate config for each bitrate condition
    print("Generating configs:")
    test_files = []
    for bitrate in BITRATE_CONDITIONS:
        filename = f"{bitrate.test_id}.yaml"
        config = generate_config(bitrate)
        save_config(config, filename)
        test_files.append((filename, bitrate))
    
    print()
    print("=" * 60)
    print("STIMULI PER TRIAL")
    print("=" * 60)
    print()
    print("  Each trial contains 5 randomized conditions:")
    print(f"    1. {HIDDEN_REF_LABEL}: Hidden reference (quality control)")
    print(f"    2. {ANCHOR_LABEL}: Low anchor (3.5 kHz lowpass)")
    for i, codec in enumerate(CODECS, start=3):
        print(f"    {i}. {codec.name}: {codec.file_prefix}_<bitrate>.wav")
    
    print()
    print("=" * 60)
    print("AUDIO FILE REQUIREMENTS")
    print("=" * 60)
    print()
    print(f"  Base path: {AUDIO_BASE_PATH}/")
    print()
    print("  For each trial directory, you need:")
    print(f"    - {REFERENCE_FILENAME}")
    print(f"    - {ANCHOR_FILENAME}")
    for bitrate in BITRATE_CONDITIONS:
        for codec in CODECS:
            print(f"    - {get_codec_filename(codec, bitrate)}")
    
    print()
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("  1. Copy configs to webMUSHRA:")
    for filename, _ in test_files:
        print(f"       cp {filename} /data/webMUSHRA/configs/")
    print()
    print("  2. Generate placeholder audio (if needed):")
    print("       ./generate_harp_audio.sh")
    print()
    print("  3. Replace with real audio files")
    print()
    print("  4. Deploy:")
    print("       cd /data/webMUSHRA")
    print("       git add configs/")
    print("       git commit -m 'Update MUSHRA configs'")
    print("       git push origin master")
    print()
    print("  Test URLs:")
    for filename, bitrate in test_files:
        print(f"    {bitrate.name}: ?config={filename}")
    print()


if __name__ == "__main__":
    main()