##RasPi - Set Up Static IP:

#### OMNIGO:
Edit the conf file:

	sudo nano /etc/dhcpcd.conf

Uncomment & complete:
```
interface wlan0
static ip_address=172.17.30.xxx/24
#stitic ip6_address=fd51:...
static routers=172.17.200.1
static domain_name_servers=172.17.10.111
```
---
#### TASKS:
1.) Get current router (**network IP**):
```
ip r | grep default
```

2.) Get current DNS server (**nameserver IP**):
```
sudo nano /etc/resolv.conf
```
Note the IP next to “nameserver“

3.) Modify the “dhcpcd.conf” configuration file:
```
sudo nano /etc/dhcpcd.conf
```

4.) Within this file, enter the following lines:

* Replace “**NETWORK**” with either “eth0” (Ethernet) **OR** you “wlan0” (WiFi)
* Replace “**STATICIP**” with the IP address that you want to assign
* Replace “**ROUTERIP**” with the network IP address
*  Replace “**DNSIP**" with the IP of the domain name server
	* either the IP you got in step 2 of this tutorial or another one such as Googles “8.8.8.8” or Cloudflare’s “1.1.1.1“
```
interface <NETWORK>
static ip_address=<STATICIP>/24
static routers=<ROUTERIP>
static domain_name_servers=<DNSIP>
```
5.) Save the file and reboot
