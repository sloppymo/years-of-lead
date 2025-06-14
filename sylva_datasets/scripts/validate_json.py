#!/usr/bin/env python3
import json

try:
    with open('years-of-lead/adolescent_responses.json', 'r') as f:
        data = json.load(f)
    print(f'JSON is valid with {len(data)} entries')
except json.JSONDecodeError as e:
    print(f'JSON error: {e}')
    print(f'Error position: line {e.lineno}, column {e.colno}')
    
    # Read the file to show context around the error
    with open('years-of-lead/adolescent_responses.json', 'r') as f:
        lines = f.readlines()
    
    start = max(0, e.lineno - 5)
    end = min(len(lines), e.lineno + 5)
    
    print(f'\nContext around error (lines {start+1}-{end}):')
    for i in range(start, end):
        marker = ' --> ' if i == e.lineno - 1 else '     '
        print(f'{marker}{i+1:3}: {lines[i].rstrip()}')