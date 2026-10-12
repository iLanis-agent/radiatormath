import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def room_plan(lengthM, widthM, heightM, factor):
    if not (lengthM > 0) or not (widthM > 0) or not (heightM > 0) or not (factor > 0):
        return {"error": "length, width, height and factor must be positive"}
    volume = lengthM * widthM * heightM
    watts = math.floor(volume * factor + 0.5)
    btu = math.floor(watts * 3.412 + 0.5)
    if watts < 600: verdict = "a small panel covers it"
    elif watts < 1500: verdict = "one standard panel covers it"
    elif watts < 3000: verdict = "one large or two smaller panels share it"
    else: verdict = "several radiators share the load"
    return {"volume": round1(volume), "watts": watts, "btu": btu, "verdict": verdict}

def delta_plan(flowC, returnC, roomC, ratedW):
    if not (flowC > 0) or not (returnC > 0) or not (roomC > 0) or not (ratedW > 0):
        return {"error": "flow, return, room and rating must be positive"}
    mean = round1((flowC + returnC) / 2)
    dt = round1(mean - roomC)
    if dt <= 0:
        return {"error": "the water must be warmer than the room"}
    if dt >= 50: factor, verdict = 1.0, "full rated output on the labeled table"
    elif dt >= 40: factor, verdict = 0.75, "three quarters on the labeled table"
    elif dt >= 30: factor, verdict = 0.51, "about half on the labeled table"
    elif dt >= 20: factor, verdict = 0.3, "under a third on the labeled table"
    else: factor, verdict = 0.12, "a trickle on the labeled table"
    real = math.floor(ratedW * factor + 0.5)
    return {"mean": mean, "dt": dt, "factor": jsnum(factor), "real": real, "verdict": verdict}

def section_plan(neededW, perSectionW):
    if not (neededW > 0) or not (perSectionW > 0):
        return {"error": "need and section output must be positive"}
    sections = math.ceil(neededW / perSectionW)
    total = sections * perSectionW
    spare = total - neededW
    if sections <= 8: verdict = "a compact radiator covers it"
    elif sections <= 16: verdict = "a standard column covers it"
    else: verdict = "a long column - two smaller radiators share the load"
    return {"sections": sections, "total": total, "spare": spare, "verdict": verdict}

def render_room(r, lengthM, widthM, heightM, factor):
    return ("A room " + fmt(lengthM) + " m x " + fmt(widthM) + " m x " + fmt(heightM) + " m holds "
            + fmt(r["volume"]) + " m3; at a labeled " + fmt(factor) + " W per m3 it asks for about "
            + plural(r["watts"], "watt") + " (" + plural(r["btu"], "BTU", "BTU") + ") - " + r["verdict"] + ".")

def render_delta(r, flowC, returnC, roomC, ratedW):
    return ("Flow " + fmt(flowC) + " C, return " + fmt(returnC) + " C and a " + fmt(roomC)
            + " C room put the mean water at " + fmt(r["mean"]) + " C, " + fmt(r["dt"])
            + " C above the room: a radiator rated at " + plural(ratedW, "watt") + " gives about "
            + plural(r["real"], "watt") + " here - " + r["verdict"] + ".")

def render_section(r, neededW, perSectionW):
    return (plural(neededW, "watt") + " needed, " + plural(perSectionW, "watt") + " a section: "
            + plural(r["sections"], "section") + ", " + plural(r["total"], "watt") + " total, "
            + plural(r["spare"], "watt") + " of headroom - " + r["verdict"] + ".")

cases = []
for a in [(4, 5, 2.5, 40), (3, 4, 2.4, 50), (2, 2, 2.2, 30), (6, 7, 3, 50), (0, 5, 2.5, 40)]:
    r = room_plan(*a)
    cases.append({"fn": "roomPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_room(r, *a)})
for a in [(75, 65, 20, 2000), (70, 60, 20, 2000), (60, 50, 20, 2000), (50, 40, 20, 2000), (40, 30, 20, 2000), (20, 20, 25, 2000), (0, 65, 20, 2000)]:
    r = delta_plan(*a)
    cases.append({"fn": "deltaPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_delta(r, *a)})
for a in [(2080, 500), (1440, 600), (264, 200), (5000, 300), (6300, 450), (0, 500)]:
    r = section_plan(*a)
    cases.append({"fn": "sectionPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_section(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
