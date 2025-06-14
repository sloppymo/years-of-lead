#!/usr/bin/env python3
import json
import re

# Read the corrupted file as text
with open('years-of-lead/adolescent_responses.json', 'r') as f:
    content = f.read()

# Find and fix the corrupted timestamp on line 404
# Pattern: "timestamp": "2024-01-16{
# Should be: "timestamp": "2024-01-16T02:50:00Z",

# Fix the specific corruption
content = re.sub(
    r'"timestamp": "2024-01-16\{',
    r'"timestamp": "2024-01-16T02:50:00Z",',
    content
)

# There may be other structural issues, let's also remove any duplicate entries
# that might have been accidentally created

# Try to parse and clean up the JSON
try:
    # First, let's try to find where the valid JSON ends
    lines = content.split('\n')
    valid_json_lines = []
    brace_count = 0
    in_array = False
    
    for i, line in enumerate(lines):
        if line.strip() == '[':
            in_array = True
            brace_count += 1
            valid_json_lines.append(line)
        elif in_array and line.strip() == ']':
            brace_count -= 1
            if brace_count == 0:
                valid_json_lines.append(line)
                break
        elif in_array:
            valid_json_lines.append(line)
    
    fixed_content = '\n'.join(valid_json_lines)
    
    # Try to parse the fixed content
    data = json.loads(fixed_content)
    
    # Remove any duplicate entries (same entry_id)
    seen_ids = set()
    cleaned_data = []
    for entry in data:
        if entry.get('entry_id') not in seen_ids:
            cleaned_data.append(entry)
            seen_ids.add(entry.get('entry_id'))
        else:
            print(f"Removed duplicate entry_id: {entry.get('entry_id')}")
    
    # Write the cleaned JSON
    with open('years-of-lead/adolescent_responses_fixed.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"Fixed JSON with {len(cleaned_data)} valid entries")
    print("Saved as: years-of-lead/adolescent_responses_fixed.json")

except json.JSONDecodeError as e:
    print(f"Still couldn't parse JSON: {e}")
    print(f"Error at line {e.lineno}, column {e.colno}")
    
    # Save the partially fixed content for manual inspection
    with open('years-of-lead/adolescent_responses_partial_fix.json', 'w') as f:
        f.write(fixed_content)
    print("Saved partially fixed content as: years-of-lead/adolescent_responses_partial_fix.json")