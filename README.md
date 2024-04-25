# Cathedral

## Introduction
This project started from the Eddie Van Halen song "Cathedral". It features a delayed guitar track and my objective is to retrieve the delay settings using scientific computing.
If you take a signal and apply delay, the resulting signal will be correlated with the original one. Since there are repeating parts one could argue that the result is correlated with itseld. From a simple research it seems that auto-correlation is a good tool to solve this problem, however my first implementation wasn't yielding the expected results. From my understanding it was because auto-correlation is unstable when applied to non-zero mean signals.


## Goals
This projects aims at interactively explore the application fo auto-correlation to solve "inverse delay" problems and in particular:
  * generate random signals and apply different delay settings
  * see in real-time the effect of such changes to the auto-correlation

As a learning experience I will be using:
  * [smooth-gui](https://github.com/FattiMei/smooth-gui)
  * ImGui
  * OpenCL to accelerate on GPU the computation for real-time requirements
