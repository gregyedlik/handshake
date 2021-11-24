# Bosch handshakes on the CAN bus
This project is about understanding the challenge-response process used in Bosch e-bike systems, with the aim of producing compatible BMS boards. A compatible BMS would allow people to build custom batteries compatible with Bosch bikes, as well as to repair batteries with damaged BMS. 

# Status
I verified that:
* The 'challenge' consists of the messages with arbitration IDs 0x72 and 0x73, sent from the bicycle
* The 'answer' consists of the messages 0x80 and 0x81, sent from the battery
* Comparing two different batteries working with the same bicycle:
    * The challenges are the same towards both batteries
    * The answers are different between the two batteries
    * But a given battery will always give the same answers to the same challenge
* It is not clear why does both the challenge and the answer consist of 2 bytes
    * The content of 0x72 seems to predict the content of 0x73
    * The content of 0x80 seems to predict the content of 0x81

I recorded a lot of handshakes, but I got stuck trying to learn how to generate an acceptable answer for the challenge. I would appreciate help from someone with more computer science background.

I also learned that the challenges are repeating, but it seems it takes a super long time to capture enough to be able to just ‘look up’ the right answer without understanding the process.

# main.py
This program can be used to automatically record handshakes from a working system.

# repetitions.py
The scripts in this file were used to quantify the progress in recording handshakes, and trying to recognise patterns.

# crosscheck.py
This script is about comparing the data recorded from two different batteries. (Takes a long time to run!!)

# crosscheck.txt
This is the output of crosscheck.py. It shows the differences in the answers to challanges between different batteries.

# list_scott.csv
This file contains handshakes recorded from one battery.

# list_badconnector.csv
This file contains handshakes recorded from another battery.
