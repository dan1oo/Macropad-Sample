# Macropad-Sample

# Overview

This is a sample Circuitpython program that I worked on in high school to setup a 12 button module with a digital encoder and LCD screen. This program is based off a very standard adafruit macropad setup using circuitpy.

# File Organization

All files and libraries are loaded directly onto the macropad. There is one main code.py program that is automatically ran by the macropad hardware. The program runs different 'macros', which are essentially different layouts that can be cycled through with the digital encoder. danloo.py is an example of a macro file, which would be stored in the macros folder within the macropad drive.

# Program Structure

There are 3 main components to the main.py program. The first component is the 'App' class, which stores and reads the 'macros' files as objects. The second component is the displayio library display setup, which stores each display component in an array. Lastly is the main loop, which continously loops and detects when keys are pressed and activates the corresponding commands, and detects whether the digital encoder is used to cycle to another macro layout.

