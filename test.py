from mctools import RCONClient
import sys
rcon = RCONClient("127.0.0.1", 25575)
rcon.login("chipmunk")
# rcon.start()
# if not rcon.is_authenticated():
#     sys.exit(1)
# for i in range(432, 10):
#     print(rcon.command(f"fill {i} -60 0 1280 -63 {i+6} air"))
# print(rcon.command("fill 0 -60 0 768 -63 10 air"))
