#!/usr/bin/env python
__author__ = 'Ben Finke'
"""
target_gen.py is a utility to automatically build the targets file for donuts.py

You can pass target_gen.py a file with DNS names, or use the interactive menu to build the list.
The rdataing file contains the DNS names of note and the correct IP address to monitor for.

March 2015
@benfinke

Usage: python target_gen.py -i <input_file> -o <output_file>

"""

import sqlite3
import sys
import dns.resolver

db_file = "donuts.db"

# Set up SQLite instance
def setup_db():
    db_conn = sqlite3.connect(db_file)

    with db_conn:
        cur = db_conn.cursor()
        cur.execute("DROP TABLE IF EXISTS targets")
        cur.execute("""
            CREATE TABLE targets(
                id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                dns_address TEXT KEY,
                a_ip TEXT,
                aaaa_ip TEXT,
                mx_ip TEXT,
                soa_ip TEXT,
                ns_ip TEXT,
                txt_ip TEXT)

        """)


# Display data in table
def display_entries():
   db_conn = sqlite3.connect(db_file)
   with db_conn:
       db_conn.row_factory = sqlite3.Row
       cur = db_conn.cursor()
       cur.execute("SELECT * from targets")
       rows = cur.fetchall()

       for row in rows:
           print ("%d -- %s -- %s -- %s -- %s -- %s -- %s" % (row['id_num'], row['dns_address'], row['a_ip'], row['aaaa_ip'], row['mx_ip'], row['ns_ip'], row['txt_ip']))



# Function to show contents of table


# function to populate the table
def print_menu():
    print (30 * '-')
    print (" Manage the target DB for donuts.")
    print (30 * '-')
    print ("1. Display the current entries.")
    print ("2. Enter a new target address.")
    print ("3. Upload a file of address to add.")
    print ("4. Remove an entry.")
    print ("5. Reset the table completely.")
    print ("6. Exit this menu")
    print (30 * '-')

def modify_table():
    loop = True

    while loop:
        print_menu()
        choice = raw_input("Enter your choice: ")
        choice = int(choice)
        if choice == 1:
            print ("Current entries in donuts:")
            display_entries()
        elif choice == 2:
            new_entry = raw_input ("Enter the DNS name you'd like to track:")
            add_entry(new_entry)
        elif choice == 3:
            new_file = raw_input ("Enter the filename to upload: ")
            # validate the file exists and it can be read
            # loop through the file and add each DNS name to the db
        elif choice == 4:
            del_entry = raw_input("Enter the DNS name or ID number to remove: ")
            #check to see if integer or dns name was entered
            #find the entry that matches, present it to the user for confirmation
            # if confirmed, remove from the table, loop back to main menu
            # if not confirmed, loop back to deletion choice
        elif choice == 5:
            setup_db()
        elif choice == 6:
            loop=False
        else:
            print ("Invalid entry, try again using a number 1-6.")



# FUnction to validate that entry is a valid DNS name
def validate_dns(address):
    #only allow alphanumeric, dash, and period.  All other characters are illegal
    return True

def add_entry(address):
        # validate DNS name, then perform a full lookup for supported DNS types
    if validate_dns(address):
        a_ip = []
        aaaa_ip = []
        mx_ip = []
        ns_ip = []
        soa_ip = []
        txt_ip = []

        test_resolver = dns.resolver.Resolver()
        try:
            a_ip_answer = test_resolver.query(address, "A")
        except dns.resolver.NoAnswer:
            print ("No answer received for A.")
            a_ip_answer = ""
        try:
            aaaa_ip_answer = test_resolver.query(address, "AAAA")
        except dns.resolver.NoAnswer:
            print ("No answer received for AAAA.")
            aaaa_ip_answer = ""
        try:
            mx_ip_answer = test_resolver.query(address, "MX")
        except dns.resolver.NoAnswer:
            print ("No answer received for MX.")
            mx_ip_answer = ""
        try:
            ns_ip_answer = test_resolver.query(address, "NS")
        except dns.resolver.NoAnswer:
            print ("No answer received for NS.")
            ns_ip_answer = ""
        try:
            soa_ip_answer = test_resolver.query(address, "SOA")
        except dns.resolver.NoAnswer:
            print ("No answer received for SOA.")
            soa_ip_answer = ""
        try:
            txt_ip_answer = test_resolver.query(address, "TXT")
        except dns.resolver.NoAnswer:
            print ("No answer received for TXT.")
            txt_ip_answer = ""

        for rdata in a_ip_answer:
            a_ip.append(rdata.address)
            #print a_ip

        for rdata in aaaa_ip_answer:
            aaaa_ip.append(rdata.address)
            #print aaaa_ip

        for rdata in mx_ip_answer:
            mx_ip.append(rdata.exchange)
            #print mx_ip

        for rdata in ns_ip_answer:
            ns_ip.append(rdata.target)
            #print ns_ip

        for rdata in soa_ip_answer:
            soa_ip.append(rdata.rname)
            #print soa_ip

        for rdata in txt_ip_answer:
            txt_ip.append(rdata.strings)
            #print txt_ip

        a = str(a_ip)
        aaaa = str(aaaa_ip)
        mx = str(mx_ip)
        ns = str(ns_ip)
        soa = str(soa_ip)
        txt = str(txt_ip)
        params = (address, a, aaaa, mx, ns, soa, txt)

        db_conn = sqlite3.connect(db_file)
        with db_conn:
            cur = db_conn.cursor()
            cur.execute("INSERT INTO targets VALUES(NULL,?,?,?,?,?,?,?)",params)

    else:
        print ("The address you provided is not a valid DNS name.")

# Main function


modify_table()



