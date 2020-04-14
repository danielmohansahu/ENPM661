#!/bin/bash
docker run -ti --rm \
       -e DISPLAY=$DISPLAY \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v /home/danielmohansahu/Homework/ENPM661/Project4/code/catkin_ws:/catkin_ws \
       --net dockernet --ip 172.18.1.10 --hostname developer\
       enpm661_project4:latest byobu
