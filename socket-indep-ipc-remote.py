from communications import *
import time
import os
from line_profiler import profile
import numpy as np


@profile
def main():
    start = time.time()
    image = np.random.randint(low=0, high=255, size=10000**2)
    print(f"client {os.getpid()}: time to generate image - {time.time() - start}s")

    if __name__ == "__main__":
        message = Message(kind="OBJECT", content=image)
        client = ClientIPv4(address=ADDRESS)
        client.send_single(message=message)

    print(f"client ({os.getpid()}): finished - time on task: {time.time() - start}s")


if __name__ == "__main__":
    main()
