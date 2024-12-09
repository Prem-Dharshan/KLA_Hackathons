from collections import defaultdict, deque
import json


def input_parser(filename: str) -> dict:
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def find_compliant_machine(mid, sid, steps, curr_m_p, machines, params):
    for m in mid:
        if all(steps[sid]['parameters'][p][0] <= curr_m_p[m][p] <= steps[sid]['parameters'][p][1] for p in params):
            return m
    return None


def cooldown_machines(mid, machines, curr_m_p, machine_curr_time, params):
    for m in mid:
        machine_curr_time[m] += machines[m]['cooldown_time']
        for p in params:
            curr_m_p[m][p] = machines[m]["initial_parameters"][p]


def assign_wafer_to_machine(wid, sid, mach, wafer_ptime, machine_curr_time, w_processed, curr_m_p, params, ptime, steps, machines):
    start_time = max(machine_curr_time[mach], wafer_ptime[wid])
    end_time = start_time + ptime

    schedule_entry = {
        "wafer_id": wid,
        "step": sid,
        "machine": mach,
        "start_time": start_time,
        "end_time": end_time
    }

    machine_curr_time[mach] = end_time
    wafer_ptime[wid] = end_time
    w_processed[mach] += 1

    if w_processed[mach] >= machines[mach]["n"]:
        for p in params:
            curr_m_p[mach][p] += machines[mach]['fluctuation'][p]
        # Reset the processed count after fluctuation
        w_processed[mach] = 0 

    return schedule_entry


def main():
    ip_file = "D:/22PW29/wafer-processing-optimization/Input/Milestone3c.json"

    data = input_parser(ip_file)

    steps = {step["id"]: step for step in data["steps"]}
    machines = {m["machine_id"]: m for m in data["machines"]}
    wafers = {f"{w['type']}-{wid}": w for w in data["wafers"] for wid in range(1, w.pop('quantity') + 1)}

    machine_ids = list(machines.keys())

    params = set(p for s in steps.values() for p in s["parameters"].keys())

    curr_m_p = {m: machines[m]["initial_parameters"].copy() for m in machines}

    step_machine = defaultdict(list)
    for m, val in machines.items():
        step_machine[val["step_id"]].append(m)

    w_processed = {m: 0 for m in machines}

    machine_curr_time = {m: 0 for m in machines}

    schedule = []

    queue = deque()

    w_s = {wid: list(val["processing_times"].keys()) for wid, val in wafers.items()}

    while all(w_s.values()):
        for wid, sts in w_s.items():
            queue.append((wid, sts.pop(0)))

    wafer_ptime = {wid: 0 for wid in wafers}

    while queue:
        wid, sid = queue.popleft()
        
        mid = step_machine[sid]
        mach = find_compliant_machine(mid, sid, steps, curr_m_p, machines, params)

        if mach is None:
            cooldown_machines(mid, machines, curr_m_p, machine_curr_time, params)
            queue.append((wid, sid))
            continue

        wval = wafers[wid]
        ptime = wval["processing_times"][sid]

        # Validate machine params before process the wafer
        while not all(steps[sid]['parameters'][p][0] <= curr_m_p[mach][p] <= steps[sid]['parameters'][p][1] for p in params):
            cooldown_machines([mach], machines, curr_m_p, machine_curr_time, params)

        schedule_entry = assign_wafer_to_machine(wid, sid, mach, wafer_ptime, machine_curr_time, w_processed, curr_m_p, params, ptime, steps, machines)
        schedule.append(schedule_entry)

    schedule = {"schedule": schedule}

    with open("./output3c.json", "w") as outfile:
        json.dump(schedule, outfile, indent=4)


if __name__ == '__main__':
    main()

# Complete 3c
