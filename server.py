"""
Pet Care AI MCP Server - Pet Management Intelligence
Built by MEOK AI Labs | https://meok.ai

Feeding schedules, vaccination tracking, breed identification,
health symptom checking, and training recommendations.
"""

import time
from datetime import datetime, timezone, timedelta
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "pet-care-ai",
    version="1.0.0",
    description="Pet care AI - feeding, vaccinations, breed ID, health checks, training",
)

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
_RATE_LIMITS = {"free": {"requests_per_hour": 60}, "pro": {"requests_per_hour": 5000}}
_request_log: list[float] = []
_tier = "free"


def _check_rate_limit() -> bool:
    now = time.time()
    _request_log[:] = [t for t in _request_log if now - t < 3600]
    if len(_request_log) >= _RATE_LIMITS[_tier]["requests_per_hour"]:
        return False
    _request_log.append(now)
    return True


# ---------------------------------------------------------------------------
# Breed database
# ---------------------------------------------------------------------------
_DOG_BREEDS: dict[str, dict] = {
    "labrador_retriever": {
        "name": "Labrador Retriever", "group": "Sporting", "size": "large",
        "weight_kg": (25, 36), "height_cm": (55, 62), "lifespan_years": (10, 14),
        "temperament": ["friendly", "active", "outgoing"], "energy_level": "high",
        "grooming_needs": "moderate", "shedding": "heavy",
        "common_health_issues": ["hip_dysplasia", "obesity", "ear_infections", "elbow_dysplasia"],
        "exercise_mins_daily": 60, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "easy", "apartment_suitable": False,
    },
    "german_shepherd": {
        "name": "German Shepherd", "group": "Herding", "size": "large",
        "weight_kg": (30, 40), "height_cm": (55, 65), "lifespan_years": (9, 13),
        "temperament": ["loyal", "confident", "courageous"], "energy_level": "high",
        "grooming_needs": "moderate", "shedding": "heavy",
        "common_health_issues": ["hip_dysplasia", "degenerative_myelopathy", "bloat"],
        "exercise_mins_daily": 90, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "easy", "apartment_suitable": False,
    },
    "french_bulldog": {
        "name": "French Bulldog", "group": "Non-Sporting", "size": "small",
        "weight_kg": (8, 14), "height_cm": (28, 33), "lifespan_years": (10, 14),
        "temperament": ["playful", "adaptable", "affectionate"], "energy_level": "low",
        "grooming_needs": "low", "shedding": "moderate",
        "common_health_issues": ["brachycephalic_syndrome", "spine_issues", "allergies", "ear_infections"],
        "exercise_mins_daily": 30, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "moderate", "apartment_suitable": True,
    },
    "golden_retriever": {
        "name": "Golden Retriever", "group": "Sporting", "size": "large",
        "weight_kg": (25, 34), "height_cm": (51, 61), "lifespan_years": (10, 12),
        "temperament": ["intelligent", "friendly", "devoted"], "energy_level": "high",
        "grooming_needs": "high", "shedding": "heavy",
        "common_health_issues": ["cancer", "hip_dysplasia", "heart_disease", "skin_allergies"],
        "exercise_mins_daily": 60, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "easy", "apartment_suitable": False,
    },
    "poodle": {
        "name": "Poodle (Standard)", "group": "Non-Sporting", "size": "medium",
        "weight_kg": (18, 32), "height_cm": (38, 60), "lifespan_years": (12, 15),
        "temperament": ["intelligent", "active", "proud"], "energy_level": "high",
        "grooming_needs": "high", "shedding": "minimal",
        "common_health_issues": ["hip_dysplasia", "eye_disorders", "bloat", "addisons_disease"],
        "exercise_mins_daily": 60, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "easy", "apartment_suitable": True,
    },
    "cavalier_king_charles": {
        "name": "Cavalier King Charles Spaniel", "group": "Toy", "size": "small",
        "weight_kg": (5, 8), "height_cm": (30, 33), "lifespan_years": (9, 14),
        "temperament": ["affectionate", "gentle", "graceful"], "energy_level": "moderate",
        "grooming_needs": "moderate", "shedding": "moderate",
        "common_health_issues": ["mitral_valve_disease", "syringomyelia", "eye_conditions"],
        "exercise_mins_daily": 40, "good_with_children": True, "good_with_other_dogs": True,
        "training_difficulty": "easy", "apartment_suitable": True,
    },
}

_CAT_BREEDS: dict[str, dict] = {
    "british_shorthair": {
        "name": "British Shorthair", "size": "medium_large",
        "weight_kg": (4, 8), "lifespan_years": (12, 20),
        "temperament": ["calm", "easygoing", "independent"], "energy_level": "low",
        "grooming_needs": "low", "shedding": "moderate",
        "common_health_issues": ["hypertrophic_cardiomyopathy", "obesity", "dental_disease"],
        "indoor_only": False, "good_with_children": True,
    },
    "maine_coon": {
        "name": "Maine Coon", "size": "large",
        "weight_kg": (5, 11), "lifespan_years": (12, 15),
        "temperament": ["gentle", "playful", "intelligent"], "energy_level": "moderate",
        "grooming_needs": "high", "shedding": "heavy",
        "common_health_issues": ["hypertrophic_cardiomyopathy", "hip_dysplasia", "spinal_muscular_atrophy"],
        "indoor_only": False, "good_with_children": True,
    },
    "siamese": {
        "name": "Siamese", "size": "medium",
        "weight_kg": (3, 5), "lifespan_years": (15, 20),
        "temperament": ["vocal", "social", "intelligent"], "energy_level": "high",
        "grooming_needs": "low", "shedding": "low",
        "common_health_issues": ["amyloidosis", "asthma", "dental_disease", "crossed_eyes"],
        "indoor_only": True, "good_with_children": True,
    },
}

_VACCINATION_SCHEDULES = {
    "dog": {
        "core": [
            {"vaccine": "DHPP (Distemper, Hepatitis, Parainfluenza, Parvo)", "age_weeks": 8, "boosters": [12, 16], "annual": True},
            {"vaccine": "Rabies", "age_weeks": 12, "boosters": [64], "annual": False, "every_years": 3},
        ],
        "non_core": [
            {"vaccine": "Bordetella (Kennel Cough)", "age_weeks": 8, "annual": True},
            {"vaccine": "Leptospirosis", "age_weeks": 12, "boosters": [16], "annual": True},
            {"vaccine": "Canine Influenza", "age_weeks": 8, "boosters": [12], "annual": True},
        ],
    },
    "cat": {
        "core": [
            {"vaccine": "FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)", "age_weeks": 8, "boosters": [12, 16], "annual": False, "every_years": 3},
            {"vaccine": "Rabies", "age_weeks": 12, "boosters": [], "annual": False, "every_years": 3},
        ],
        "non_core": [
            {"vaccine": "FeLV (Feline Leukemia)", "age_weeks": 8, "boosters": [12], "annual": True},
        ],
    },
}

_SYMPTOMS_DB = {
    "vomiting": {"urgency": "moderate", "possible_causes": ["dietary_indiscretion", "infection", "toxin_ingestion", "obstruction", "pancreatitis"], "action": "Monitor for 24h. Vet if persistent, bloody, or with lethargy."},
    "diarrhea": {"urgency": "moderate", "possible_causes": ["diet_change", "infection", "parasites", "stress", "food_intolerance"], "action": "Bland diet (rice + chicken). Vet if bloody or lasting >48h."},
    "lethargy": {"urgency": "high", "possible_causes": ["infection", "pain", "anemia", "heart_disease", "poisoning"], "action": "Vet visit recommended within 24 hours."},
    "limping": {"urgency": "moderate", "possible_causes": ["sprain", "fracture", "joint_disease", "nail_injury", "arthritis"], "action": "Rest for 24-48h. Vet if no improvement or if non-weight-bearing."},
    "excessive_thirst": {"urgency": "high", "possible_causes": ["diabetes", "kidney_disease", "cushings", "liver_disease", "infection"], "action": "Vet visit soon. Could indicate serious metabolic condition."},
    "scratching": {"urgency": "low", "possible_causes": ["fleas", "allergies", "dry_skin", "mites", "fungal_infection"], "action": "Check for fleas. Try oatmeal bath. Vet if persistent or with hair loss."},
    "coughing": {"urgency": "moderate", "possible_causes": ["kennel_cough", "heart_disease", "allergies", "tracheal_collapse", "pneumonia"], "action": "Vet visit if persistent >3 days or with difficulty breathing."},
    "not_eating": {"urgency": "high", "possible_causes": ["illness", "dental_pain", "stress", "obstruction", "nausea"], "action": "Dogs: vet if >24h. Cats: vet if >12h (risk of hepatic lipidosis)."},
}


@mcp.tool()
def generate_feeding_schedule(
    species: str,
    breed: Optional[str] = None,
    weight_kg: float = 10.0,
    age_months: int = 24,
    activity_level: str = "moderate",
    special_needs: Optional[list[str]] = None,
) -> dict:
    """Generate a tailored feeding schedule for a pet.

    Args:
        species: dog | cat.
        breed: Breed name (snake_case, e.g. labrador_retriever).
        weight_kg: Current weight in kg.
        age_months: Age in months.
        activity_level: low | moderate | high.
        special_needs: List like ["weight_loss", "sensitive_stomach", "senior"].
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    special_needs = special_needs or []
    is_puppy = age_months < 12 if species == "dog" else age_months < 12
    is_senior = age_months > 84 if species == "dog" else age_months > 120

    # Base caloric needs (RER * activity factor)
    rer = 70 * (weight_kg ** 0.75)
    activity_mult = {"low": 1.2, "moderate": 1.4, "high": 1.8}.get(activity_level, 1.4)
    if is_puppy:
        activity_mult = 2.5 if age_months < 4 else 2.0
    if is_senior:
        activity_mult *= 0.85
    if "weight_loss" in special_needs:
        activity_mult *= 0.80

    daily_calories = round(rer * activity_mult)
    meals_per_day = 3 if is_puppy else 2

    # Portion sizing (assuming ~350 kcal per cup dry food)
    cups_per_day = round(daily_calories / 350, 1)
    grams_per_day = round(daily_calories / 3.5)  # ~3.5 kcal per gram dry

    schedule = {
        "morning": {"time": "07:00", "portion": f"{round(grams_per_day / meals_per_day)}g dry food", "notes": "Fresh water always available"},
        "evening": {"time": "18:00", "portion": f"{round(grams_per_day / meals_per_day)}g dry food", "notes": ""},
    }
    if meals_per_day == 3:
        schedule["midday"] = {"time": "12:30", "portion": f"{round(grams_per_day / meals_per_day)}g dry food", "notes": "Important for growing pets"}

    breed_info = None
    if breed:
        db = _DOG_BREEDS if species == "dog" else _CAT_BREEDS
        breed_info = db.get(breed)

    return {
        "pet_profile": {"species": species, "breed": breed, "weight_kg": weight_kg, "age_months": age_months, "life_stage": "puppy/kitten" if is_puppy else "senior" if is_senior else "adult"},
        "daily_requirements": {"calories": daily_calories, "cups_dry_food": cups_per_day, "grams_dry_food": grams_per_day, "meals_per_day": meals_per_day},
        "schedule": schedule,
        "treats": {"max_daily_calories": round(daily_calories * 0.1), "note": "Treats should not exceed 10% of daily intake"},
        "special_considerations": special_needs if special_needs else ["None specified"],
        "breed_notes": breed_info.get("common_health_issues", []) if breed_info else [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def track_vaccinations(
    species: str,
    age_weeks: int,
    vaccinations_given: Optional[list[str]] = None,
    indoor_only: bool = False,
) -> dict:
    """Track vaccination status and generate upcoming schedule.

    Args:
        species: dog | cat.
        age_weeks: Current age in weeks.
        vaccinations_given: List of vaccines already administered.
        indoor_only: Whether pet is indoor-only (affects non-core recommendations).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    vaccinations_given = vaccinations_given or []
    schedule = _VACCINATION_SCHEDULES.get(species)
    if not schedule:
        return {"error": f"Unknown species: {species}. Use dog or cat."}

    overdue = []
    upcoming = []
    completed = []

    for vax in schedule["core"]:
        name = vax["vaccine"]
        if name in vaccinations_given:
            completed.append({"vaccine": name, "status": "completed", "type": "core"})
        elif age_weeks >= vax["age_weeks"]:
            overdue.append({"vaccine": name, "due_at_weeks": vax["age_weeks"], "weeks_overdue": age_weeks - vax["age_weeks"], "type": "core", "priority": "HIGH"})
        else:
            upcoming.append({"vaccine": name, "due_at_weeks": vax["age_weeks"], "weeks_until_due": vax["age_weeks"] - age_weeks, "type": "core"})

        for booster_week in vax.get("boosters", []):
            booster_name = f"{name} (booster)"
            if booster_name in vaccinations_given:
                completed.append({"vaccine": booster_name, "status": "completed", "type": "core"})
            elif age_weeks >= booster_week:
                overdue.append({"vaccine": booster_name, "due_at_weeks": booster_week, "weeks_overdue": age_weeks - booster_week, "type": "core", "priority": "HIGH"})
            else:
                upcoming.append({"vaccine": booster_name, "due_at_weeks": booster_week, "weeks_until_due": booster_week - age_weeks, "type": "core"})

    if not indoor_only:
        for vax in schedule.get("non_core", []):
            name = vax["vaccine"]
            if name in vaccinations_given:
                completed.append({"vaccine": name, "status": "completed", "type": "non_core"})
            elif age_weeks >= vax["age_weeks"]:
                upcoming.append({"vaccine": name, "due_at_weeks": vax["age_weeks"], "type": "non_core", "note": "Recommended based on lifestyle"})

    return {
        "species": species, "age_weeks": age_weeks,
        "completed": completed, "overdue": overdue, "upcoming": upcoming,
        "summary": {
            "total_given": len(completed), "overdue_count": len(overdue), "upcoming_count": len(upcoming),
            "next_appointment": overdue[0] if overdue else upcoming[0] if upcoming else None,
            "status": "OVERDUE" if overdue else "UP_TO_DATE" if not upcoming else "ON_TRACK",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def identify_breed(
    species: str,
    characteristics: dict,
) -> dict:
    """Identify likely breed from physical and behavioral characteristics.

    Args:
        species: dog | cat.
        characteristics: Dict with optional keys: size (small|medium|large), weight_kg, coat_length,
                        energy_level, temperament_tags (list), color, good_with_children (bool).
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    db = _DOG_BREEDS if species == "dog" else _CAT_BREEDS
    scores: list[tuple[str, float, dict]] = []

    for breed_id, breed in db.items():
        score = 0.0
        max_score = 0.0

        # Size match
        if "size" in characteristics:
            max_score += 3
            if characteristics["size"] == breed.get("size"):
                score += 3

        # Weight match
        if "weight_kg" in characteristics:
            max_score += 2
            w = characteristics["weight_kg"]
            wrange = breed.get("weight_kg", (0, 100))
            if wrange[0] <= w <= wrange[1]:
                score += 2
            elif abs(w - sum(wrange) / 2) < 5:
                score += 1

        # Energy match
        if "energy_level" in characteristics:
            max_score += 2
            if characteristics["energy_level"] == breed.get("energy_level"):
                score += 2

        # Temperament overlap
        if "temperament_tags" in characteristics:
            max_score += 3
            breed_temps = set(breed.get("temperament", []))
            user_temps = set(characteristics["temperament_tags"])
            overlap = len(breed_temps & user_temps)
            score += min(3, overlap * 1.5)

        # Good with children
        if "good_with_children" in characteristics:
            max_score += 1
            if characteristics["good_with_children"] == breed.get("good_with_children"):
                score += 1

        pct = round((score / max_score) * 100) if max_score > 0 else 0
        scores.append((breed_id, pct, breed))

    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:3]

    return {
        "species": species,
        "input_characteristics": characteristics,
        "matches": [
            {
                "breed": match[2].get("name", match[0]),
                "confidence_pct": match[1],
                "profile": match[2],
            }
            for match in top
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def check_health_symptoms(
    species: str,
    symptoms: list[str],
    age_months: int = 24,
    additional_info: Optional[str] = None,
) -> dict:
    """Check pet health symptoms and get guidance on urgency and next steps.

    Args:
        symptoms: List of symptoms (e.g. vomiting, lethargy, limping, scratching).
        species: dog | cat.
        age_months: Pet age in months.
        additional_info: Any extra context (e.g. "ate chocolate 2 hours ago").
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    findings = []
    max_urgency = "low"
    urgency_rank = {"low": 0, "moderate": 1, "high": 2, "emergency": 3}

    for symptom in symptoms:
        sym_key = symptom.lower().replace(" ", "_")
        info = _SYMPTOMS_DB.get(sym_key)
        if info:
            findings.append({"symptom": symptom, **info})
            if urgency_rank.get(info["urgency"], 0) > urgency_rank.get(max_urgency, 0):
                max_urgency = info["urgency"]
        else:
            findings.append({"symptom": symptom, "urgency": "unknown", "possible_causes": ["consult_vet"], "action": "Symptom not in database. Consult a veterinarian."})

    # Age-based urgency escalation
    if age_months < 6 or age_months > 120:
        max_urgency = "high" if max_urgency != "emergency" else max_urgency

    # Multiple symptom escalation
    if len(symptoms) >= 3:
        if urgency_rank.get(max_urgency, 0) < 2:
            max_urgency = "high"

    return {
        "species": species, "age_months": age_months,
        "symptoms_analyzed": findings,
        "overall_urgency": max_urgency,
        "recommendation": {
            "low": "Monitor at home for 24-48 hours. Vet if worsening.",
            "moderate": "Schedule a vet appointment within 24-48 hours.",
            "high": "See a vet within 24 hours.",
            "emergency": "Seek emergency veterinary care immediately.",
        }.get(max_urgency, "Consult a veterinarian."),
        "disclaimer": "This is advisory guidance only. Always consult a qualified veterinarian for medical decisions.",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def get_training_recommendations(
    species: str,
    breed: Optional[str] = None,
    age_months: int = 6,
    issues: Optional[list[str]] = None,
    experience_level: str = "beginner",
) -> dict:
    """Get personalized training recommendations for a pet.

    Args:
        species: dog | cat.
        breed: Breed name (snake_case).
        age_months: Pet age in months.
        issues: Behavioral issues to address (e.g. pulling_on_lead, barking, jumping).
        experience_level: beginner | intermediate | advanced.
    """
    if not _check_rate_limit():
        return {"error": "Rate limit exceeded. Upgrade to pro tier."}

    issues = issues or []
    is_puppy = age_months < 6

    _TRAINING_TIPS = {
        "pulling_on_lead": {"method": "Stop-start technique. Stop walking when they pull, resume when leash is slack.", "sessions": "10-15 min twice daily", "timeframe": "2-4 weeks", "tools": ["front-clip harness", "high-value treats"]},
        "barking": {"method": "Identify trigger, desensitize gradually. Reward quiet behavior.", "sessions": "5-10 min, multiple times daily", "timeframe": "3-6 weeks", "tools": ["treats", "puzzle toys for mental stimulation"]},
        "jumping": {"method": "Turn away and ignore. Only give attention when all four paws on floor.", "sessions": "Every interaction is training", "timeframe": "1-3 weeks with consistency", "tools": ["treats", "patience"]},
        "recall": {"method": "Start indoors, use high-value rewards, long line for outdoor practice.", "sessions": "10 min twice daily", "timeframe": "4-8 weeks", "tools": ["long line", "high-value treats", "whistle"]},
        "separation_anxiety": {"method": "Gradual alone-time building. Start with seconds, build to hours.", "sessions": "Multiple short sessions daily", "timeframe": "4-12 weeks", "tools": ["Kong/puzzle toys", "calming music", "possibly DAP diffuser"]},
        "litter_training": {"method": "Place cat in clean box after meals and naps. Reward success.", "sessions": "Consistent placement after key activities", "timeframe": "1-2 weeks for kittens", "tools": ["large litter box", "unscented litter"]},
    }

    recommendations = []
    if is_puppy and species == "dog":
        recommendations.append({
            "priority": 1, "skill": "socialization",
            "method": "Expose to 100 new experiences in first 100 days. People, dogs, sounds, surfaces.",
            "sessions": "Daily varied experiences", "timeframe": "Before 16 weeks critical",
            "tools": ["treats", "safe environments"],
        })
        recommendations.append({
            "priority": 2, "skill": "basic_obedience",
            "method": "Sit, down, stay, come. Use positive reinforcement only.",
            "sessions": "5-10 min 3x daily", "timeframe": "Ongoing",
            "tools": ["clicker", "small training treats"],
        })

    for issue in issues:
        tip = _TRAINING_TIPS.get(issue)
        if tip:
            recommendations.append({"priority": len(recommendations) + 1, "skill": issue, **tip})
        else:
            recommendations.append({"priority": len(recommendations) + 1, "skill": issue, "method": "Consult a certified trainer for personalized guidance.", "sessions": "N/A", "timeframe": "Varies", "tools": ["professional trainer"]})

    breed_info = None
    if breed:
        db = _DOG_BREEDS if species == "dog" else _CAT_BREEDS
        breed_info = db.get(breed)

    return {
        "pet_profile": {"species": species, "breed": breed, "age_months": age_months, "life_stage": "puppy/kitten" if is_puppy else "adult"},
        "training_plan": recommendations,
        "general_principles": [
            "Use positive reinforcement - reward desired behavior",
            "Keep sessions short (5-15 minutes)",
            "Be consistent across all family members",
            "End on a positive note",
            "Never use punishment-based methods",
        ],
        "breed_considerations": {
            "training_difficulty": breed_info.get("training_difficulty", "unknown") if breed_info else "unknown",
            "energy_level": breed_info.get("energy_level", "unknown") if breed_info else "unknown",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()
