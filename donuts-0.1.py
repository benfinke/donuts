"""
Created on January 5, 2012

@author - Ben Finke - @benfinke

DoNutS - DNS Testing and scoring tool

Send a series of DNS requests to a target DNS server and score the response time and the accuracy of the results.

Usage: ./donuts.py <DNS server> <file of targets> <number of DNS queries> <number of threads>

By default we do 10 DNS queries for each entry in the file and 1 thread.  Output goes to screen.

"""

import socket
from sys import argv
from os.path import exists
import dns.resolver
from dns import resolver

script, server, times = argv

numtimes = int(times)

site_key = {}

list_sites = []

print "Welcome to DoNutS.  Let's get started."

workingresolver = resolver.Resolver()
workingresolver.nameservers = [server]
print "Attempting DNS lookups against the following servers:"
for i in workingresolver.nameservers:
    print i +"\n"
attempts = 1
i = 0
x = 0
good_result = 0
bad_result = 0

while attempts <= numtimes:
    site = list_sites[x]
    result = workingresolver.query(site, "A")
    #result = socket.gethostbyname(site)
    for rdata in result:
        addresult = rdata.address
    print "Attempt number %d for %s results in %s.\n" % (attempts, site, addresult)
    if addresult == site_key[site]:
        print "Result matches expected value."
        good_result += 1
    else:
        print "The value returned isn't what we expected.  Recieved %s instead of %s." % (addresult, site_key[site])
        bad_result += 1
    attempts += 1
    i += 1
    x = i % 4 # use modulus to make sure the number stays in the range of sites we are using
    
print "Stats: Good results -> %d/%d  Bad results -> %d/%d." % (good_result, numtimes, bad_result, numtimes)
print "Shutting down.  Thanks for playing!"


