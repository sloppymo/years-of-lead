#!/bin/bash

# Years of Lead - Push Automated Playtest Changes
echo "🚀 Preparing to push Years of Lead automated playtest changes..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run this from your Years of Lead project root."
    exit 1
fi

echo "📁 Staging new files..."
git add automated_playtest.py
git add AUTOMATED_PLAYTEST_REPORT.md
git add PLAYTEST_NARRATIVE_HIGHLIGHTS.md
git add playtest_logs/

echo "🔧 Staging modified files..."
git add src/game/emotional_state.py
git add CHANGELOG.md

echo "📝 Creating commit..."
git commit -m "feat: Add automated playtest system and comprehensive testing

- Add automated_playtest.py: MAX mode testing framework for Phases 1 & 2
- Generate 20 mission iterations testing psychological integration
- Discover 17 bugs across 4 categories (captured agents, datetime, API mismatches)
- Create detailed analysis reports and narrative highlights
- Fix timedelta.hours bug in emotional_state.py
- Update CHANGELOG.md with comprehensive playtest findings

Key Findings:
- Psychological integration successfully creates emergent narratives
- Mission difficulty needs rebalancing (0% clean success rate)
- Betrayal mechanics need threshold adjustments
- Agent state management bugs require fixes

Testing reveals strong foundation for emotionally weighty insurgency simulation."

echo "🌐 Pushing to remote repository..."
git push origin main

echo "✅ Changes pushed successfully!"
echo ""
echo "📊 Summary of changes:"
echo "  - 1 new testing framework (746 lines)"
echo "  - 2 new documentation files"
echo "  - 20 detailed mission logs"
echo "  - 1 critical bug fix"
echo "  - Updated changelog"
echo ""
echo "🎯 Next steps:"
echo "  1. Review automated playtest report"
echo "  2. Prioritize bug fixes (captured agent logic)"
echo "  3. Adjust mission difficulty balance"
echo "  4. Run additional testing iterations"