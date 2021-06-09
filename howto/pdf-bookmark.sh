# reference: https://www.xmodulo.com/add-bookmarks-pdf-document-linux.html


cat <<'EOF' >index.info
[/Count 1 /Page 12 /Title (1. BASIC MATHEMATICS) /OUT pdfmark
[/Page 13 /Title (1.1 Basic Mathematics) /OUT pdfmark

[/Count 5 /Page 24 /Title (2. MEASUREMENT AND ERRORS) /OUT pdfmark
[/Page 25 /Title (2.1 Errors in Measurement and Least Count) /OUT pdfmark
[/Page 25 /Title (2.2 Significant Figures) /OUT pdfmark
[/Page 27 /Title (2.3 Rounding off a Digit) /OUT pdfmark
[/Page 28 /Title (2.4 Algebraic Operations with Significant Figures) /OUT pdfmark
[/Page 30 /Title (2.5 Error Analysis) /OUT pdfmark

[/Count 11 /Page 44 /Title (3. EXPERIMENTS) /OUT pdfmark
[/Page 45 /Title (3.1 Vernier Callipers) /OUT pdfmark
[/Page 49 /Title (3.2 Screw Gauge) /OUT pdfmark
[/Page 52 /Title (3.3 Determination of 'g' using a Simple Pendulum) /OUT pdfmark
[/Page 55 /Title (3.4 Young's Modulus by Searle's Method) /OUT pdfmark
[/Page 60 /Title (3.5 Determination of Specific Heat) /OUT pdfmark
[/Page 63 /Title (3.6 Speed of Sound using Resonance Tube) /OUT pdfmark
[/Page 65 /Title (3.7 Verification of Ohm's Law using Voltmeter and Ammeter) /OUT pdfmark
[/Page 69 /Title (3.8 Meter Bridge Experiment) /OUT pdfmark
[/Page 73 /Title (3.9 Post Office Box) /OUT pdfmark
[/Page 75 /Title (3.10 Focal Length of a Concave Mirror using u-v method) /OUT pdfmark
[/Page 80 /Title (3.11 Focal Length of a Convex Lens using u-v method) /OUT pdfmark

[/Count 4 /Page 90 /Title (4. UNITS AND DIMENSIONS 79-96) /OUT pdfmark
[/Page 91 /Title (4.1 Units) /OUT pdfmark
[/Page 91 /Title (4.2 Fundamental and Derived Units) /OUT pdfmark
[/Page 92 /Title (4.3 Dimensions) /OUT pdfmark
[/Page 96 /Title (4.4 Uses of Dimensions) /OUT pdfmark

[/Count 5 /Page 108 /Title (5. VECTORS 97-125) /OUT pdfmark
[/Page 109 /Title (5.1 Vector and Scalar Quantities) /OUT pdfmark
[/Page 109 /Title (5.2 General Points regarding Vectors) /OUT pdfmark
[/Page 113 /Title (5.3 Addition and Subtraction of Two Vectors) /OUT pdfmark
[/Page 116 /Title (5.4 Components of a Vector) /OUT pdfmark
[/Page 119 /Title (5.5 Product of Two Vectors) /OUT pdfmark

[/Count 10 /Page 138 /Title (6. KINEMATICS 127-214) /OUT pdfmark
[/Page 139 /Title ( 6.1 Introduction to Mechanics and Kinematics) /OUT pdfmark
[/Page 139 /Title ( 6.2 Few General Points of Motion) /OUT pdfmark
[/Page 140 /Title ( 6.3 Classification of Motion) /OUT pdfmark
[/Page 142 /Title ( 6.4 Basic Definition) /OUT pdfmark
[/Page 145 /Title ( 6.5 Uniform Motion) /OUT pdfmark
[/Page 147 /Title ( 6.6 One Dimensional Motion with Uniform Acceleration) /OUT pdfmark
[/Page 152 /Title ( 6.7 One Dimensional Motion with Non-uniform Acceleration) /OUT pdfmark
[/Page 155 /Title ( 6.8 Motion in Two and Three Dimensions) /OUT pdfmark
[/Page 158 /Title ( 6.9 Graphs) /OUT pdfmark
[/Page 168 /Title (6.10 Relative Motion) /OUT pdfmark

[/Count 6 /Page 226 /Title (7. PROJECTILE MOTION 215-259) /OUT pdfmark
[/Page 227 /Title (7.1 Introduction) /OUT pdfmark
[/Page 227 /Title (7.2 Projectile Motion) /OUT pdfmark
[/Page 228 /Title (7.3 Two Methods of Solving a Projectile Motion) /OUT pdfmark
[/Page 232 /Title (7.4 Time of Flight, Maximum Height and Horizontal Range of a Projectile) /OUT pdfmark
[/Page 238 /Title (7.5 Projectile Motion along an Inclined Plane) /OUT pdfmark
[/Page 241 /Title (7.6 Relative Motion between Two Projectiles) /OUT pdfmark

[/Count 7 /Page 272 /Title (8. LAWS OF MOTION 261-359) /OUT pdfmark
[/Page 273 /Title (8.1 Types of Forces) /OUT pdfmark
[/Page 275 /Title (8.2 Free Body Diagram) /OUT pdfmark
[/Page 277 /Title (8.3 Equilibrium) /OUT pdfmark
[/Page 287 /Title (8.4 Newton's Laws of Motion) /OUT pdfmark
[/Page 296 /Title (8.5 Constraint Equations) /OUT pdfmark
[/Page 302 /Title (8.6 Pseudo Force) /OUT pdfmark
[/Page 305 /Title (8.7 Friction) /OUT pdfmark

[/Count 9 /Page 372 /Title (9. WORK, ENERGY AND POWER 361-427) /OUT pdfmark
[/Page 373 /Title (9.1 Introduction to Work) /OUT pdfmark
[/Page 373 /Title (9.2 Work Done) /OUT pdfmark
[/Page 379 /Title (9.3 Conservative and Non-conservative Forces) /OUT pdfmark
[/Page 381 /Title (9.4 Kinetic Energy) /OUT pdfmark
[/Page 382 /Title (9.5 Work-Energy Theorem) /OUT pdfmark
[/Page 386 /Title (9.6 Potential Energy) /OUT pdfmark
[/Page 389 /Title (9.7 Three Types of Equilibrium) /OUT pdfmark
[/Page 393 /Title (9.8 Power of a Force) /OUT pdfmark
[/Page 395 /Title (9.9 Law of Conservation of Mechanical Energy) /OUT pdfmark

[/Count 5 /Page 440 /Title (10. CIRCULAR MOTION 429-476) /OUT pdfmark
[/Page 441 /Title (10.1 Introduction) /OUT pdfmark
[/Page 441 /Title (10.2 Kinematics of Circular Motion) /OUT pdfmark
[/Page 446 /Title (10.3 Dynamics of Circular Motion) /OUT pdfmark
[/Page 454 /Title (10.4 Centrifugal Force) /OUT pdfmark
[/Page 455 /Title (10.5 Motion in a Vertical Circle) /OUT pdfmark

[/Page 488 /Title (Hints & Solutions 477-608) /OUT pdfmark
[/Page 620 /Title (JEE Main & Advanced Previous Years' Questions (2018-13) 1-18) /OUT pdfmark
EOF

/usr/bin/gs -sDEVICE=pdfwrite -q -dBATCH -dNOPAUSE -sOutputFile=out.pdf -dPDFSETTINGS=/prepress index.info -f in.pdf

