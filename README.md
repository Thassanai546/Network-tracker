# Network_Tracker :incoming_envelope:
## What is this?
* Guide: https://vinsloev.medium.com/python-cybersecurity-network-tracking-using-wireshark-and-google-maps-2adf3e497a93 \

With this tool you can take .pcap files from wireshark and turn them into xml files. What this will allow you to do is import them into google maps and visualize your network traffic. This is my second Python program. An example of one of the features is the automatic request for the public IP address of the device. 

## Instructions
1) Capture some network traffic on wireshark. After some time for example 20 seconds, you can click the red square in Wireshark to pause the capture.
2) Save this capture (File -> Export Specified Packets -> Filetype: wireshark/tcpdump/...-pcap
3) Place this file into the pcap_files folder. This folder is used by the program to check for specified files. You can obviously re-route this to anywhere you like.
4) Execute the program, if you choose to generate an XML file it should be found in the 'generated_files' folder. This is if you execute the program from its directory.

## Wireshark
* Download WireShark at: https://www.wireshark.org/
