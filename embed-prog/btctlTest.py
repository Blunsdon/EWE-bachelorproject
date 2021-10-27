from sh import bluetoothctl
import re

lopd = bluetoothctl("paired-devices")
print("lopd: " + str(lopd))
span = []
for device in lopd:
    search = re.search("[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]", device).span()
    span.append(search)

x = 0
mac_list = []
mac_str = ""
count = len(span)
for device in span:
    count -= count
    print("device: " + str(device))
    for mac_int in range(len(lopd[count])):
        if mac_int >= span[count][0] and mac_int < span[count][1]:
            mac_str += lopd[count][mac_int]
            x += 1
        print("mac_str: " + str(mac_str))
        mac_list.append(mac_str)

print(mac_list)

#ctl_unpair = "remove " + mac_str

#bluetoothctl("remove", mac_str)
