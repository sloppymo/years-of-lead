def test_betrayal_plan_and_memory(game_state, two_agents):
    """Creating a betrayal plan should attach to agent and be retrievable via GameState helpers."""
    agent_a_id, agent_b_id = two_agents

    # Ensure no plan exists initially
    assert game_state.agents[agent_a_id].planned_betrayal is None

    trigger_conditions = {"affinity_below": -50, "trust_below": 10}

    plan = game_state.create_betrayal_plan(
        agent_id=agent_a_id,
        target_agent_id=agent_b_id,
        trigger_conditions=trigger_conditions,
        preferred_timing="immediate",
    )

    # Plan should be returned and linked to agent
    assert plan is not None
    assert game_state.agents[agent_a_id].planned_betrayal is plan

    # Creating a memory entry should succeed
    memory = game_state.create_memory_entry(
        agent_id=agent_a_id,
        event_type="betrayal_plan_created",
        other_agent_id=agent_b_id,
        custom_summary="Agent planned betrayal against rival.",
    )

    assert memory is not None

    # Memory should appear in agent memory journal
    memories = game_state.get_agent_memories(agent_a_id, turns_back=1)
    assert any(m.summary == memory.summary for m in memories)
