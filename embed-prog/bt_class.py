import bluetooth
import time
from lock_control import lock_control
from btctlTest import btcl
import os

#TODO: change RB3 to not be an audio device?

time.sleep(10)

print("starting up")

os.system('sudo hciconfig hci0 piscan')

lock_control = lock_control()
btcl = btcl()
msg = 42
time.sleep(3)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

try:
    while True:
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        e = client_sock.send('hello')
        try:
            while True:
                msg = client_sock.recv(1024)
                msg = str(msg)
                msg = msg.replace("'", "")
                msg = msg[1:]
                msg = msg[:2]
                print(msg)
                print(isinstance(msg, str))
                if lock_control.validate_key(msg):
                    "Great open lock"
                    print("Key is valid lock is now unlocked")
                    if lock_control.unlock_lock():
                        "The lock is now unlocked for 30 sec"
                        time.sleep(5)
                        if lock_control.lock_lock():
                            "200 = success"
                            client_sock.send("200")
                            client_sock.close()
                            btcl.unpair()
                            print("The lock is now locked")
                            "Great lock is locked"
                        else:
                            "500 = internal error"
                            client_sock.send("500")
                            client_sock.close()
                            btcl.unpair()
                            "lock failed"
                    else:
                        "500 = internal error"
                        client_sock.send("500")
                        client_sock.close()
                        btcl.unpair()
                        "lock failed to unlock"
                else:
                    "401 = unauthorized"
                    client_sock.send("401")
                    client_sock.close()
                    btcl.unpair()
                    print("Key is no good")
        except OSError:
            client_sock.close()
            pass
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")