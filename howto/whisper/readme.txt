brew install cmake
brew install ffmpeg

mkdir -p ~/sb
cd ~/sb
git clone https://github.com/ggml-org/whisper.cpp.git
cd whisper.cpp

# download models

cat <<EOF >dload
bash ./models/download-coreml-model.sh base.en
bash ./models/download-coreml-model.sh medium.en
bash ./models/download-coreml-model.sh large-v1
bash ./models/download-coreml-model.sh large-v2
bash ./models/download-coreml-model.sh large-v3
bash ./models/download-coreml-model.sh large-v3-turbo
EOF

bash dload

# build the project
cmake -B build
cmake --build build -j --config Release

# transcribe a sample audio file
./build/bin/whisper-cli -f samples/jfk.wav


mkdir -p ~/bin
cat <<"EOF" >~/bin/whisp
#!/bin/bash
ffmpeg -i "$1" -ar 16000 -ac 1 -c:a pcm_s16le ./_a.wav
~/sb/whisper.cpp/build/bin/whisper-cli -m ~/sb/whisper.cpp/models/ggml-large-v1.bin -f ./_a.wav
rm -f ./_a.wav
EOF
chmod a+x ~/bin/whisp
