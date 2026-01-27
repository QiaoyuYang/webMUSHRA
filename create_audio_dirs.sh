#!/bin/bash
# Run this script to create the audio directory structure

AUDIO_PATH="configs/resources/audio"

mkdir -p $AUDIO_PATH/training
mkdir -p $AUDIO_PATH/trial01
mkdir -p $AUDIO_PATH/trial02
mkdir -p $AUDIO_PATH/trial03
mkdir -p $AUDIO_PATH/trial04
mkdir -p $AUDIO_PATH/trial05
mkdir -p $AUDIO_PATH/trial06
mkdir -p $AUDIO_PATH/trial07
mkdir -p $AUDIO_PATH/trial08
mkdir -p $AUDIO_PATH/trial09
mkdir -p $AUDIO_PATH/trial10
mkdir -p $AUDIO_PATH/trial11
mkdir -p $AUDIO_PATH/trial12

echo '✅ Audio directories created!'
echo ''
echo 'Required files for each directory:'
echo '  - reference.wav'
echo '  - anchor_opus.wav'
echo '  - yourcodec_7.5k.wav'
echo '  - yourcodec_4.5k.wav'
echo '  - dac_7.5k.wav'
echo '  - dac_4.5k.wav'
echo '  - encodec_6.0k.wav'
