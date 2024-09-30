#!/bin/bash

# Cleanup and setup
VID_DIR="$HOME/.vid"
rm -rf "$VID_DIR"
mkdir -p "$VID_DIR"

# Generate initial list of files with numbered entries
n=0
ls -1a | grep -vE '^\.$|^\.\.$' | while IFS= read -r line; do
    n=$(( n + 1 ))
    printf "%d\t%s\n" "$n" "$line"
done > "$VID_DIR/f1"

# Create a copy for editing
cp -f "$VID_DIR/f1" "$VID_DIR/f2"
vi "$VID_DIR/f2"

mycomm() {
    local f g
    case "$1" in
        -23) f="$2"; g="$3" ;;
        -13) f="$3"; g="$2" ;;
    esac
    grep -vxFf "$f" "$g"
}

# Prepare lists for identifying deletions and renaming
cut -f1 < "$VID_DIR/f1" | sort > "$VID_DIR/n1"
cut -f1 < "$VID_DIR/f2" | sort > "$VID_DIR/n2"
mycomm -23 "$VID_DIR/n1" "$VID_DIR/n2" > "$VID_DIR/del"

sort "$VID_DIR/f1" > "$VID_DIR/g1"
sort "$VID_DIR/f2" > "$VID_DIR/g2"
mycomm -13 "$VID_DIR/g1" "$VID_DIR/g2" | cut -f1 > "$VID_DIR/ren"

# Generate the script for deletions and renaming
{
    tab=$(printf '\t')
    while IFS= read -r linenum; do
        f=$(grep "^$linenum$tab" "$VID_DIR/f1" | cut -f2-)
        printf "rm -rf %q\n" "$f"
    done < "$VID_DIR/del"

    while IFS= read -r linenum; do
        f=$(grep "^$linenum$tab" "$VID_DIR/f1" | cut -f2-)
        g=$(grep "^$linenum$tab" "$VID_DIR/f2" | cut -f2-)

        d=$(dirname "$g")
        [[ "$d" != '.' ]] && printf "mkdir -p %q\n" "$d"
        [[ -z "$g" ]] && printf "rm -rf %q\n" "$f" || printf "mv %q %q\n" "$f" "$g"
    done < "$VID_DIR/ren"
} > "$VID_DIR/do0"

grep '^mkdir' <"$VID_DIR/do0" | sort -u >"$VID_DIR/do"
grep -v '^mkdir' <"$VID_DIR/do0" >>"$VID_DIR/do"

# Display and suggest executing the generated script
echo '---------------------------------------------'
cat "$VID_DIR/do"
echo '---------------------------------------------'
echo
echo "bash $VID_DIR/do"
