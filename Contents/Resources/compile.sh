#! /bin/sh
find . -name "*.xib" -type f | awk '{sub(/.xib/,"");print}' | xargs -I % ibtool --compile %.nib %.xib
