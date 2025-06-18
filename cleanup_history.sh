#!/bin/bash

# Create a backup of the current repository state
echo "Creating backup of current repository state..."
cd /home/sloppymo/Documents/Windsurf/years-of-lead

# Create a list of large files to remove
cat > /tmp/large_files.txt << 'EOL'
therapeutic_dataset_8000_complete.json
therapeutic_dataset_complete.json
therapeutic_dataset_extended.json
therapeutic_dataset_final_2000.json
therapeutic_dataset.json
sylva_cursor_dataset.json
adolescent_responses.json
sylva_diverse_voices_dataset.json
therapeutic_dataset_disability.json
maintenance_logs/
EOL

# Run git-filter-repo to remove large files from history
echo "Removing large files from Git history..."
git filter-repo --strip-blobs-bigger-than 10M \
  --path-glob '*.json' --invert-paths \
  --path maintenance_logs/ --invert-paths \
  --path src/ui/node_modules/ --invert-paths \
  --force

# Clean up and optimize repository
echo "Cleaning up and optimizing repository..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "Repository cleanup complete!"
