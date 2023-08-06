===============
Release History
===============

v0.1.8 (2021-07-26)
-----------------------------------
* Fix imcompatibility with dnspython 2.X 

v0.1.7 (2021-07-20)
-----------------------------------
* More descriptive error messages when dependency apps not installed

Initial Release v0.1.0 (2021-07-13)
-----------------------------------
1. Performs DNS zone transfers to collect an organization's A and CNAME 
   records.
2. Uses Masscan to scan for open HTTP/HTTPS ports on an organization's net 
   ranges, as well as any IP addresses outside those ranges that were present 
   in the organization's A and CNAME records.
3. Uses the Python requests library to collect all responses and store in a 
   MariaDB database. All DNS names corresponding to an IP with open HTTP/HTTPS 
   ports will be included in requests in addition to the IP address, so that 
   sites using different headers will not cause a website to be missed.
4. Downloads Wappalyzer web technologies database and stores in MariaDB 
   database, enabling users to query the location(s) of a common web technology 
   by name.
5. Allows users to query the location(s) where custom regexes are contained 
   within stored responses.
