#!/bin/bash

DIR_NAME="Samples"
LIB_REPOSITORY="http://www.stud.fit.vutbr.cz/~xmlyna06/POV"
SAMPLES=( "game_00" "game_01" "game_02" "game_03" "game_04" "game_05")

mkdir -p $DIR_NAME
cd $DIR_NAME

for game in "${SAMPLES[@]}"
do
    wget -N $LIB_REPOSITORY/$game.json
    wget -N $LIB_REPOSITORY/$game.txt
    wget -N $LIB_REPOSITORY/$game.mp4
done
cd ..