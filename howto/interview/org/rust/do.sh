#!/bin/bash

cat <<EOF
# Install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# With Cargo
# -----------
# Create project
cargo new my_project
cd my_project/src
# cp main.rs here

cargo run

# Without cargo
# -------------
rustc main.rs -o my_program
./my_program

EOF
