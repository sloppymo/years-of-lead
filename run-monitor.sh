# run-monitor.sh
watch -n 5 '
echo "=== 1) CURRENT ITERATION LOGS (last lines) ===";
tail -n 5 maintenance_logs/iteration_0*.json 2>/dev/null | tail -n 20;
echo "";
echo "=== 2) MOST RECENT CHANGELOG ENTRIES ===";
tail -n 20 docs/developer/CHANGELOG.md;
echo "";
echo "=== 3) BALANCE-PHASE SUMMARY HEALTH ===";
tail -n 15 docs/reports/BALANCE_PHASE_SUMMARY.md;
echo "";
echo "=== 4) QUICK TEST PASS (all unit tests) ===";
python3 -m pytest -q tests/unit/test_*.py 2>/dev/null || echo "(tests pending)";
'
