import sys
import logging
import getpass
from optparse import OptionParser
import subprocess
import sleekxmpp
from tkinter import *


global st
global rechnen


# set default encoding to utf8
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


###################################################
#hier wird die Klasse fuer den Empfaenger erstellt:
class empfang(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # start the session
        self.add_event_handler("session_start", self.start)

        # message handler
        #Wenn eine nachricht ankommt wird self.empfang ausgef+Ã¼hrt
        self.add_event_handler("message", self.empfang)

        
    def start(self, event):
        # session start method
        self.send_presence()
        self.get_roster()
        #Er ist bereit
        print("startet")
        
    def status(self):
        global rechnen
        global st
        if rechnen == True: #Status wird abgefragt
            status = Tk()
            g = Label(status, bg="green")
            g.pack()
            st = "beschÃƒÂ¤ftigt."
        else:
            status = Tk()
            r = Label(status, bg="red")
            r.pack()
            st = "arbeitslos."

    def empfang(self, msg):
        global st
        st = "null" #VorÃ¼bergÃ¤ngig
        print("NACHRICHT!")
        #Die Nachricht wir angezeigt
        print(msg['body'])
        print("Du bist gerade ", st)
#######################################################

        
#######################################################################
class senden(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # start the session
        self.add_event_handler("session_start", self.start)

        # send handler
        self.add_event_handler("nachricht_senden", self.nachricht_senden)

    def nachricht_senden(self):
        name = input("Name an: ")
        nachricht = input("Nachricht: ")
        self.send_message(name + "@ifga", nachricht)
        
    def start(self, event):
        # session start method
        self.send_presence()
        self.get_roster()
        self.nachricht_senden()
        
###################################################################
            
if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)


    
    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    x = input("Username: ")
    y = input("Password: ")
    opts.jid = x +'@ifga'
    opts.password = y
    print("Logged in as " + opts.jid)

    #Login Daten mpüssen hier auch noch mal eingetragen Werden !
    opts.jid = 'rosenbhe@ifga'
    opts.password = 'rosenbhe'

    # Setup the empfanger and register plugins.
    empfanger = empfang(opts.jid, opts.password)
    empfanger.register_plugin('xep_0030') # Service Discovery
    empfanger.register_plugin('xep_0004') # Data Forms
    empfanger.register_plugin('xep_0060') # PubSub
    empfanger.register_plugin('xep_0199') # XMPP Ping
    #for easy
    empfanger.auto_authorize = True
    empfanger.auto_subscribe = True



    senden = senden(opts.jid, opts.password)
    senden.register_plugin('xep_0030') # Service Discovery
    senden.register_plugin('xep_0004') # Data Forms
    senden.register_plugin('xep_0060') # PubSub
    senden.register_plugin('xep_0199') # XMPP Ping
    senden.auto_authorize = True
    senden.auto_subscribe = True

    # Connect to the XMPP server and start processing XMPP stanzas.
    if empfanger.connect(('odin', 5222), use_tls=True):
        empfanger.process(threaded=False) #block=True
        print("Done")
    else:
        print("Empfaenger is unable to connect.")


    if senden.connect(('odin', 5222), use_tls=False): #Kein SSL Zertifikat Error
        senden.process(threaded=False) #block=True
        print("Done")
    else:
        print("sender is unable to connect.")

status.mainloop()
