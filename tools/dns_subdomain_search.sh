#!/bin/bash
rawdomain="$1"
sublist3r -d $rawdomain -o tools/temp2
sed -i s/\<BR\>/\\n/g tools/temp2
cat tools/temp2 | sort -u > tools/temp
rm tools/temp2

