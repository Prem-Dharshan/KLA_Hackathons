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
        w_processed[mach] = 0

    return schedule_entry

def process_dependencies(wafers, steps):
    dependencies = defaultdict(list)
    for step_id, step_data in steps.items():
        if step_data["dependency"]:
            for dep in step_data["dependency"]:
                dependencies[step_id].append(dep)

    sorted_wafers = {}
    for wid, wval in wafers.items():
        sorted_steps = []
        visited = set()
        queue = deque([step for step in wval["processing_times"].keys() if not steps[step]["dependency"]])
        while queue:
            step = queue.popleft()
            if step not in visited:
                visited.add(step)
                sorted_steps.append(step)
                for dep in [k for k, v in dependencies.items() if step in v]:
                    if dep in wval["processing_times"]:
                        queue.append(dep)
        sorted_wafers[wid] = sorted_steps
    return sorted_wafers

def main():
    ip_file = "D:/22PW29/wafer-processing-optimization/Input/Milestone4b.json"

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

    w_s = process_dependencies(wafers, steps)

    queue = deque()
    for wid, sorted_steps in w_s.items():
        for step in sorted_steps:
            queue.append((wid, step))

    wafer_ptime = {wid: 0 for wid in wafers}

    processed_steps = defaultdict(set)

    while queue:
        wid, sid = queue.popleft()

        if steps[sid]["dependency"] and not all(dep in processed_steps[wid] for dep in steps[sid]["dependency"]):
            queue.append((wid, sid))
            continue

        mid = step_machine[sid]
        mach = find_compliant_machine(mid, sid, steps, curr_m_p, machines, params)

        if mach is None:
            cooldown_machines(mid, machines, curr_m_p, machine_curr_time, params)
            queue.append((wid, sid))
            continue

        wval = wafers[wid]
        ptime = wval["processing_times"][sid]

        while not all(steps[sid]['parameters'][p][0] <= curr_m_p[mach][p] <= steps[sid]['parameters'][p][1] for p in params):
            cooldown_machines([mach], machines, curr_m_p, machine_curr_time, params)

        schedule_entry = assign_wafer_to_machine(wid, sid, mach, wafer_ptime, machine_curr_time, w_processed, curr_m_p, params, ptime, steps, machines)
        schedule.append(schedule_entry)

        processed_steps[wid].add(sid)

    schedule = {"schedule": schedule}

    with open("./output4b.json", "w") as outfile:
        json.dump(schedule, outfile, indent=4)

if __name__ == '__main__':
    main()
