import sys
import csv

#Heuristics
def filter_noncomponents(row):
    id, refs, fp, count, value = row
    if fp.lower().startswith("measurement_point"):
        return None
    if fp.lower().startswith("fiducial"):
        return None
    if value.lower() == "jumper" or (fp.lower().startswith('gs') and fp[2].isdigit()):
        return None
    return row

def is_passive(component):
    is_rc = component["footprint"][:2] in ['R_', 'C_']
    #ref_is_rc = all([ref[0] in ["R", "C"] for ref in component["references"].split(',')])
    return is_rc #and ref_is_rc

def is_pinheader(component):
    is_straight_ph = component["footprint"].startswith("Pin_Header_Straight_")
    is_angled_ph = component["footprint"].startswith("Pin_Header_Angled_")
    return is_straight_ph or is_angled_ph

def is_breakout(component):
    is_breakout = component["value"].lower().endswith("_breakout")
    return is_breakout

# Description creation functions

def create_pinheader_description(component):
    marker = "Pin_Header_"
    fp_parts = component["footprint"][len(marker):].split('_')
    if len(fp_parts) == 2:
        type, size = fp_parts
        pitch_desc = 'Pitch2.54mm'
    elif len(fp_parts) == 3:
        type, size, pitch_desc = fp_parts
    else:
        raise ValueError("Unknown pinheader footprint: {}".format(component["footprint"]))
    pitch = pitch_desc[5:]
    return "{} {} pinheader ({})".format(size, type.lower(), pitch)

def create_passive_description(component):
    fp_parts = component["footprint"].split('_')
    if fp_parts[-1].lower() == "handsoldering":
        fp_parts = fp_parts[:-1]
    if len(fp_parts) == 3:
        fp_parts = fp_parts[:2]
    if len(fp_parts) != 2:
        raise ValueError("Unknown R/C footprint: {}".format(component["footprint"]))
    ref_code = component["references"][0][0]
    name = {"R":"resistor", "C":"capacitor", "D":"diode", "L":"inductor"}[ref_code]
    case = fp_parts[1]
    value = component["value"]
    return "{} {} {}".format(case, value, name)


def create_breakout_description(component):
    name = component["value"].rsplit('_', 1)[0]
    return "{} breakout".format(name)

#Output formatting

def get_description(component):
    if is_passive(component):
        s = create_passive_description(component)
    elif is_pinheader(component):
        s = create_pinheader_description(component)
    elif is_breakout(component):
        s = create_breakout_description(component)
    else:
        s = component["value"] + " " + component["footprint"]
    return "{}pcs: {} ({})".format(component["count"], s, component["references"])

#Data conversion

def get_component_from_row(row):
    id, refs, fp, count, value = row
    component = {}
    component["references"] = refs
    component["footprint"] = fp
    component["count"] = count
    component["value"] = value
    component["description"] = get_description(component)
    return component

filename = sys.argv[1]
base_filename = filename.rsplit('.', 1)[0]

components = []

with open(filename, 'r') as f:
    csv = csv.reader(f, delimiter=';', quotechar='"')
    for row in csv:
        if csv.line_num == 1: # heading
            continue
        row = [el.strip() for el in row][:5]
        row = filter_noncomponents(row)
        if row:
            #print ', '.join(row)
            component = get_component_from_row(row)
            components.append(component)

for component in components:
    print(component["description"])
