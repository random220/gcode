#!/bin/bash


function make_index() {
    cat <<'EOF' >index.info
[/Count 7 /Page 12 /Title (17. WAVE MOTION 1-50) /OUT pdfmark
[/Page 13 /Title (17.1 Introduction) /OUT pdfmark
[/Page 13 /Title (17.2 Classification of a Wave) /OUT pdfmark
[/Page 14 /Title (17.3 Equation of a Travelling Wave) /OUT pdfmark
[/Page 18 /Title (17.4 Sine Wave) /OUT pdfmark
[/Page 22 /Title (17.5 Two Graphs in Sine Wave) /OUT pdfmark
[/Page 28 /Title (17.6 Wave Speed) /OUT pdfmark
[/Page 33 /Title (17.7 Energy in Wave Motion) /OUT pdfmark

[/Count 6 /Page 62 /Title (18. SUPERPOSITION OF WAVES 51-98) /OUT pdfmark
[/Page 63 /Title (18.1 Principle of Superposition) /OUT pdfmark
[/Page 63 /Title (18.2 Resultant Amplitude and Intensity due to Coherent Sources) /OUT pdfmark
[/Page 65 /Title (18.3 Interference) /OUT pdfmark
[/Page 69 /Title (18.4 Standing Wave) /OUT pdfmark
[/Page 74 /Title (18.5 Normal Modes of a String) /OUT pdfmark
[/Page 79 /Title (18.6 Reflection and Transmission of a Wave) /OUT pdfmark

[/Count 9 /Page 110 /Title (19 SOUND WAVES 99-170) /OUT pdfmark
[/Page 111 /Title (19.1 Introduction) /OUT pdfmark
[/Page 111 /Title (19.2 Displacement Wave, Pressure Wave and Density Wave) /OUT pdfmark
[/Page 116 /Title (19.3 Speed of a Longitudinal Wave) /OUT pdfmark
[/Page 117 /Title (19.4 Sound Waves in Gases) /OUT pdfmark
[/Page 120 /Title (19.5 Sound Intensity) /OUT pdfmark
[/Page 123 /Title (19.6 Interference in Sound Wave and Stationary Wave) /OUT pdfmark
[/Page 125 /Title (19.7 Standing Longitudinal Waves in Organ Pipes) /OUT pdfmark
[/Page 130 /Title (19.8 Beats) /OUT pdfmark
[/Page 133 /Title (19.9 The Doppler's Effect) /OUT pdfmark

[/Count 10 /Page 182 /Title (20. THERMOMETRY, THERMAL EXPANSION & KINETIC THEORY OF GASES 171-236) /OUT pdfmark
[/Page 183 /Title (20.1 Thermometers and The Celsius Temperature Scale) /OUT pdfmark
[/Page 183 /Title (20.2 The Constant Volume Gas Thermometer and The Absolute Temperature Scale) /OUT pdfmark
[/Page 187 /Title (20.3 Heat and Temperature) /OUT pdfmark
[/Page 188 /Title (20.4 Thermal Expansion) /OUT pdfmark
[/Page 196 /Title (20.5 Behaviour of Gases) /OUT pdfmark
[/Page 204 /Title (20.6 Degree of Freedom) /OUT pdfmark
[/Page 206 /Title (20.7 Internal Energy of an Ideal Gas) /OUT pdfmark
[/Page 206 /Title (20.8 Law of Equipartition of Energy) /OUT pdfmark
[/Page 209 /Title (20.9 Molar Heat Capacity) /OUT pdfmark
[/Page 212 /Title (20.10 Kinetic Theory of Gases) /OUT pdfmark

[/Count 7 /Page 248 /Title (21. LAWS OF THERMODYNAMICS 237-305) /OUT pdfmark
[/Page 249 /Title (21.1 The First Law of Thermodynamics) /OUT pdfmark
[/Page 251 /Title (21.2 Further Explanation of Three Terms Used in First Law) /OUT pdfmark
[/Page 260 /Title (21.3 Different Thermodynamic Processes) /OUT pdfmark
[/Page 268 /Title (21.4 Heat Engine and its Efficiency) /OUT pdfmark
[/Page 270 /Title (21.5 Refrigerator) /OUT pdfmark
[/Page 275 /Title (21.6 Zeroth Law of Thermodynamics) /OUT pdfmark
[/Page 276 /Title (21.7 Second Law of Thermodynamics) /OUT pdfmark

[/Count 2 /Page 318 /Title (22. CALORIMETRY & HEAT TRANSFER 307-352) /OUT pdfmark
[/Page 319 /Title (22.1 Calorimetry) /OUT pdfmark
[/Page 324 /Title (22.2 Heat Transfer) /OUT pdfmark

[/Page 338 /Title (Solved Examples) /OUT pdfmark
[/Page 345 /Title (Miscellaneous Examples) /OUT pdfmark
[/Page 354 /Title (Exercises) /OUT pdfmark
[/Page 364 /Title (Answers) /OUT pdfmark

[/Page 446 /Title (JEE Main & Advanced Previous Years' Questions (2018-13) 1-19) /OUT pdfmark
EOF

    /usr/bin/gs -sDEVICE=pdfwrite -q -dBATCH -dNOPAUSE -sOutputFile=out.pdf -dPDFSETTINGS=/prepress index.info -f in.pdf
}



function repackit() {
# -----------------------------------------------------------------------------
# How to repack
# -----------------------------------------------------------------------------
    
    cat >a.txt <<'_EOF'
#
# -----------------------------------------------------------------------------
# How to generage bookmarks for this pdf book
# -----------------------------------------------------------------------------
# cat a.sh|gzip - -9|openssl enc - base64 >a.txt
cat <<EOF | openssl enc -d -base64|gunzip - >a.sh
_EOF

    cat $0|gzip -9 -|openssl enc -base64 >>a.txt

    cat >>a.txt <<'_EOF'
EOF
chmod a+x a.sh
# -----------------------------------------------------------------------------
#
_EOF
}

if [[ $1 == idx ]]; then
    make_index
elif [[ $1 == repack ]]; then
    repackit
else
    echo "$0 idx|repack"
fi
  


