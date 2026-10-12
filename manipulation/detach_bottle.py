import os
import signal
import subprocess

try:

    result = subprocess.check_output(
        ["pgrep", "-f", "attach_bottle.py"]
    )

    for pid in result.decode().split():

        os.kill(
            int(pid),
            signal.SIGTERM
        )

    print("BOTTLE DETACHED")

except subprocess.CalledProcessError:

    print("No attach_bottle.py process found")