@echo off
title Segment and Pose for SHARPER Night 2023
call %USERPROFILE%\Anaconda3\Scripts\activate sharpernight2023
cd %USERPROFILE%\yolo_cli
python main.py
