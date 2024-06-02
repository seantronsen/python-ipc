from comms import *


server = ServerIPv4(ADDRESS)
try:
    while True:
        try:
            message = server.receive_once()
            print(f"received: {message}")
        except Exception as e:
            print(f"error: {e}")

except KeyboardInterrupt:
    print("rec interrupt")
except Exception as e:
    print("exception: ", e)
finally:
    print("shutting down")
    del server
