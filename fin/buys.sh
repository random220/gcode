#!/bin/bash
grep '^Run' input.csv >bought.csv
grep BOUGHT input.csv >>bought.csv
grep '^Run' input.csv >sold.csv
grep SOLD input.csv >>sold.csv
