#!/usr/bin/env python3
"""
Years of Lead - Experimental Emotional Forking Plugin

Implements advanced emotional memory forking, where memories can branch into multiple
versions based on emotional state, perspective, and symbolic interpretation.
"""

import sys
import os
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from game.entities import Agent, GameState
from game.advanced_relationships import MemoryEntry


class EmotionalForkType(Enum):
    """Types of emotional memory forks"""
    PERSPECTIVE_SHIFT = "perspective_shift"
    IDEOLOGICAL_FILTER = "ideological_filter"
    TRAUMA_DISTORTION = "trauma_distortion"
    WISHFUL_THINKING = "wishful_thinking"
    COLLECTIVE_MEMORY = "collective_memory"
    TEMPORAL_DECAY = "temporal_decay"


@dataclass
class MemoryFork:
    """Represents a forked memory with emotional/perspective variations"""
    original_memory_id: str
    fork_type: EmotionalForkType
    fork_id: str
    variant_summary: str
    emotional_divergence: Dict[str, float]
    symbolic_elements: List[str] = field(default_factory=list)
    created_turn: int = 0
    stability: float = 1.0


class EmotionalForkingEngine:
    """Manages emotional memory forking and narrative divergence"""

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.collective_memories = {}
        self.memory_resonance_threshold = 0.6
        self.fork_propagation_rate = 0.3

    def process_memory_forking(self, agent: Agent, memory: MemoryEntry) -> Optional[MemoryFork]:
        """Process potential forking for a memory"""
        if random.random() > 0.7:  # 30% chance of forking
            fork = MemoryFork(
                original_memory_id=memory.id,
                fork_type=EmotionalForkType.PERSPECTIVE_SHIFT,
                fork_id=f"fork_{memory.id}_{random.randint(1000, 9999)}",
                variant_summary=f"Reinterpreted: {memory.summary}",
                emotional_divergence={"hope": 0.2, "fear": -0.1},
                symbolic_elements=["transformation", "growth"],
                created_turn=self.game_state.turn_number
            )

            if not hasattr(agent, "memory_forks"):
                agent.memory_forks = []
            agent.memory_forks.append(fork)

            return fork
        return None

    def propagate_collective_memory(self, shared_memory_id: str, participating_agents: List[str]):
        """Propagate a collective memory fork across multiple agents"""
        collective_fork = MemoryFork(
            original_memory_id=shared_memory_id,
            fork_type=EmotionalForkType.COLLECTIVE_MEMORY,
            fork_id=f"collective_{shared_memory_id}_{random.randint(1000, 9999)}",
            variant_summary="Our shared memory of this event",
            emotional_divergence={"hope": 0.2, "trust": 0.2},
            symbolic_elements=["unity", "shared", "collective"],
            created_turn=self.game_state.turn_number,
            stability=0.9
        )

        # Apply to all participating agents
        for agent_id in participating_agents:
            agent = self.game_state.agents.get(agent_id)
            if agent:
                if not hasattr(agent, "memory_forks"):
                    agent.memory_forks = []
                agent.memory_forks.append(collective_fork)


def simulate_tick():
    """Simulate a single game tick for testing"""
    game_state = GameState()
    game_state.initialize_game()
    game_state.emotional_forking = EmotionalForkingEngine(game_state)
    return game_state


if __name__ == "__main__":
    print("Testing emotional forking system...")
    game_state = simulate_tick()
    print("Emotional forking system initialized successfully.")