import socket
import webbrowser
import dpkt
import pygeoip
import requests
from requests import get

# This database is found in the root of the project
gi = pygeoip.GeoIP('GeoLiteCity.dat')

# allow user to quickly open Google Maps to use their KML file
url = "https://www.google.com/maps/d/u/0/"

# this link allows you to get your public ip address
# More on Requests library here: http://docs.python-requests.org/en/latest/
try:
    ip = requests.get('https://api.ipify.org', timeout=.5).text
    print("IP: " + str(ip))
except:
    print("Could not get public IP address")

def main():
    # open captured data
    # create header and footer of KML file
    print("Enter 'q' to cancel.")
    while True:
        print("Enter name of .pcap file to use: ")
        response = input()

        if response == 'q' or response == 'Q':
            print("You have chosen to exit.")
            exit()

        # if user does not add file extension
        if ".pcap" not in response:
            response = response + ".pcap"
        print(response)

        try:
            # 'rb' means open file in binary format for reading.
            # 'wb' would mean opening the file for binary writing
            f = open("*Wherever you want files to be created*" + response, 'rb')
            break
        except OSError as e:
            print("Error: " + str(e.errno) + "\n File could not be found.")

    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml ' \
                'xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n' \
                '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'

    # building doc
    kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

    print("Output a file? [y/N]")
    response = input()
    if response == 'y' or response == 'Y':
        print("Enter file name: ")
        fname = input()

        if '.kml' not in fname:
            fname += '.kml'

        # w+ indicates Python to write file and create if it does not exist
        file = open("generated_files/" + fname, "w+")
        file.write(kmldoc)
        file.close()
        print("A file has been generated.")
    else:
        print(kmldoc)  # prints to terminal

    print('Open google maps? [y/N]')
    response = input()
    if response == 'y' or response == 'Y':
        # uses default browser
        webbrowser.open_new(url)
        print('Create a new map on this site and add the file as a layer to view details.')


def plotIPs(pcap):
    # method that will loop over captured network data and extract IP's.
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            # inet_ntoa returns IP address in dotted quad-string format.
            # it takes ip addresses in 32-bit packed format as an argument
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts


def retKML(dstip, srcip):
    # Attach geo location to IP's
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name(ip)  # your public IP address, this was found using 'requests'
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
                  '<Placemark>\n'
                  '<name>%s</name>\n'
                  '<extrude>1</extrude>\n'
                  '<tessellate>1</tessellate>\n'
                  '<styleUrl>#transBluePoly</styleUrl>\n'
                  '<LineString>\n'
                  '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
                  '</LineString>\n'
                  '</Placemark>\n'
              ) % (dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''


if __name__ == '__main__':
    main()
