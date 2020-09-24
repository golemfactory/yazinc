#!/bin/bash

idir=/golem/input
odir=/golem/output
circuit="$idir"/circuit.znb
key="$idir"/proving-key
public="$idir"/public-data.json
witness="$idir"/witness.json
output="$odir"/proof.txt


ZVM='/golem/zvm'

"$ZVM" prove --circuit="$circuit" --proving-key="$key" --public-data="$public" --witness="$witness" > "$output"
