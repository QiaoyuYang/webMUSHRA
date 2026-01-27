#!/usr/bin/env python3
"""
Generate webMUSHRA configuration file for audio codec MUSHRA test.
SHORTENED VERSION: 12 trials for ~25-30 minute test duration.

Customize the variables below for your specific test setup.
"""

import yaml

# ============== CUSTOMIZE THESE SETTINGS ==============

TEST_NAME = "Audio Codec Quality Evaluation"
TEST_ID = "codec_mushra_2025"

# Define your trial information (REDUCED: 4 per audio type = 12 total)
# Format: (trial_id, audio_type, description)
TRIALS = [
    # Speech trials (1-4)
    ("trial01", "speech", "Speech - Male speaker"),
    ("trial02", "speech", "Speech - Female speaker"),
    ("trial03", "speech", "Speech - Expressive/emotional"),
    ("trial04", "speech", "Speech - Multiple speakers"),
    
    # Music trials (5-8)
    ("trial05", "music", "Music - Solo instrument"),
    ("trial06", "music", "Music - Vocal with accompaniment"),
    ("trial07", "music", "Music - Full band/orchestra"),
    ("trial08", "music", "Music - Electronic/synthesized"),
    
    # Sound trials (9-12)
    ("trial09", "sound", "Sound - Nature/ambient"),
    ("trial10", "sound", "Sound - Mechanical/urban"),
    ("trial11", "sound", "Sound - Mixed/complex scene"),
    ("trial12", "sound", "Sound - Transients/impacts"),
]

# Define conditions (codecs/bitrates to compare)
# Format: (condition_id, filename_suffix)
# TIP: Fewer conditions = faster test. 5-6 conditions is ideal.
CONDITIONS = [
    ("YourCodec_7.5k", "yourcodec_7.5k"),
    ("YourCodec_4.5k", "yourcodec_4.5k"),
    ("DAC_7.5k", "dac_7.5k"),
    ("DAC_4.5k", "dac_4.5k"),
    ("EnCodec_6.0k", "encodec_6.0k"),
]

AUDIO_FORMAT = "wav"  # or "mp3", "ogg"
AUDIO_BASE_PATH = "configs/resources/audio"

# Estimated test duration (for display to participants)
ESTIMATED_DURATION = "25-30 minutes"

# ============== END OF CUSTOMIZATION ==============


def generate_config():
    config = {
        "testname": TEST_NAME,
        "testId": TEST_ID,
        "bufferSize": 2048,
        "stopOnErrors": True,
        "showButtonPrevious": True,
        "remoteService": None,
        "pages": []
    }
    
    # Introduction page
    config["pages"].append({
        "type": "generic",
        "id": "introduction",
        "name": "Welcome",
        "content": f"""<h2>Audio Codec Listening Test</h2>
<p>Thank you for participating in this study evaluating audio codec quality.</p>

<h3>Instructions:</h3>
<ul>
  <li>Please use <strong>high-quality headphones</strong> in a quiet environment</li>
  <li>You will hear multiple versions of the same audio clip</li>
  <li>Rate each version from 0 (Bad) to 100 (Excellent) compared to the Reference</li>
  <li>The Reference represents the best possible quality</li>
  <li>You can replay and switch between samples as many times as needed</li>
</ul>

<h3>Rating Scale:</h3>
<ul>
  <li><strong>80-100:</strong> Excellent - Imperceptible difference from reference</li>
  <li><strong>60-80:</strong> Good - Perceptible but not annoying</li>
  <li><strong>40-60:</strong> Fair - Slightly annoying</li>
  <li><strong>20-40:</strong> Poor - Annoying</li>
  <li><strong>0-20:</strong> Bad - Very annoying</li>
</ul>

<p>The test contains <strong>{len(TRIALS)} trials</strong> and takes approximately <strong>{ESTIMATED_DURATION}</strong>.</p>"""
    })
    
    # Headphone check page
    config["pages"].append({
        "type": "generic",
        "id": "headphone_check",
        "name": "Equipment Check",
        "content": """<h2>Before You Begin</h2>
<p>Please confirm the following:</p>
<ul>
  <li>☑️ I am wearing <strong>headphones</strong> (not using speakers)</li>
  <li>☑️ I am in a <strong>quiet environment</strong></li>
  <li>☑️ I have adjusted my <strong>volume to a comfortable level</strong></li>
  <li>☑️ I will not adjust the volume during the test</li>
</ul>
<p>Click <strong>Next</strong> to proceed to a training trial.</p>"""
    })
    
    # Training trial
    config["pages"].append({
        "type": "mushra",
        "id": "training",
        "name": "Training Trial (Practice)",
        "content": "This is a <strong>practice trial</strong> to familiarize yourself with the interface. Your ratings will NOT be recorded. Try clicking on different samples and adjusting the sliders.",
        "showWaveform": True,
        "enableLooping": True,
        "reference": f"{AUDIO_BASE_PATH}/training/reference.{AUDIO_FORMAT}",
        "createAnchor35": False,
        "createAnchor70": False,
        "stimuli": {
            "anchor": f"{AUDIO_BASE_PATH}/training/anchor_opus.{AUDIO_FORMAT}",
            **{cond_id: f"{AUDIO_BASE_PATH}/training/{filename}.{AUDIO_FORMAT}" 
               for cond_id, filename in CONDITIONS[:2]}  # Just 2 conditions for training
        }
    })
    
    # Main test trials
    for i, (trial_id, audio_type, description) in enumerate(TRIALS, 1):
        stimuli = {
            "anchor": f"{AUDIO_BASE_PATH}/{trial_id}/anchor_opus.{AUDIO_FORMAT}"
        }
        for cond_id, filename in CONDITIONS:
            stimuli[cond_id] = f"{AUDIO_BASE_PATH}/{trial_id}/{filename}.{AUDIO_FORMAT}"
        
        config["pages"].append({
            "type": "mushra",
            "id": trial_id,
            "name": f"Trial {i} of {len(TRIALS)}",
            "content": f"<strong>{description}</strong><br>Rate the audio quality of each sample compared to the Reference.",
            "showWaveform": True,
            "enableLooping": True,
            "reference": f"{AUDIO_BASE_PATH}/{trial_id}/reference.{AUDIO_FORMAT}",
            "createAnchor35": False,
            "createAnchor70": False,
            "stimuli": stimuli
        })
    
    # Finish page
    config["pages"].append({
        "type": "finish",
        "id": "finish",
        "name": "Test Complete",
        "content": """<h2>Thank You!</h2>
<p>You have completed all trials.</p>
<p><strong>⚠️ Important:</strong> Please click the <strong>"Send Results"</strong> button below to submit your responses.</p>
<p>If the button doesn't work, please download your results and email them to the researcher.</p>
<p>Thank you for your valuable contribution to this research!</p>""",
        "showResults": True,
        "writeResults": True
    })
    
    return config


def main():
    config = generate_config()
    
    # Write YAML config
    output_file = "codec_mushra_test.yaml"
    with open(output_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ Generated: {output_file}")
    print(f"   - {len(TRIALS)} trials")
    print(f"   - {len(CONDITIONS)} conditions per trial (+ reference + anchor)")
    print(f"   - Estimated duration: {ESTIMATED_DURATION}")
    
    # Generate directory structure script
    with open("create_audio_dirs.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# Run this script to create the audio directory structure\n\n")
        f.write(f"AUDIO_PATH=\"{AUDIO_BASE_PATH}\"\n\n")
        f.write("mkdir -p $AUDIO_PATH/training\n")
        for trial_id, _, _ in TRIALS:
            f.write(f"mkdir -p $AUDIO_PATH/{trial_id}\n")
        f.write("\necho '✅ Audio directories created!'\n")
        f.write("echo ''\n")
        f.write("echo 'Required files for each directory:'\n")
        f.write("echo '  - reference.wav'\n")
        f.write("echo '  - anchor_opus.wav'\n")
        for _, filename in CONDITIONS:
            f.write(f"echo '  - {filename}.wav'\n")
    
    print("✅ Generated: create_audio_dirs.sh")
    
    # Generate file checklist
    with open("audio_file_checklist.txt", "w") as f:
        f.write("Audio File Checklist for MUSHRA Test (Short Version)\n")
        f.write("=" * 55 + "\n")
        f.write(f"Total trials: {len(TRIALS)}\n")
        f.write(f"Estimated duration: {ESTIMATED_DURATION}\n")
        f.write("=" * 55 + "\n\n")
        
        all_dirs = [("training", "practice", "Training")] + [(t[0], t[1], t[2]) for t in TRIALS]
        for dir_name, audio_type, desc in all_dirs:
            f.write(f"\n{AUDIO_BASE_PATH}/{dir_name}/  [{audio_type}]\n")
            f.write(f"  Description: {desc}\n")
            f.write(f"  [ ] reference.{AUDIO_FORMAT}\n")
            f.write(f"  [ ] anchor_opus.{AUDIO_FORMAT}\n")
            for _, filename in CONDITIONS:
                f.write(f"  [ ] {filename}.{AUDIO_FORMAT}\n")
    
    print("✅ Generated: audio_file_checklist.txt")
    
    # Summary table
    print("\n" + "=" * 50)
    print("TRIAL SUMMARY")
    print("=" * 50)
    print(f"{'Trial':<10} {'Type':<10} {'Description':<30}")
    print("-" * 50)
    for trial_id, audio_type, desc in TRIALS:
        print(f"{trial_id:<10} {audio_type:<10} {desc:<30}")
    print("=" * 50)


if __name__ == "__main__":
    main()