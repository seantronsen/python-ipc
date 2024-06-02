from communications import *
from line_profiler import profile


@profile
def main():
    server = ServerIPv4(ADDRESS)
    try:
        message = server.receive_once()
        print(f"server: received: {message}")

    except KeyboardInterrupt:
        print("server: received SIGTERM")
    except Exception as e:
        print(f"server: received unanticipated exception: {e}")
    finally:
        print("server: shutting down")
        del server

if __name__ == "__main__":
    main()
