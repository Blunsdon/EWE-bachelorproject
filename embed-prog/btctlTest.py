import sh
import re

class btcl(object):
    def unpair(self):
        lopd = sh.bluetoothctl("paired-devices")
        llopd = []

        for device in lopd:
            llopd.append(device)

        span = []
        for device in llopd:
            search = re.search("[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]", device)
            span.append(search.group(0))

        for mac_str in span:
            sh.bluetoothctl("remove", mac_str)
