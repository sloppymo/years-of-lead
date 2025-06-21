# Willow System Implementation Guide

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv willow_env
source willow_env/bin/activate  # On Windows: willow_env\Scripts\activate

# Install dependencies
pip install -r requirements_willow.txt
```

### Basic Usage

```python
from willow_integrated_system import WillowIntegratedCore

# Initialize with configuration
config = {
    "symbol_preference": "nature",  # or "traditional", "minimal", "none"
    "escalation_thresholds": {
        "capacity": 2.0,
        "arousal": 9.5,
        "language_switch_count": 3
    }
}

willow = WillowIntegratedCore(config)

# Process a message
result = willow.process_message(
    user_id="tenant_123",
    message="My heat isn't working and it's freezing!",
    emotional_state={
        "arousal": 8.5,
        "capacity": 4.0,
        "urgency": 9
    },
    context={
        "response_time": 3.2,
        "symbol_preference": "nature"
    }
)

print(result["response"])
```

## Component Configuration

### 1. Symbolic Anchor Configuration

```python
# Symbol styles available
SYMBOL_STYLES = {
    "traditional": {
        "grounding": "💙",
        "presence": "🫂", 
        "hope": "🌟"
    },
    "nature": {
        "grounding": "🌊",
        "presence": "🌿",
        "hope": "🌅"
    },
    "minimal": {
        "grounding": "•",
        "presence": "→",
        "hope": "✓"
    },
    "none": {
        # Empty symbols for users who prefer plain text
    }
}
```

### 2. Tier Flow Rules

```python
TIER_RULES = {
    "tier_1_minimum": 2,        # Minimum containment responses
    "tier_1_timeout": 300,      # 5 minutes before tier 1 expires
    "capacity_threshold": 3.0,  # Minimum capacity for tier 2
    "arousal_threshold": 7.0,   # Maximum arousal for tier 2
    "consent_keywords": ["ready", "yes", "help", "options", "what can"]
}
```

### 3. Capacity Decay Indicators

```python
DECAY_INDICATORS = {
    "rapid_decline": {
        "threshold": -2.0,  # 2 point drop
        "window": 300       # in 5 minutes
    },
    "sustained_low": {
        "threshold": 3.0,   # Below 3.0
        "duration": 600     # for 10 minutes
    },
    "dissociation": {
        "coherence_drop": 0.3,
        "latency_spike": 2.0
    }
}
```

### 4. Language Detection

```python
SUPPORTED_LANGUAGES = {
    "es": "Spanish",
    "zh": "Chinese",
    "ar": "Arabic", 
    "tl": "Tagalog"
}

# Crisis keywords by language
CRISIS_WORDS = {
    "es": ["ayuda", "socorro", "emergencia"],
    "zh": ["帮助", "救命", "紧急"],
    "ar": ["ساعدني", "طوارئ"],
    "tl": ["tulong", "emergency"]
}
```

## Integration Patterns

### Pattern 1: Crisis with Gradual Capacity Decline

```python
# Initial high-stress contact
response_1 = willow.process_message(
    user_id="user_123",
    message="Basement flooding, everything ruined!",
    emotional_state={"arousal": 9, "capacity": 5}
)
# Returns: Tier 1 containment with symbols

# Capacity declining
response_2 = willow.process_message(
    user_id="user_123", 
    message="can't think straight",
    emotional_state={"arousal": 8, "capacity": 3}
)
# Returns: Simplified language, continued Tier 1

# Severe exhaustion
response_3 = willow.process_message(
    user_id="user_123",
    message="...",
    emotional_state={"arousal": 7, "capacity": 1}
)
# Returns: Emergency escalation to human
```

### Pattern 2: Bilingual Crisis Escalation

```python
# English start
response_1 = willow.process_message(
    user_id="user_456",
    message="Pipes burst in apartment!",
    emotional_state={"arousal": 8, "capacity": 6}
)

# Language switching under stress
response_2 = willow.process_message(
    user_id="user_456",
    message="No puedo más, my kids are crying!",
    emotional_state={"arousal": 9, "capacity": 4}
)
# Detects code-switching, adds bilingual acknowledgment

# Full bilingual crisis
response_3 = willow.process_message(
    user_id="user_456",
    message="AYUDA!! Emergency!!",
    emotional_state={"arousal": 9.5, "capacity": 3}
)
# Triggers bilingual human routing
```

## Advanced Features

### Custom Escalation Triggers

```python
class CustomEscalationTrigger:
    def should_escalate(self, session_data):
        # Add custom business logic
        if session_data["interaction_count"] > 10:
            return True, "prolonged_crisis"
        
        if "suicide" in session_data["message"].lower():
            return True, "safety_concern"
            
        return False, None

# Register custom trigger
willow.add_escalation_trigger(CustomEscalationTrigger())
```

### Session Analytics

```python
# Get detailed session metrics
session_id = "user_123"
metrics = willow.get_session_analytics(session_id)

print(f"Tier progression: {metrics['tier_history']}")
print(f"Capacity trend: {metrics['capacity_trend']}")
print(f"Language switches: {metrics['language_switches']}")
print(f"Escalation triggers: {metrics['escalation_triggers']}")
```

### Batch Processing for Analysis

```python
# Process historical conversations
historical_messages = load_historical_data()

results = []
for msg in historical_messages:
    result = willow.process_message(
        user_id=msg["user_id"],
        message=msg["text"],
        emotional_state=msg["emotional_state"]
    )
    results.append({
        "original": msg,
        "willow_response": result,
        "would_escalate": result["action"] == "escalate_to_human"
    })

# Analyze patterns
escalation_rate = sum(1 for r in results if r["would_escalate"]) / len(results)
print(f"Historical escalation rate: {escalation_rate:.2%}")
```

## Error Handling

### Graceful Degradation

```python
try:
    result = willow.process_message(user_id, message, emotional_state)
except SymbolicSystemError:
    # Fall back to no symbols
    willow.config["symbol_preference"] = "none"
    result = willow.process_message(user_id, message, emotional_state)
    
except TierControlError:
    # Fall back to Tier 1 only
    result = {
        "response": "I'm here with you. This situation sounds overwhelming.",
        "action": "continue",
        "tier": "tier_1_fallback"
    }
    
except Exception as e:
    # Ultimate fallback
    result = {
        "response": "I'm connecting you with human support right away.",
        "action": "escalate_to_human",
        "reason": f"system_error: {str(e)}"
    }
```

## Testing

### Unit Test Example

```python
def test_capacity_decline_escalation():
    willow = WillowIntegratedCore(test_config)
    
    # Simulate severe capacity decline
    result = willow.process_message(
        "test_user",
        "can't anymore",
        {"arousal": 7, "capacity": 1.5}
    )
    
    assert result["action"] == "escalate_to_human"
    assert "exhaustion" in result["reason"]
```

### Integration Test Example

```python
def test_bilingual_crisis_flow():
    willow = WillowIntegratedCore(test_config)
    
    # English start
    r1 = willow.process_message(
        "test_user",
        "Emergency help needed!",
        {"arousal": 9, "capacity": 5}
    )
    assert r1["action"] == "continue"
    
    # Spanish switch
    r2 = willow.process_message(
        "test_user", 
        "No puedo más!",
        {"arousal": 9.5, "capacity": 4}
    )
    
    # Should detect and acknowledge
    assert "Spanish" in r2["response"] or "español" in r2["response"]
```

## Performance Optimization

### Caching Strategy

```python
from functools import lru_cache

class OptimizedWillow(WillowIntegratedCore):
    @lru_cache(maxsize=1000)
    def _detect_language_cached(self, message_hash):
        # Cache language detection for repeated phrases
        return self.bilingual_detector._detect_languages(message_hash)
```

### Async Processing

```python
import asyncio

async def process_message_async(willow, user_id, message, emotional_state):
    # Run subsystems in parallel where possible
    tasks = [
        asyncio.create_task(willow.check_capacity(user_id, emotional_state)),
        asyncio.create_task(willow.detect_language(message)),
        asyncio.create_task(willow.analyze_tier_state(user_id))
    ]
    
    capacity, language, tier = await asyncio.gather(*tasks)
    
    # Combine results
    return willow.generate_response(capacity, language, tier)
```

## Monitoring and Observability

### Logging Configuration

```python
import logging

# Configure Willow logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add structured logging
willow.enable_structured_logging({
    "log_escalations": True,
    "log_capacity_changes": True,
    "log_language_switches": True,
    "log_tier_transitions": True
})
```

### Metrics Collection

```python
# Prometheus-style metrics
from prometheus_client import Counter, Histogram, Gauge

escalation_counter = Counter('willow_escalations_total', 'Total escalations', ['reason'])
response_time = Histogram('willow_response_duration_seconds', 'Response time')
active_sessions = Gauge('willow_active_sessions', 'Currently active sessions')

# Wrap process_message
@response_time.time()
def monitored_process_message(willow, *args, **kwargs):
    result = willow.process_message(*args, **kwargs)
    
    if result["action"] == "escalate_to_human":
        escalation_counter.labels(reason=result["reason"]).inc()
        
    return result
```

## Security Considerations

### Input Sanitization

```python
import re

def sanitize_message(message):
    # Remove potential injection attempts
    message = re.sub(r'<[^>]+>', '', message)  # Strip HTML
    message = message[:1000]  # Limit length
    return message.strip()
```

### Session Security

```python
import hashlib
from datetime import datetime, timedelta

def generate_secure_session_id(user_id):
    # Create time-bound session IDs
    timestamp = datetime.now().isoformat()
    return hashlib.sha256(f"{user_id}:{timestamp}".encode()).hexdigest()

def validate_session_age(session):
    # Expire old sessions
    max_age = timedelta(hours=24)
    if datetime.now() - session.start_time > max_age:
        raise SessionExpiredError("Session too old")
```

## Deployment Checklist

- [ ] Configure appropriate symbol style for your user base
- [ ] Set escalation thresholds based on your support capacity
- [ ] Enable appropriate language support modules
- [ ] Configure logging and monitoring
- [ ] Set up error alerting
- [ ] Test escalation pathways with support team
- [ ] Verify HIPAA/privacy compliance if applicable
- [ ] Load test with expected concurrent users
- [ ] Document escalation procedures for support staff
- [ ] Create runbooks for common issues

## Troubleshooting

### Common Issues

1. **Symbols not displaying correctly**
   - Check client encoding (UTF-8 required)
   - Try "minimal" or "none" symbol styles

2. **Premature escalations**
   - Review and adjust capacity thresholds
   - Check arousal calculation logic
   - Verify language detection accuracy

3. **Tier progression stuck**
   - Check consent keyword detection
   - Verify capacity scoring
   - Review tier timeout settings

4. **Language detection errors**
   - Expand language marker dictionaries
   - Adjust detection thresholds
   - Consider adding language hint from user profile