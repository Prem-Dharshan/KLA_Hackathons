from collections import deque
from dataclasses import dataclass
import json
import logging
import os
import sys
from typing import List


def inputParser(filename: str) -> json:

    data = None

    with open(filename, 'r') as file:
        data = json.load(file)

    print(data)

    return data


def main () -> None:

    ip_file = "D:/22PW29/wafer-processing-optimization/Input/Milestone0.json"

    data = None

    with open(ip_file, 'r') as file:
        data = json.load(file)

    steps = {}
    for step in data["steps"]:
        steps[step["id"]] = step
    print("\nSteps\n", steps)

    machines = {}
    for m in data["machines"]:
        machines[m["machine_id"]] = m
    print("\nMachines", machines)

    # qtyies = {}
    # for w in data["wafers"]:
    #     qtyies[w["type"]] = w["quantity"]
    # print("\nQtyies: ", qtyies)

    wafers = {}
    for w in data["wafers"]:
        qty = w.pop('quantity')
        for wid in range(1, qty + 1):
            wafers[f"{w["type"]}-{wid}"] = w
    print("\nWafers", wafers)

    machine_ids = [m for m, val in machines.items()]
    print(f"\nM ids: {machine_ids}")

    params = set()
    for s, val in steps.items():
        for p in val["parameters"].keys():
            params.add(p)
    print("\nParams", params)

    curr_m_p = {}
    for m, val in machines.items():
        curr_m_p[m] = val["initial_parameters"]
    print("\nCurrent N Params: ", curr_m_p)

    step_machine = {}
    for m, val in machines.items():
        step_machine[val["step_id"]] = m
    print("\nStep machine mapping:", step_machine)

    w_processed = {}
    for mid in machine_ids:
        w_processed[mid] = 0
    print("\nMachine processed: ", w_processed)

    machine_curr_time = {}
    for m in machine_ids:
        machine_curr_time[m] = 0
    print("\nCurrent machine timestamps: ", machine_curr_time)

    schedule = []

    queue = deque()

    w_s = {}
    for wid, val in wafers.items():
        w_s[wid] = list(val["processing_times"].keys())
    print("\nW_S: ", w_s)

    while all(w_s.values()):
        for wid, sts in w_s.items():
            queue.append((wid, sts[0]))
            w_s[wid].pop(0)

    print("\nQueue: ", queue)

    wafer_ptime = {}
    for wid, val in wafers.items():
        wafer_ptime[wid] = 0

    flag = True
    while (queue):

        if (flag):
            wid, sid = queue.popleft()
            flag = False
        else:
            wid, sid = queue.pop()
            flag = True

        wval = wafers[wid]
        ptime = wval["processing_times"][sid]
    # for wid, wval in wafers.items():
    #     for sid, ptime in wval["processing_times"].items():
        if steps[sid]["dependency"] == None:
            mach = step_machine[sid]
            for pid, rangee in steps[sid]["parameters"].items():
                if rangee[0] <= curr_m_p[mach][pid] <= rangee[1]:
                    schedule.append(
                        {
                            "wafer_id": wid,
                            "step": sid,
                            "machine": mach,
                            "start_time": max(machine_curr_time[mach], wafer_ptime[wid]),
                            "end_time":  max(machine_curr_time[mach] + ptime, wafer_ptime[wid] + ptime)
                        }
                    )
                    machine_curr_time[mach] += ptime
                    wafer_ptime[wid] += ptime


    schedule = {"schedule": schedule}
    print("\n\nSchedule: ", schedule)
    
    json_object = json.dumps(schedule, indent=4)
    with open("./output.json", "w") as outfile:
        outfile.write(json_object)

    return None

if __name__ == '__main__':
    main()