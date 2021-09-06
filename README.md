# Pycorder (for lack of a better name)
A simple application for recording sound from an audio interface.

*Status: work-in-progress*

## Goal
The goal of this application is to have an audio recorder with an extremely simple (touch) interface that starts recording as soon as the application 
is launched. The intented use case is to be able to have a recording running as soon as you power up your studio. This way performances are always captured 
and you don't have to worry whether a recorder is running or not.

The recorder will output:
1. a datetime-named .wav recording and, 
2. a text file with timestamps, if the "Mark" button was pressed at least once.

## Workflow
The application should work as follows:
1. Simply boot the machine as start making music. 
2. Press an onscreen button to mark when anything interesting happens.
3. ?
4. Profit!

## Environment
This application was developed with Python and Glade (GTK) and is intended to run on a Debian machine (such as an Ubuntu machine).
