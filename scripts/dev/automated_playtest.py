from __future__ import annotations

"""
automated_playtest.py
----------------------
Quick CLI-driven automated play-testing harness for the *Years of Lead* simulation.

Usage:
    python scripts/dev/automated_playtest.py [--turns 100] [--seed 42]

The play-tester will:
  1. Bootstrap a fresh `GameState` from `game.core` (same as the interactive CLI).
  2. Advance the simulation for the requested number of turns.
  3. Execute random high-level actions each turn (triggering the more complex internal
     systems that are already wired into `GameState.advance_turn`).
  4. Capture and log any unexpected exceptions, state inconsistencies, or suspicious
     values.
  5. Produce a final JSON report summarising all problems found and suggested fixes.

The script purposefully avoids *any* interactive input so that it can be run in CI
pipelines or inside a headless Docker container.
"""

import argparse
import json
import logging
import random
import traceback
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, List, Optional, Tuple, Type
import sys  # Need early to modify path

# -------------------------------------------------------------------------------------------------
# Logging configuration
# -------------------------------------------------------------------------------------------------

LOG_DIR = Path("maintenance_logs") / "playtests"
LOG_DIR.mkdir(parents=True, exist_ok=True)

project_root = Path(__file__).resolve().parent.parent.parent  # scripts/dev/.. -> project root
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "automated_playtest.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------
# Import the game – placed *after* logger setup so that any module-level logs go to our file.
# -------------------------------------------------------------------------------------------------

try:
    from game.core import GameState  # type: ignore
except ImportError as exc:  # pragma: no cover – early guard
    logger.critical("Failed to import game modules: %s", exc)
    raise SystemExit(1)

# -------------------------------------------------------------------------------------------------
# Helper structures
# -------------------------------------------------------------------------------------------------

class BugReport:
    """Structured information about a single bug encountered during play-testing."""

    def __init__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_tb: TracebackType,
        context: str,
        turn_number: int,
    ) -> None:
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb
        self.context = context
        self.turn_number = turn_number

    def as_dict(self) -> Dict[str, Any]:
        return {
            "turn": self.turn_number,
            "context": self.context,
            "exception_type": self.exc_type.__name__,
            "message": str(self.exc_value),
            "traceback": "".join(traceback.format_exception(self.exc_type, self.exc_value, self.exc_tb)),
            "suggested_fix": self._suggest_fix(),
        }

    # ------------------------------------------------------------------------------------------
    # Extremely naive patch suggestions – we just look for a few common patterns. Real-world
    # systems would employ static analysis or specialised LLM prompts.
    # ------------------------------------------------------------------------------------------
    def _suggest_fix(self) -> str:
        msg = str(self.exc_value)
        if isinstance(self.exc_value, AttributeError):
            attr = msg.split("'", 2)[1] if "'" in msg else "<unknown>"
            return (
                f"Attribute '{attr}' was missing. Ensure the attribute is initialised in __init__ or "
                "spelled correctly everywhere it is accessed."
            )
        if isinstance(self.exc_value, IndexError):
            return "Index out of range – validate list access and ensure indices are within bounds."
        if isinstance(self.exc_value, KeyError):
            key = msg.strip("'")
            return (
                f"Missing key '{key}' in dict – confirm that the key exists before access or use dict.get()."
            )
        # Default generic suggestion
        return "Investigate root cause and add appropriate error handling or state initialisation."

# -------------------------------------------------------------------------------------------------
# Core play-tester class
# -------------------------------------------------------------------------------------------------

class AutomatedPlayTester:
    """Runs a headless simulation and captures any issues encountered."""

    def __init__(self, turns: int, seed: Optional[int] = None):
        self.turns = turns
        self.seed = seed or random.randint(1, 1_000_000)
        random.seed(self.seed)
        self.game_state = GameState()
        self.game_state.initialize_game()

        self.bug_reports: List[BugReport] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> None:
        logger.info("Starting automated play-test: %d turns (seed=%d)", self.turns, self.seed)
        for _ in range(self.turns):
            turn = self.game_state.turn_number
            try:
                self._simulate_turn()
            except Exception as exc:  # pylint: disable=broad-except
                exc_type, exc_value, exc_tb = sys.exc_info()  # type: ignore[misc]
                logger.error("Exception on turn %d: %s", turn, exc)
                self.bug_reports.append(
                    BugReport(exc_type or Exception, exc_value or exc, exc_tb, context="advance_turn", turn_number=turn)
                )
                # Attempt graceful recovery: advance turn counter manually to avoid infinite loop
                self._force_advance_turn_on_failure()
        self._write_report()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _simulate_turn(self) -> None:
        """Advance the simulation one step and optionally trigger random actions."""
        # Step the core simulation (this fires missions, relationship events, etc.)
        self.game_state.advance_turn()

        # Random manual manipulations to increase coverage – 20% chance each.
        if random.random() < 0.2:
            self._trigger_random_agent_interaction()
        if random.random() < 0.2:
            self._trigger_random_betrayal_plan()

    def _trigger_random_agent_interaction(self) -> None:
        """Select two agents at random and make them interact (relationship system)."""
        agents = list(self.game_state.agents.values())
        if len(agents) < 2:
            return
        a, b = random.sample(agents, 2)
        try:
            result = a.interact_with(b)  # type: ignore[attr-defined]
            if result and random.random() < 0.05:
                logger.debug("Interaction result: %s", result)
        except Exception as exc:  # pylint: disable=broad-except
            exc_type, exc_value, exc_tb = sys.exc_info()  # type: ignore[misc]
            self.bug_reports.append(
                BugReport(exc_type or Exception, exc_value or exc, exc_tb, context="agent_interaction", turn_number=self.game_state.turn_number)
            )

    def _trigger_random_betrayal_plan(self) -> None:
        """Have a random agent plan betrayal to stress mission/loyalty subsystems."""
        agents = list(self.game_state.agents.keys())
        if len(agents) < 2:
            return
        betrayer_id, target_id = random.sample(agents, 2)
        try:
            self.game_state.create_betrayal_plan(
                agent_id=betrayer_id,
                target_agent_id=target_id,
                trigger_conditions={"turn": self.game_state.turn_number + random.randint(1, 5)},
                preferred_timing="future",
            )
        except Exception as exc:  # pylint: disable=broad-except
            exc_type, exc_value, exc_tb = sys.exc_info()  # type: ignore[misc]
            self.bug_reports.append(
                BugReport(exc_type or Exception, exc_value or exc, exc_tb, context="create_betrayal", turn_number=self.game_state.turn_number)
            )

    def _force_advance_turn_on_failure(self) -> None:
        """Ensure the simulation keeps moving forward after a catastrophic failure."""
        try:
            self.game_state.turn_number += 1  # pragma: no cover – fallback
        except Exception as exc:  # pragma: no cover
            logger.critical("Failed to force advance turn after crash: %s", exc)

    def _write_report(self) -> None:
        report_path = LOG_DIR / "playtest_report.json"
        with report_path.open("w", encoding="utf-8") as fp:
            json.dump(
                {
                    "total_turns": self.turns,
                    "seed": self.seed,
                    "bugs_found": len(self.bug_reports),
                    "bug_reports": [br.as_dict() for br in self.bug_reports],
                },
                fp,
                indent=2,
                ensure_ascii=False,
            )
        logger.info("Play-test complete: %d bugs found. Report saved to %s", len(self.bug_reports), report_path)

# -------------------------------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:  # noqa: D401 – simple interface
    parser = argparse.ArgumentParser(description="Automated play-testing harness for Years of Lead")
    parser.add_argument("--turns", type=int, default=100, help="Number of turns to simulate (default: 100)")
    parser.add_argument("--seed", type=int, help="RNG seed for deterministic runs")
    args = parser.parse_args(argv)

    tester = AutomatedPlayTester(turns=args.turns, seed=args.seed)
    tester.run()


if __name__ == "__main__":
    main()