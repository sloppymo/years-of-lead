#!/usr/bin/env python3
"""
Generate 100 expanded tenant scenarios with increased complexity
Focus on specialized requests, emotional support, personalization, and seasonal themes
"""

import json
import random
from datetime import datetime

# Specialized Installation/Modification Requests
SPECIALIZED_REQUESTS = [
    ("washer_dryer_install", "Can I install a washer and dryer in my unit?", 3.8, 7.6),
    ("satellite_dish", "I need to install a satellite dish for work", 4.2, 7.4),
    ("home_security", "Can I add my own security system?", 4.5, 7.2),
    ("smart_home_devices", "Want to install smart locks and thermostat", 3.5, 7.8),
    ("window_ac_unit", "Can I put in a window AC unit?", 4.3, 7.3),
    ("ceiling_fan_install", "I'd like to install ceiling fans in bedrooms", 3.7, 7.6),
    ("water_filter_system", "Can I add an under-sink water filter?", 3.4, 7.9),
    ("electric_car_charger", "Need to install EV charging in my spot", 4.6, 7.1),
    ("garden_balcony", "Can I create a small garden on my balcony?", 3.2, 8.0),
    ("soundproofing_add", "Want to add soundproofing to home office", 4.4, 7.2),
]

# Lost Items and Emergency Situations
LOST_AND_FOUND = [
    ("lost_pet_building", "My cat escaped and might be in the building!", 7.2, 5.4),
    ("lost_child_playground", "Can't find my child, last seen at playground", 8.5, 4.8),
    ("lost_wallet_gym", "Left my wallet in the gym yesterday", 5.0, 6.8),
    ("lost_medication", "Lost my prescription meds somewhere", 6.5, 5.8),
    ("lost_keys_trash", "Think I threw my keys in the trash chute", 5.8, 6.2),
    ("lost_package_stolen", "Package says delivered but it's not here", 5.2, 6.7),
    ("lost_bike_moved", "My bike isn't where I locked it", 5.5, 6.5),
    ("lost_parking_spot", "Someone else is using my assigned spot", 4.8, 7.0),
    ("lost_storage_access", "Can't find my storage unit key anywhere", 4.3, 7.3),
    ("lost_mail_key", "Mailbox key broke off in the lock", 4.6, 7.1),
]

# Event Booking and Community Spaces
EVENT_REQUESTS = [
    ("rooftop_birthday", "How can I book the rooftop for a 30th birthday?", 3.2, 8.0),
    ("pool_party_kids", "Can I reserve the pool area for kids party?", 3.5, 7.8),
    ("gym_personal_trainer", "Can my personal trainer come to the gym?", 3.3, 7.9),
    ("courtyard_wedding", "Is it possible to have small wedding in courtyard?", 3.8, 7.6),
    ("conference_room_work", "Need conference room for client meetings", 3.6, 7.7),
    ("bbq_area_reunion", "Want to book BBQ area for family reunion", 3.4, 7.9),
    ("lobby_art_display", "Can I display my art in the lobby?", 3.3, 7.9),
    ("parking_food_truck", "Can we have a food truck event?", 3.7, 7.6),
    ("community_yoga", "Want to start morning yoga in the garden", 3.2, 8.0),
    ("movie_night_setup", "Can we do outdoor movie night on lawn?", 3.4, 7.9),
]

# Tenant Disputes and Interpersonal Issues
DISPUTE_SCENARIOS = [
    ("parking_confrontation", "Neighbor threatened me over parking dispute", 6.8, 5.6),
    ("noise_retaliation", "Upstairs neighbor making noise on purpose now", 6.2, 5.9),
    ("pet_complaints_false", "Neighbor keeps making false complaints about my dog", 5.8, 6.2),
    ("shared_wall_argument", "Had argument with neighbor about TV volume", 5.5, 6.5),
    ("hallway_belongings", "Neighbor leaves stuff in hallway, blocking path", 5.0, 6.8),
    ("cooking_smells_complaint", "Multiple complaints about my cooking smells", 5.3, 6.6),
    ("children_playing_dispute", "Neighbors complaining about kids playing", 5.7, 6.3),
    ("smoking_accusations", "Being accused of smoking but I don't smoke", 5.9, 6.1),
    ("laundry_room_conflict", "Someone keeps removing my laundry", 5.4, 6.6),
    ("gossip_harassment", "Neighbors spreading rumors about me", 6.3, 5.8),
]

# Seasonal and Holiday Concerns
SEASONAL_REQUESTS = [
    ("holiday_decorations", "How early can I put up Christmas decorations?", 3.0, 8.2),
    ("halloween_safety", "Planning trick-or-treat route for building kids", 3.2, 8.0),
    ("summer_ac_rules", "AC not keeping up with heat wave", 5.2, 6.7),
    ("winter_heating_cost", "Heating bill tripled this winter, is that normal?", 5.5, 6.5),
    ("spring_allergies", "Can we change HVAC filters for allergy season?", 4.2, 7.4),
    ("fall_leaves_hazard", "Wet leaves making entrance slippery", 4.8, 7.0),
    ("nye_party_rules", "What are the rules for New Year's Eve parties?", 3.4, 7.9),
    ("thanksgiving_guests", "Can family stay for Thanksgiving week?", 3.3, 7.9),
    ("summer_pool_hours", "Why does pool close so early in summer?", 4.0, 7.5),
    ("winter_package_theft", "Holiday packages keep disappearing", 5.6, 6.4),
]

# Personalized Tenant History References
PERSONALIZED_INTERACTIONS = [
    ("repeat_maintenance", "This is the third time my disposal has broken", 5.8, 6.2),
    ("package_frequency", "I get lots of packages, need better system", 4.2, 7.4),
    ("work_from_home_needs", "Since I'm always home, noise is bigger issue now", 5.0, 6.8),
    ("elderly_parent_visits", "My mom visits monthly, she needs accessibility", 4.5, 7.2),
    ("pet_history", "You approved my cat, can I get a second one?", 3.5, 7.8),
    ("payment_history_good", "I've paid on time for 3 years, can I get upgrade?", 3.8, 7.6),
    ("previous_complaint", "Remember my mold issue? It might be back", 5.5, 6.5),
    ("long_term_tenant", "Been here 5 years, never had this problem before", 4.8, 7.0),
    ("recent_life_change", "Since my surgery, need grab bars we discussed", 4.3, 7.3),
    ("past_resolution", "The solution you gave last time worked great!", 3.0, 8.2),
]

# Community Engagement and Local Resources
COMMUNITY_RESOURCES = [
    ("farmers_market", "Is there a farmers market nearby?", 2.8, 8.4),
    ("pet_services", "Any recommended pet sitters in building?", 3.2, 8.0),
    ("childcare_options", "Do other parents here use any daycares?", 3.5, 7.8),
    ("recycling_program", "How can I help improve our recycling?", 3.0, 8.2),
    ("community_garden", "Can we start a community garden?", 3.3, 7.9),
    ("local_events", "Any building events for meeting neighbors?", 3.1, 8.1),
    ("green_initiatives", "What eco-friendly programs do we have?", 3.2, 8.0),
    ("volunteer_opportunities", "Ways to help elderly neighbors?", 2.9, 8.3),
    ("fitness_groups", "Any running groups in the building?", 3.0, 8.2),
    ("book_club", "Is there a building book club?", 2.8, 8.4),
]

# Complex Maintenance with Emotional Context
EMOTIONAL_MAINTENANCE = [
    ("nursery_safety", "Baby coming, need to childproof everything", 4.5, 7.2),
    ("medical_equipment_power", "Life support equipment needs reliable power", 6.5, 5.8),
    ("depression_mess", "Depression got bad, apartment needs deep clean", 5.8, 6.2),
    ("divorce_locks", "Going through divorce, need locks changed ASAP", 6.2, 5.9),
    ("death_family", "Family member passed, need to break lease", 6.8, 5.6),
    ("job_loss_rent", "Lost my job, need to discuss rent options", 7.0, 5.5),
    ("disability_new", "New disability diagnosis, need accommodations", 5.5, 6.5),
    ("anxiety_repairs", "Repair people in my space triggers anxiety", 5.3, 6.6),
    ("ptsd_fireworks", "Fireworks trigger my PTSD, what can we do?", 6.0, 6.0),
    ("addiction_recovery", "In recovery, need to avoid certain neighbors", 5.7, 6.3),
]

# Technology and Modern Living Issues
TECH_MODERN_ISSUES = [
    ("internet_wfh", "Internet too slow for video calls", 4.8, 7.0),
    ("smart_home_interference", "Smart devices interfering with neighbors", 4.2, 7.4),
    ("delivery_drone", "Can delivery drones come to my balcony?", 3.5, 7.8),
    ("crypto_mining", "Tenant mining crypto, huge electric bill", 5.5, 6.5),
    ("streaming_bandwidth", "Too many people streaming, buffering issues", 4.6, 7.1),
    ("zoom_background", "Need better lighting for video calls", 3.8, 7.6),
    ("ring_doorbell", "Can I install a Ring doorbell?", 3.6, 7.7),
    ("mesh_network", "Want to set up mesh network for whole unit", 3.7, 7.6),
    ("electric_bike_storage", "Where to charge my e-bike safely?", 4.0, 7.5),
    ("vr_space_needed", "Need more space for VR gaming", 3.4, 7.9),
]

# Cultural and Dietary Accommodations
CULTURAL_CONSIDERATIONS = [
    ("kosher_kitchen", "Need separate fridges for kosher kitchen", 4.2, 7.4),
    ("prayer_times_quiet", "Need quiet during daily prayer times", 4.5, 7.2),
    ("cultural_cooking", "Neighbors complain about curry smells", 5.3, 6.6),
    ("religious_mezuzah", "Can I put mezuzah on doorframe?", 3.3, 7.9),
    ("ramadan_noise", "Preparing pre-dawn meals, worried about noise", 4.0, 7.5),
    ("diwali_candles", "Want to light diyas for Diwali safely", 3.8, 7.6),
    ("lunar_new_year", "Can we have firecracker ceremony?", 4.3, 7.3),
    ("meditation_space", "Need quiet space for daily meditation", 3.9, 7.5),
    ("dietary_disposal", "Disposal can't handle my vegetarian cooking", 4.1, 7.4),
    ("incense_complaints", "Incense for prayers bothering neighbors", 4.7, 7.0),
]

def generate_expanded_scenario(entry_id: str, scenario_data: tuple, category: str) -> dict:
    """Generate an expanded scenario with complex emotional and practical elements"""
    scenario_name, issue, initial_arousal, initial_capacity = scenario_data
    
    messages = []
    
    # Initial tenant message
    messages.append({
        "role": "tenant",
        "content": issue,
        "arousal": initial_arousal,
        "capacity": initial_capacity
    })
    
    # Generate contextual response based on category
    if category == "specialized":
        acknowledgment = get_specialized_acknowledgment(scenario_name)
        solution = get_specialized_solution(scenario_name)
        challenges = get_installation_challenges(scenario_name)
        response = f"{acknowledgment} {solution} {challenges}"
        technique = "comprehensive_guidance"
        
    elif category == "lost":
        acknowledgment = get_emergency_acknowledgment(initial_arousal)
        immediate_action = get_lost_item_action(scenario_name)
        support = get_emotional_support(scenario_name)
        response = f"{acknowledgment} {immediate_action} {support}"
        technique = "crisis_support"
        
    elif category == "event":
        acknowledgment = "I'd be happy to help you plan this special event!"
        process = get_event_process(scenario_name)
        tips = get_event_tips(scenario_name)
        response = f"{acknowledgment} {process} {tips}"
        technique = "event_coordination"
        
    elif category == "dispute":
        acknowledgment = "I understand how stressful neighbor conflicts can be."
        validation = "Your feelings about this situation are completely valid."
        action = get_dispute_resolution(scenario_name)
        response = f"{acknowledgment} {validation} {action}"
        technique = "conflict_mediation"
        
    elif category == "seasonal":
        acknowledgment = get_seasonal_acknowledgment(scenario_name)
        solution = get_seasonal_solution(scenario_name)
        community = get_seasonal_community_note(scenario_name)
        response = f"{acknowledgment} {solution} {community}"
        technique = "seasonal_support"
        
    elif category == "personalized":
        acknowledgment = get_personalized_acknowledgment(scenario_name)
        history_reference = get_history_reference(scenario_name)
        solution = get_personalized_solution(scenario_name)
        response = f"{acknowledgment} {history_reference} {solution}"
        technique = "relationship_building"
        
    elif category == "community":
        acknowledgment = "I love that you're interested in connecting with our community!"
        resources = get_community_resources(scenario_name)
        encouragement = "Building connections makes our community stronger."
        response = f"{acknowledgment} {resources} {encouragement}"
        technique = "community_building"
        
    elif category == "emotional":
        acknowledgment = get_compassionate_acknowledgment(scenario_name)
        validation = "What you're going through is really challenging."
        support = get_emotional_maintenance_support(scenario_name)
        response = f"{acknowledgment} {validation} {support}"
        technique = "trauma_informed_support"
        
    elif category == "tech":
        acknowledgment = "Modern living definitely comes with unique challenges!"
        solution = get_tech_solution(scenario_name)
        consideration = get_tech_consideration(scenario_name)
        response = f"{acknowledgment} {solution} {consideration}"
        technique = "tech_support"
        
    else:  # cultural
        acknowledgment = "I appreciate you sharing your cultural needs with me."
        validation = "Your traditions and practices are important."
        accommodation = get_cultural_accommodation(scenario_name)
        response = f"{acknowledgment} {validation} {accommodation}"
        technique = "cultural_sensitivity"
    
    # Calculate arousal impact based on response quality
    if initial_arousal >= 7.0:
        arousal_impact = -1.5
    elif initial_arousal >= 5.5:
        arousal_impact = -1.2
    elif initial_arousal >= 4.0:
        arousal_impact = -0.8
    else:
        arousal_impact = -0.5
    
    messages.append({
        "role": "willow",
        "content": response,
        "tier": "tier_1",
        "technique": technique,
        "arousal_impact": arousal_impact
    })
    
    # Add follow-up interaction (80% of time)
    if random.random() < 0.8:
        new_arousal = max(2.0, initial_arousal + arousal_impact)
        new_capacity = min(9.0, initial_capacity + 0.5)
        
        # Category-specific follow-ups
        if category in ["emotional", "dispute", "lost"]:
            follow_ups = [
                "Thank you for being so understanding",
                "I really appreciate your support",
                "This means a lot to me",
                "You're the first person to really listen",
                "I feel heard for the first time",
                "Thank you for not judging me"
            ]
        else:
            follow_ups = [
                "This is exactly what I needed to know",
                "You've been incredibly helpful",
                "I appreciate the detailed information",
                "Perfect, I'll get started on that",
                "Thanks for thinking of everything",
                "You make living here so much easier"
            ]
        
        messages.append({
            "role": "tenant",
            "content": random.choice(follow_ups),
            "arousal": new_arousal,
            "capacity": new_capacity
        })
        
        # Tier 2 response with additional support
        tier2_response = get_tier2_response(category, scenario_name)
        
        messages.append({
            "role": "willow",
            "content": tier2_response,
            "tier": "tier_2",
            "technique": "reinforcement_support",
            "arousal_impact": -0.3
        })
    
    # Build comprehensive metrics
    arousal_curve = [initial_arousal]
    capacity_curve = [initial_capacity]
    
    current_arousal = initial_arousal
    current_capacity = initial_capacity
    
    for msg in messages[1:]:
        if msg['role'] == 'willow' and 'arousal_impact' in msg:
            current_arousal = max(2.0, current_arousal + msg['arousal_impact'])
            current_capacity = min(9.0, current_capacity + 0.3)
        elif msg['role'] == 'tenant' and 'arousal' in msg:
            current_arousal = msg['arousal']
            current_capacity = msg.get('capacity', current_capacity)
        
        arousal_curve.append(current_arousal)
        capacity_curve.append(current_capacity)
    
    # Determine containment quality
    arousal_reduction = initial_arousal - current_arousal
    if arousal_reduction >= 2.0:
        containment_quality = "excellent"
    elif arousal_reduction >= 1.0:
        containment_quality = "good"
    else:
        containment_quality = "adequate"
    
    return {
        "id": entry_id,
        "scenario": scenario_name,
        "category": category,
        "complexity_level": "high",
        "initial_state": {
            "arousal": initial_arousal,
            "capacity": initial_capacity,
            "issue_type": category
        },
        "messages": messages,
        "process_metrics": {
            "tier_progression": ["tier_1"] if len(messages) == 2 else ["tier_1", "tier_2"],
            "arousal_curve": arousal_curve,
            "capacity_curve": capacity_curve,
            "containment_quality": containment_quality,
            "personalization_used": category == "personalized",
            "cultural_sensitivity": category == "cultural",
            "community_building": category == "community"
        }
    }

# Helper functions for generating contextual responses
def get_specialized_acknowledgment(scenario: str) -> str:
    acknowledgments = {
        "washer_dryer_install": "Installing a washer/dryer can really improve quality of life!",
        "satellite_dish": "I understand how important reliable connectivity is for work.",
        "home_security": "Your safety and peace of mind are definitely priorities.",
        "smart_home_devices": "Smart home technology can make life so much more convenient!",
        "window_ac_unit": "Additional cooling can make such a difference in comfort.",
        "ceiling_fan_install": "Ceiling fans are great for both comfort and energy efficiency!",
        "water_filter_system": "Clean, filtered water is definitely important for health.",
        "electric_car_charger": "Supporting sustainable transportation is wonderful!",
        "garden_balcony": "A balcony garden can really make your space feel like home.",
        "soundproofing_add": "A quiet workspace is essential for productivity."
    }
    return acknowledgments.get(scenario, "I understand this is important to you.")

def get_specialized_solution(scenario: str) -> str:
    solutions = {
        "washer_dryer_install": "You'll need to submit a modification request form, and we'll need to verify the plumbing and electrical capacity.",
        "satellite_dish": "We have designated areas for satellite installation that don't damage the building.",
        "home_security": "You can install wireless systems, but hardwired systems need approval.",
        "smart_home_devices": "Smart devices are generally fine, but we'll need to ensure compatibility with our systems.",
        "window_ac_unit": "Window units are allowed in buildings without central air, with some safety requirements.",
        "ceiling_fan_install": "We can have our approved electricians install ceiling fans to ensure safety.",
        "water_filter_system": "Under-sink filters are typically approved with proper installation.",
        "electric_car_charger": "We're actually planning EV charging stations - let me add you to the interest list!",
        "garden_balcony": "Balcony gardens are encouraged! Just ensure proper drainage and weight limits.",
        "soundproofing_add": "We can recommend approved soundproofing solutions that won't damage walls."
    }
    return solutions.get(scenario, "Let me check our modification policies for you.")

def get_installation_challenges(scenario: str) -> str:
    challenges = {
        "washer_dryer_install": "Keep in mind there's a $500 installation fee, and it may affect your rent slightly due to increased utility usage.",
        "satellite_dish": "Installation must be done by our approved vendors to maintain the building warranty.",
        "home_security": "Remember that any cameras must not point at neighbors' windows or common areas.",
        "smart_home_devices": "Just note that you'll need to reset everything to default when you move out.",
        "window_ac_unit": "You'll need to sign a liability waiver and ensure proper support brackets.",
        "ceiling_fan_install": "The installation cost is typically $200-300 per fan including labor.",
        "water_filter_system": "Annual filter replacements will be your responsibility to maintain.",
        "electric_car_charger": "There's a monthly fee for dedicated charging spots once installed.",
        "garden_balcony": "Please use lightweight pots and ensure no water drips to balconies below.",
        "soundproofing_add": "Professional installation typically runs $500-1000 per room."
    }
    return challenges.get(scenario, "I'll send you complete details about the process and any associated costs.")

def get_emergency_acknowledgment(arousal: float) -> str:
    if arousal >= 8.0:
        return "Oh no, I can hear how distressing this is! Let's act quickly."
    elif arousal >= 7.0:
        return "I understand this is really urgent and stressful for you."
    elif arousal >= 6.0:
        return "This must be so worrying! Let me help you right away."
    else:
        return "I know how concerning it is to lose something important."

def get_lost_item_action(scenario: str) -> str:
    actions = {
        "lost_pet_building": "I'm immediately alerting all staff to look for your cat. Can you send me a photo? I'll also post in our building's emergency channel.",
        "lost_child_playground": "I'm calling security RIGHT NOW to check all areas. Please go to the playground while I coordinate the search.",
        "lost_wallet_gym": "I'll have maintenance check the gym immediately and review security footage from yesterday.",
        "lost_medication": "This is urgent - I'll have staff check all common areas. Do you need help getting an emergency refill?",
        "lost_keys_trash": "I'll have maintenance check before the trash pickup! In the meantime, I can get you emergency locksmith access.",
        "lost_package_stolen": "I'll check with our mail room and review lobby cameras. We take package theft very seriously.",
        "lost_bike_moved": "Security might have moved it if it was blocking access. I'll check our bike impound area.",
        "lost_parking_spot": "I'll have security check who's in your spot and get them to move immediately.",
        "lost_storage_access": "I can get maintenance to help you access your storage unit right away.",
        "lost_mail_key": "Maintenance can extract the broken key and get you a replacement today."
    }
    return actions.get(scenario, "I'll mobilize our team to help you search immediately.")

def get_emotional_support(scenario: str) -> str:
    support = {
        "lost_pet_building": "I know how much your cat means to you. We'll do everything possible to find them safely.",
        "lost_child_playground": "I'm a parent too - we'll find them. Children often just wander to interesting spots.",
        "lost_wallet_gym": "Losing a wallet is so stressful with all the cards and IDs. We'll do our best to recover it.",
        "lost_medication": "Your health is the priority here. Let's work on both finding and replacing if needed.",
        "lost_keys_trash": "What a frustrating situation! But don't worry, we've recovered items from trash before.",
        "lost_package_stolen": "It's so violating when packages disappear. We'll investigate thoroughly.",
        "lost_bike_moved": "Your bike is valuable both practically and personally. We'll track it down.",
        "lost_parking_spot": "It's frustrating when people don't respect assigned spaces. This will be resolved quickly.",
        "lost_storage_access": "I know you probably need something important from storage. We'll get you in there.",
        "lost_mail_key": "What an annoying situation! But this is actually pretty common and fixable."
    }
    return support.get(scenario, "I understand how stressful this is. We're here to help.")

def get_event_process(scenario: str) -> str:
    processes = {
        "rooftop_birthday": "You'll need to fill out an event form at least 2 weeks in advance. The rooftop can accommodate up to 50 people.",
        "pool_party_kids": "Pool parties need special insurance and a lifeguard for children's events. I can help arrange both!",
        "gym_personal_trainer": "Trainers need to provide proof of insurance and sign our vendor agreement. It's a simple process!",
        "courtyard_wedding": "Small weddings are allowed! You'll need event insurance and approval for any vendors.",
        "conference_room_work": "Our conference room is $50/hour for residents, with AV equipment included.",
        "bbq_area_reunion": "The BBQ area is free for residents! Just reserve it to ensure availability.",
        "lobby_art_display": "We love supporting resident artists! Let's discuss duration and installation needs.",
        "parking_food_truck": "Food trucks need permits and insurance, but we've hosted them before successfully!",
        "community_yoga": "Community-led activities are encouraged! We just need a liability waiver from participants.",
        "movie_night_setup": "Outdoor movies are fun! We have power outlets and can help with equipment setup."
    }
    return processes.get(scenario, "Let me get you the complete event planning guide.")

def get_event_tips(scenario: str) -> str:
    tips = {
        "rooftop_birthday": "Remember, if you exceed 50 guests, additional insurance is required. Also, music must end by 10 PM on weeknights.",
        "pool_party_kids": "Pro tip: Schedule for early afternoon when the pool is less crowded. We can provide extra chairs!",
        "gym_personal_trainer": "Many residents share trainers to split costs - I can connect you with others if interested!",
        "courtyard_wedding": "Consider having a backup plan for weather. We have a lovely indoor community room too!",
        "conference_room_work": "Book recurring slots for better rates. The morning light in there is perfect for video calls!",
        "bbq_area_reunion": "We have coolers and extra tables available for larger gatherings - just ask!",
        "lobby_art_display": "Past artists have had great success with opening receptions - we can help promote!",
        "parking_food_truck": "Friday evenings work best for food trucks - great community turnout!",
        "community_yoga": "Our garden has beautiful morning light - perfect for sunrise sessions!",
        "movie_night_setup": "We have a projector you can borrow! Family-friendly films get the best attendance."
    }
    return tips.get(scenario, "I'll share some tips from other successful events to help you plan!")

def get_dispute_resolution(scenario: str) -> str:
    resolutions = {
        "parking_confrontation": "Threats are never acceptable. I'm documenting this and will speak with that resident immediately. If you feel unsafe, we can also involve security.",
        "noise_retaliation": "Retaliation is against our community rules. I'll address this formally and mediate a solution that works for everyone.",
        "pet_complaints_false": "I'll review the actual pet policies with your neighbor and clarify that false complaints are not acceptable.",
        "shared_wall_argument": "Let's set up a mediation meeting. Sometimes neighbors just need help finding compromise on reasonable hours.",
        "hallway_belongings": "I'll send a reminder about fire code requirements and speak directly with that resident about keeping hallways clear.",
        "cooking_smells_complaint": "Cooking smells are part of apartment living. I'll remind everyone about being respectful of cultural differences.",
        "children_playing_dispute": "Children have a right to play during reasonable hours. Let's find a balance that respects everyone's needs.",
        "smoking_accusations": "False accusations are serious. I'll investigate and clear this up, ensuring your reputation isn't unfairly damaged.",
        "laundry_room_conflict": "I'll review the laundry room footage and post clearer guidelines about respecting others' laundry time.",
        "gossip_harassment": "Harassment through gossip is still harassment. I'll address this formally and ensure it stops."
    }
    return resolutions.get(scenario, "I'll mediate this situation professionally and ensure both parties are heard.")

def get_seasonal_acknowledgment(scenario: str) -> str:
    acknowledgments = {
        "holiday_decorations": "The holidays are such a special time to make your space festive!",
        "halloween_safety": "How wonderful that you're organizing trick-or-treating for the building kids!",
        "summer_ac_rules": "Heat waves are really challenging, especially in older buildings.",
        "winter_heating_cost": "Heating costs can be shocking in extreme weather!",
        "spring_allergies": "Allergy season is really tough for so many residents.",
        "fall_leaves_hazard": "Safety during fall weather is definitely a concern.",
        "nye_party_rules": "New Year's Eve is such a special celebration!",
        "thanksgiving_guests": "Family gatherings during Thanksgiving are so important.",
        "summer_pool_hours": "I understand wanting to enjoy the pool during long summer evenings!",
        "winter_package_theft": "Holiday package theft is unfortunately more common."
    }
    return acknowledgments.get(scenario, "Seasonal considerations are important for community comfort!")

def get_seasonal_solution(scenario: str) -> str:
    solutions = {
        "holiday_decorations": "Decorations can go up after Thanksgiving. Just avoid damaging walls or blocking exits.",
        "halloween_safety": "I'll help create a building map showing participating units and ensure common areas are well-lit!",
        "summer_ac_rules": "I'll have maintenance check your AC unit immediately and provide tips for keeping cool efficiently.",
        "winter_heating_cost": "Let's review your unit's insulation and weather stripping - small fixes can save significant money.",
        "spring_allergies": "We actually change to HEPA filters during allergy season - I'll expedite yours!",
        "fall_leaves_hazard": "I'll have maintenance increase leaf clearing frequency and add extra mats at entrances.",
        "nye_party_rules": "Parties are allowed with normal noise rules relaxed until 1 AM on New Year's Eve only.",
        "thanksgiving_guests": "Week-long guest stays are fine! Just register them at the office for parking and access.",
        "summer_pool_hours": "I'll bring up extended summer hours at our next community meeting - great suggestion!",
        "winter_package_theft": "We're implementing a secure package system and increasing lobby monitoring during holidays."
    }
    return solutions.get(scenario, "Let me provide specific seasonal guidelines and support.")

def get_seasonal_community_note(scenario: str) -> str:
    notes = {
        "holiday_decorations": "We actually have a decoration contest with prizes - you should enter!",
        "halloween_safety": "Last year's building trick-or-treat was a huge hit. Your organization will make it even better!",
        "summer_ac_rules": "We're also setting up a cooling center in the community room during heat waves.",
        "winter_heating_cost": "We have a resident support fund if heating costs become unmanageable - just let me know.",
        "spring_allergies": "Several residents have started an allergy support group - interested in joining?",
        "fall_leaves_hazard": "Thanks for looking out for everyone's safety - this is what makes our community special.",
        "nye_party_rules": "Many residents host open-door parties - it's become a lovely building tradition!",
        "thanksgiving_guests": "Our community room is available if you need extra space for dinner!",
        "summer_pool_hours": "We're considering adult swim hours in the evening - your input helps shape these decisions.",
        "winter_package_theft": "Neighbors are organizing a package watch system - community solutions work best!"
    }
    return notes.get(scenario, "Your input helps us improve seasonal services for everyone!")

def get_personalized_acknowledgment(scenario: str) -> str:
    acknowledgments = {
        "repeat_maintenance": "I see this is becoming a recurring issue - that must be so frustrating!",
        "package_frequency": "You do receive a lot of packages! Let's find a better solution for you.",
        "work_from_home_needs": "Your work-from-home needs have definitely evolved since you first moved in.",
        "elderly_parent_visits": "It's wonderful that your mom visits regularly - family is so important.",
        "pet_history": "Your first cat has been such a model resident!",
        "payment_history_good": "You've been an exemplary tenant - we really value residents like you.",
        "previous_complaint": "I remember how stressful the mold situation was for you last time.",
        "long_term_tenant": "Five years of great tenancy definitely gives weight to your concerns.",
        "recent_life_change": "I hope your recovery is going well - let's get those accommodations in place.",
        "past_resolution": "I'm so glad our previous solution worked! Let's build on that success."
    }
    return acknowledgments.get(scenario, "I appreciate your continued communication with us.")

def get_history_reference(scenario: str) -> str:
    references = {
        "repeat_maintenance": "Looking at your history, the disposal has failed in January, March, and now May.",
        "package_frequency": "Your package volume has increased 300% since you started your business!",
        "work_from_home_needs": "I see you've been with us since before remote work became so common.",
        "elderly_parent_visits": "I have notes about the shower grab bar we installed for her last year.",
        "pet_history": "Fluffy has been with us for two years now without a single complaint!",
        "payment_history_good": "36 consecutive on-time payments is remarkable - thank you for that.",
        "previous_complaint": "The mold remediation was completed in March with a guarantee.",
        "long_term_tenant": "You've seen this building through many changes and improvements.",
        "recent_life_change": "I have your occupational therapist's recommendations from last month.",
        "past_resolution": "The soundproofing panels we installed seemed to solve the noise issue perfectly."
    }
    return references.get(scenario, "Your history with us helps me understand your needs better.")

def get_personalized_solution(scenario: str) -> str:
    solutions = {
        "repeat_maintenance": "This pattern suggests we need to replace the entire unit, not just repair it. I'll authorize a full replacement.",
        "package_frequency": "Let's set up a dedicated package solution - maybe a larger lockbox or daily delivery notification system.",
        "work_from_home_needs": "I can prioritize your unit for our upcoming soundproofing improvements and ensure quiet hours are enforced.",
        "elderly_parent_visits": "Let's install those additional grab bars before her next visit. I'll also reserve close parking for her.",
        "pet_history": "Based on Fluffy's good behavior, I'm pre-approving your second cat. Just bring vaccination records!",
        "payment_history_good": "I'm checking what upgrades we can offer - perhaps the renovated unit on the third floor?",
        "previous_complaint": "I'll have our mold specialist do a thorough re-inspection immediately, at no charge to you.",
        "long_term_tenant": "Your loyalty deserves priority service. I'm escalating this to get immediate resolution.",
        "recent_life_change": "I'll fast-track the grab bar installation and see what other accommodations might help.",
        "past_resolution": "Let's apply the same successful approach to any other rooms where you need it!"
    }
    return solutions.get(scenario, "Your history with us allows me to provide more tailored solutions.")

def get_community_resources(scenario: str) -> str:
    resources = {
        "farmers_market": "There's a great farmers market two blocks away every Saturday! Plus, some residents organize group trips.",
        "pet_services": "We have a building pet-sitter list! Also, Dr. Smith in 4B is a retired vet who helps in emergencies.",
        "childcare_options": "Several parents here use Bright Starts Daycare. There's also a nanny-share board in the mail room!",
        "recycling_program": "Join our Green Team! They meet monthly and have already improved our recycling rate by 40%.",
        "community_garden": "Perfect timing! We're actually converting part of the courtyard to raised beds next month.",
        "local_events": "We have monthly coffee mornings and seasonal parties. The next one is this Saturday!",
        "green_initiatives": "We have composting, energy challenges, and a new solar panel project you could join!",
        "volunteer_opportunities": "Our Senior Support Network helps with groceries and appointments. They'd love more volunteers!",
        "fitness_groups": "Yes! The 'Building Runners' meet every Tuesday and Thursday at 6 AM by the lobby.",
        "book_club": "The 'Literary Neighbors' meet monthly in the community room. They're reading Beloved this month!"
    }
    return resources.get(scenario, "We have several community groups that might interest you!")

def get_compassionate_acknowledgment(scenario: str) -> str:
    acknowledgments = {
        "nursery_safety": "Preparing for a baby is such an exciting but overwhelming time!",
        "medical_equipment_power": "I understand how critical reliable power is for medical equipment.",
        "depression_mess": "Thank you for trusting me with this. Depression can make everything feel impossible.",
        "divorce_locks": "I'm so sorry you're going through this difficult time.",
        "death_family": "I'm deeply sorry for your loss. Please don't worry about the lease right now.",
        "job_loss_rent": "Job loss is incredibly stressful. Let's work together on this.",
        "disability_new": "Adjusting to a new disability is a major life change.",
        "anxiety_repairs": "I completely understand how having strangers in your space can trigger anxiety.",
        "ptsd_fireworks": "PTSD triggers are serious, and you deserve to feel safe in your home.",
        "addiction_recovery": "Your recovery is important, and we want to support your success."
    }
    return acknowledgments.get(scenario, "I hear you and understand this is really difficult.")

def get_emotional_maintenance_support(scenario: str) -> str:
    support = {
        "nursery_safety": "We'll do a full safety inspection and install outlet covers, cabinet locks, and ensure windows are secure. Congratulations on your growing family!",
        "medical_equipment_power": "I'm marking your unit as medical priority for power restoration. We'll also install a backup power notification system.",
        "depression_mess": "We can arrange a compassionate cleaning service that specializes in these situations. No judgment, just help getting back on track.",
        "divorce_locks": "I'll have the locks changed within 24 hours and ensure your ex is removed from all access lists. Your safety is paramount.",
        "death_family": "We offer a 30-day grace period for these situations. Take the time you need, and we'll work out the details when you're ready.",
        "job_loss_rent": "We have payment plan options and can connect you with local assistance programs. You won't face eviction while we work this out.",
        "disability_new": "Let's schedule a full accessibility assessment. We can install ramps, grab bars, and any other modifications you need.",
        "anxiety_repairs": "We can schedule repairs when you're out, or have the same trusted technician each time. You can also have a friend present.",
        "ptsd_fireworks": "I'll notify you in advance of any planned fireworks and advocate for quieter celebrations. We can also explore soundproofing options.",
        "addiction_recovery": "I can arrange different routes to avoid triggering neighbors and ensure maintenance respects your privacy and recovery space."
    }
    return support.get(scenario, "We'll work together to find solutions that support your wellbeing.")

def get_tech_solution(scenario: str) -> str:
    solutions = {
        "internet_wfh": "Let me contact our ISP about dedicated bandwidth for work-from-home residents. We can also check your router placement.",
        "smart_home_interference": "We need to ensure your devices are on the correct frequency to avoid interference. I'll send our tech specialist.",
        "delivery_drone": "Drone deliveries are allowed to designated areas only. Let me add your balcony to the approved list!",
        "crypto_mining": "Mining operations require separate utility metering due to high power usage. Let's discuss the proper setup.",
        "streaming_bandwidth": "We're actually upgrading to fiber next month! In the meantime, I can help optimize your connection.",
        "zoom_background": "I can have maintenance install better lighting fixtures. Good lighting makes such a difference for video calls!",
        "ring_doorbell": "Video doorbells are allowed! Just ensure they only capture your doorway, not the hallway or neighbors' doors.",
        "mesh_network": "Mesh networks are great for coverage! Just use a unique network name to avoid confusion with building WiFi.",
        "electric_bike_storage": "We have designated e-bike charging stations in the bike room with proper ventilation and fire safety.",
        "vr_space_needed": "Have you considered the amenity room for VR gaming? We can reserve time slots for space-intensive activities!"
    }
    return solutions.get(scenario, "Let's find a tech solution that works for everyone in the building.")

def get_tech_consideration(scenario: str) -> str:
    considerations = {
        "internet_wfh": "Many residents are in the same situation - we're advocating for business-class internet options.",
        "smart_home_interference": "Smart home tech is the future - we just need to manage it properly for apartment living.",
        "delivery_drone": "We're one of the first buildings to allow drone delivery - exciting times!",
        "crypto_mining": "We support innovation but need to balance it with fair utility usage for all residents.",
        "streaming_bandwidth": "The pandemic really changed our bandwidth needs - we're adapting our infrastructure.",
        "zoom_background": "So many residents need good video call setups now - it's the new normal!",
        "ring_doorbell": "Security tech helps everyone feel safer when used respectfully.",
        "mesh_network": "Better WiFi coverage benefits everyone - thanks for leading the way!",
        "electric_bike_storage": "E-bikes are becoming so popular - we're expanding charging capacity.",
        "vr_space_needed": "VR is amazing! We're considering a dedicated VR/gaming room in our renovation plans."
    }
    return considerations.get(scenario, "Technology is changing how we live, and we want to support that!")

def get_cultural_accommodation(scenario: str) -> str:
    accommodations = {
        "kosher_kitchen": "We can absolutely work with you on kitchen modifications for kosher requirements. Many residents have similar needs.",
        "prayer_times_quiet": "I'll note your prayer times and ensure maintenance doesn't schedule work during those hours in nearby units.",
        "cultural_cooking": "Cooking aromas are part of diverse community living. I'll remind everyone about cultural respect and acceptance.",
        "religious_mezuzah": "Of course! Mezuzahs and other religious items on doorframes are protected under fair housing laws.",
        "ramadan_noise": "I'll send a building notice about Ramadan so neighbors understand the early morning activity. Community education helps!",
        "diwali_candles": "Let's ensure you can celebrate safely! Battery-operated diyas are a great option, or we can discuss supervised candle use.",
        "lunar_new_year": "We love cultural celebrations! Let's plan a safe firecracker ceremony in the parking lot for all to enjoy.",
        "meditation_space": "Our quiet room is perfect for meditation. I can also ensure your apartment hours are respected for practice.",
        "dietary_disposal": "High-fiber vegetarian diets can be tough on disposals. Let me get you a composting solution that works better!",
        "incense_complaints": "Incense for religious purposes is protected. I'll educate neighbors while we explore ventilation improvements."
    }
    return accommodations.get(scenario, "We celebrate diversity and will accommodate your cultural needs respectfully.")

def get_tier2_response(category: str, scenario: str) -> str:
    """Generate contextual tier 2 responses based on category"""
    if category == "emotional":
        return "Please remember you're not alone in this. We're here to support you through this challenging time, and there's no rush on any decisions. Take care of yourself first."
    elif category == "dispute":
        return "I'll follow up with you after speaking with the other party. Your wellbeing and peaceful enjoyment of your home are my priorities. We'll find a resolution that works."
    elif category == "lost":
        return "I'll keep you updated every hour until we resolve this. If we can't find it, I'll help you with replacement options. Try not to worry - we've got this handled."
    elif category == "personalized":
        return "Your long-term residency really matters to us. I'll personally oversee this to ensure it's handled properly. Thank you for your patience and loyalty."
    elif category == "community":
        return "I love seeing residents connect with each other! Let me know how the group goes - we might be able to provide space or resources to help it grow."
    elif category == "seasonal":
        return "Seasonal changes definitely affect quality of life. I'll make sure your concerns are addressed before the weather gets more extreme. We're in this together!"
    elif category == "cultural":
        return "Thank you for helping us be a more inclusive community. Your cultural practices enrich our building's diversity. Let me know if you need any other accommodations."
    elif category == "tech":
        return "The future of apartment living includes all this technology! Thanks for your patience as we adapt our infrastructure. You're helping us improve for everyone."
    elif category == "specialized":
        return "I'll send you a complete information packet with all the details, costs, and timelines. Feel free to ask any questions - we want to make this work for you!"
    else:
        return "I'll personally monitor this situation to ensure everything goes smoothly. Your satisfaction and comfort in your home are what matter most to us."

def main():
    """Generate 100 expanded tenant scenarios"""
    all_scenarios = []
    
    # Combine all categories
    scenarios_by_category = [
        ("specialized", SPECIALIZED_REQUESTS),
        ("lost", LOST_AND_FOUND),
        ("event", EVENT_REQUESTS),
        ("dispute", DISPUTE_SCENARIOS),
        ("seasonal", SEASONAL_REQUESTS),
        ("personalized", PERSONALIZED_INTERACTIONS),
        ("community", COMMUNITY_RESOURCES),
        ("emotional", EMOTIONAL_MAINTENANCE),
        ("tech", TECH_MODERN_ISSUES),
        ("cultural", CULTURAL_CONSIDERATIONS)
    ]
    
    # Generate entries
    entry_num = 201  # Starting from WILLOW_201
    
    # Generate 10 from each category
    for category, scenarios in scenarios_by_category:
        for scenario in scenarios:
            entry_id = f"WILLOW_{entry_num}"
            entry = generate_expanded_scenario(entry_id, scenario, category)
            all_scenarios.append(entry)
            entry_num += 1
            
            if entry_num > 300:  # Stop at 100 entries
                break
        if entry_num > 300:
            break
    
    # Write to file
    with open('willow_expanded_scenarios_100.jsonl', 'w') as f:
        for entry in all_scenarios:
            f.write(json.dumps(entry) + '\n')
    
    # Print summary statistics
    print(f"Generated {len(all_scenarios)} expanded tenant scenarios")
    print("\nCategory distribution:")
    category_counts = {}
    for entry in all_scenarios:
        cat = entry['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat.capitalize()}: {count}")
    
    print("\nComplexity features:")
    print("  - Specialized installation requests with cost/process details")
    print("  - Emergency lost item scenarios with immediate action plans")
    print("  - Event planning with tips and community building")
    print("  - Dispute resolution with mediation approaches")
    print("  - Seasonal considerations with community notes")
    print("  - Personalized responses referencing tenant history")
    print("  - Community resource connections")
    print("  - Emotional support for life challenges")
    print("  - Modern technology accommodations")
    print("  - Cultural sensitivity and accommodations")
    
    print(f"\nSaved to: willow_expanded_scenarios_100.jsonl")

if __name__ == "__main__":
    main()