#!/bin/bash

# Коренева директорія проєкту
PROJECT_DIR="./iscra-1"

# Перевірка наявності директорій
mkdir -p $PROJECT_DIR/{agents,config,core,data,edge_tts-master,ffmpeg-8.0,finance,interfaces,logs,ml,storage}

# Переміщення файлів
mv $PROJECT_DIR/agent_*.py $PROJECT_DIR/agents/
mv $PROJECT_DIR/ai_delegate.py $PROJECT_DIR/agents/
mv $PROJECT_DIR/run_once.py $PROJECT_DIR/agents/
mv $PROJECT_DIR/self_upgrade.py $PROJECT_DIR/agents/

mv $PROJECT_DIR/env.txt $PROJECT_DIR/config/
mv $PROJECT_DIR/*.cfg $PROJECT_DIR/config/
mv $PROJECT_DIR/*.ini $PROJECT_DIR/config/
mv $PROJECT_DIR/*.yml $PROJECT_DIR/config/
mv $PROJECT_DIR/LICENSE $PROJECT_DIR/config/
mv $PROJECT_DIR/.gitignore $PROJECT_DIR/config/
mv $PROJECT_DIR/py.typed $PROJECT_DIR/config/

mv $PROJECT_DIR/__main__.py $PROJECT_DIR/core/
mv $PROJECT_DIR/constants.py $PROJECT_DIR/core/
mv $PROJECT_DIR/exceptions.py $PROJECT_DIR/core/
mv $PROJECT_DIR/version.py $PROJECT_DIR/core/
mv $PROJECT_DIR/util.py $PROJECT_DIR/core/
mv $PROJECT_DIR/typing.py $PROJECT_DIR/core/
mv $PROJECT_DIR/memory.py $PROJECT_DIR/core/
mv $PROJECT_DIR/communicate.py $PROJECT_DIR/core/
mv $PROJECT_DIR/drm.py $PROJECT_DIR/core/
mv $PROJECT_DIR/mobile_mode.py $PROJECT_DIR/core/

mv $PROJECT_DIR/*.json $PROJECT_DIR/data/
mv $PROJECT_DIR/*.txt $PROJECT_DIR/data/

mv $PROJECT_DIR/voice_engine*.py $PROJECT_DIR/edge_tts-master/
mv $PROJECT_DIR/voices.py $PROJECT_DIR/edge_tts-master/
mv $PROJECT_DIR/win32_playback.py $PROJECT_DIR/edge_tts-master/
mv $PROJECT_DIR/srt_composer.py $PROJECT_DIR/edge_tts-master/
mv $PROJECT_DIR/submaker.py $PROJECT_DIR/edge_tts-master/

mv $PROJECT_DIR/binance*.py $PROJECT_DIR/finance/
mv $PROJECT_DIR/risk_manager.py $PROJECT_DIR/finance/
mv $PROJECT_DIR/cloud_*.py $PROJECT_DIR/finance/

mv $PROJECT_DIR/telegram*.py $PROJECT_DIR/interfaces/
mv $PROJECT_DIR/server.js $PROJECT_DIR/interfaces/

mv $PROJECT_DIR/log_manager.py $PROJECT_DIR/logs/
mv $PROJECT_DIR/*.mp3 $PROJECT_DIR/logs/

mv $PROJECT_DIR/ml_*.py $PROJECT_DIR/ml/
mv $PROJECT_DIR/*_core.py $PROJECT_DIR/ml/
mv $PROJECT_DIR/data_classes.py $PROJECT_DIR/ml/

mv $PROJECT_DIR/*.sh $PROJECT_DIR/storage/
mv $PROJECT_DIR/*.doc $PROJECT_DIR/storage/

echo "✅ Файли успішно розкидано по папках!"
