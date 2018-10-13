#!/usr/bin/env python
# coding=UTF-8

import math, subprocess

class Battery(object):
    def __init__(self):
        pass

    def show_status(self):
        p = subprocess.Popen(["ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
        output = p.communicate()[0]

        o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
        o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]

        b_max = float(o_max.rpartition('=')[-1].strip())
        b_cur = float(o_cur.rpartition('=')[-1].strip())

        charge = b_cur / b_max
        charge_threshold = int(math.ceil(10 * charge))

        # Output

        total_slots, slots = 10, []
        filled = int(math.ceil(charge_threshold * (total_slots / 10.0))) * u'◼'
        # old arrow: ▹▸▶
        empty = (total_slots - len(filled)) * u'◻'

        out = (filled + empty).encode('utf-8')
        import sys

        RED   = "\033[1;31m"
        BLUE  = "\033[1;34m"
        YELLOW  = "\033[1;33m"
        CYAN  = "\033[1;36m"
        GREEN = "\033[0;32m"
        RESET = "\033[0;0m"
        BOLD    = "\033[;1m"
        REVERSE = "\033[;7m"

        color_out = (
            GREEN if len(filled) > 6
            else YELLOW if len(filled) > 4
            else RED
        )

        out = "[ " + color_out + out + RESET + " ]" + "\n"
        sys.stdout.write(out)
