"""Hogwarts tests/coverage_output.py."""

import json
import xml.etree.ElementTree as ET

tree = ET.parse('coverage/coverage.xml')
attrib = tree.getroot().attrib

out = {
    'coverage_pct': float(attrib.get('line-rate')) * 100,
    'lines_total': int(attrib.get('lines-valid')),
    'lines_covered': int(attrib.get('lines-covered')),
    'branch_pct': int(attrib.get('branch-rate')),
    'branches_covered': int(attrib.get('branches-covered')),
    'branches_total': int(attrib.get('branches-valid')),
}

with open('coverage/coverage_output.json', 'w') as outfile:
    json.dump(out, outfile)
