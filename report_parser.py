import re

def parse_reference_range(text):
    # Matches forms like 13-17, 13.0-17.0, (<number> - <number>) or 13 - 17
    m = re.search(r"(\d+(?:\.\d+)?)[ ]*[-–][ ]*(\d+(?:\.\d+)?)", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return None

def flag_value(value, reference_range):
    # conservative numeric compare; if non-numeric, return unknown
    try:
        v = float(str(value))
        if not reference_range:
            return 'unknown'
        m = re.match(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)", reference_range)
        if not m:
            return 'unknown'
        low = float(m.group(1)); high = float(m.group(2))
        if v < low:
            return 'low'
        if v > high:
            return 'high'
        return 'normal'
    except Exception:
        return 'unknown'

def parse_report_text(text):
    findings = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # Try to find common lab line patterns: Name 13.5 g/dL (13.0-17.0)
    lab_pattern = re.compile(r"^(?P<name>[A-Za-z0-9 /+-]+?)\s+(?P<value>-?\d+\.?\d*)\s*(?P<unit>[A-Za-z%/\-\^\d]*)\s*(?:\(?\s*(?P<range>\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?)\s*\)?)?$")
    for i, line in enumerate(lines):
        m = lab_pattern.match(line)
        if m:
            name = m.group('name').strip()
            value = m.group('value')
            unit = m.group('unit').strip() or None
            ref = m.group('range') or parse_reference_range(line)
            flag = flag_value(value, ref)
            findings.append({'name': name, 'value': value, 'unit': unit, 'reference_range': ref, 'flag': flag, 'provenance': {'line': i+1, 'text': line}})
            continue
        # fallback: try to find name: value (range)
        colon_match = re.match(r"^(?P<name>[^:]+):\s*(?P<value>[-]?\d+\.?\d*)\s*(?P<unit>[^\(]*)\(?\s*(?P<range>\d+\.?\d*\s*[-–]\s*\d+\.?\d*)?", line)
        if colon_match:
            name = colon_match.group('name').strip()
            value = colon_match.group('value')
            unit = colon_match.group('unit').strip() or None
            ref = colon_match.group('range') or parse_reference_range(line)
            flag = flag_value(value, ref)
            findings.append({'name': name, 'value': value, 'unit': unit, 'reference_range': ref, 'flag': flag, 'provenance': {'line': i+1, 'text': line}})

    return {'findings': findings, 'provenance': {'lines': len(lines)}}
