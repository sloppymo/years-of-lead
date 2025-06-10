import os, sys, random
# Ensure src package on path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from game.revolutionary_ecosystem import RevolutionaryEcosystem


def test_counterintel_sweep_detection():
    """Sleeper cell should have a chance to be exposed by counterintel sweep"""
    random.seed(123)
    eco = RevolutionaryEcosystem()
    eco.initialize_default_factions()
    handler = eco.active_factions[0].name
    target = eco.active_factions[1].name
    cell = eco.deploy_sleeper_cell(handler, target)
    # Increase target heat to boost sweep probability
    target_faction = next(f for f in eco.active_factions if f.name == target)
    target_faction.government_heat = 9.0
    # Run multiple turns to allow sweeps
    exposed = False
    for _ in range(10):
        eco.simulate_ecosystem_turn()
        if not cell.active:
            exposed = True
            break
    assert exposed, "Sleeper cell should eventually be exposed under high heat"