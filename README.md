# Cathedral

## Introduction
This project started from the Eddie Van Halen song "Cathedral". It features a delayed guitar track and my objective is to retrieve the delay settings using scientific computing.

If you take a signal and apply a delay, the resulting signal will be correlated with the original one because there are repeating parts. If you compute the correlation between the delayed track and a translated version (operation known as autocorrelation) the result will hopefully peak when the time translation is equal to the delay.

My first implementation was numerically unstable, most probably because I was computing the autocorrelation of non-zero mean signals. This project is composed in two parts

## Part 1 - Interactivity
Develop a simple python application to interactively:
  * generate random signals and apply different delay settings
  * see in real-time the effect of such changes to the autocorrelation


![plot](./img/screenshot_demo_random.png)

## Part 2 - Full demo
  * compute the auto correlation for the "Cathedral" track to solve the "inverse delay" problem
  * estimate with minimal effort the program time
  * explore different parallelization techniques (openmp, gpu offloading)

This problem is massively parallel but quadratic in the number of samples, we need all the help we can from the hardware.
