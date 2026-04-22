from datetime import datetime, timedelta, timezone

from app.services.game_engine import (
    ACTION_DELTAS,
    DEFAULT_REACTION,
    DEFAULT_VITAL,
    EVOLUTION_ACTION_BUFFER_THRESHOLD,
    EVOLUTION_STREAK_TARGET,
    apply_vital_changes,
    apply_elapsed_time,
    build_reaction_for_action,
    create_default_pet,
    derive_state,
    repair_or_reset_loaded_pet,
    reset_pet_fields,
    sync_status,
    tick_pet_once,
    update_streak_after_action,
)


def test_default_pet_state_is_healthy() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    assert pet.name == "ChuChu"
    assert pet.hunger == 92
    assert pet.happiness == 92
    assert pet.energy == 92
    assert pet.status == "normal"


def test_feed_action_delta_matches_spec() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    apply_vital_changes(pet, ACTION_DELTAS["feed"])

    assert (pet.hunger, pet.happiness, pet.energy) == (100, 98, 91)


def test_play_action_delta_matches_spec() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    apply_vital_changes(pet, ACTION_DELTAS["play"])

    assert (pet.hunger, pet.happiness, pet.energy) == (88, 100, 84)


def test_rest_action_delta_matches_spec() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    apply_vital_changes(pet, ACTION_DELTAS["rest"])

    assert (pet.hunger, pet.happiness, pet.energy) == (90, 91, 100)


def test_single_tick_decay_changes_vitals() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    tick_pet_once(pet)

    assert (pet.hunger, pet.happiness, pet.energy) == (89, 89, 89)


def test_six_ticks_follow_locked_decay_pattern() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))

    for _ in range(6):
        tick_pet_once(pet)

    assert (pet.hunger, pet.happiness, pet.energy) == (74, 74, 74)


def test_elapsed_time_caps_to_eight_hours() -> None:
    start = datetime.now(timezone.utc)
    pet = create_default_pet(start)

    apply_elapsed_time(pet, start + timedelta(hours=12))

    assert pet.last_updated_at == start + timedelta(hours=12)
    assert pet.hunger == 0
    assert pet.happiness == 0
    assert pet.energy == 0


def test_sub_tick_syncs_do_not_freeze_time_progression() -> None:
    start = datetime.now(timezone.utc)
    pet = create_default_pet(start)

    apply_elapsed_time(pet, start + timedelta(milliseconds=500))
    apply_elapsed_time(pet, start + timedelta(milliseconds=1000))
    apply_elapsed_time(pet, start + timedelta(milliseconds=1500))

    assert (pet.hunger, pet.happiness, pet.energy) == (92, 92, 92)
    assert pet.total_ticks == 0
    assert pet.last_updated_at == start

    apply_elapsed_time(pet, start + timedelta(milliseconds=2100))

    assert (pet.hunger, pet.happiness, pet.energy) == (89, 89, 89)
    assert pet.total_ticks == 1
    assert pet.last_updated_at == start + timedelta(seconds=2)


def test_high_value_recovery_clamps_to_maximum() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.hunger = 95
    pet.happiness = 98
    pet.energy = 99

    apply_vital_changes(pet, ACTION_DELTAS["feed"])

    assert pet.hunger == 100
    assert pet.happiness == 100
    assert pet.energy == 98

    apply_vital_changes(pet, ACTION_DELTAS["rest"])

    assert pet.energy == 100


def test_derived_state_marks_attention_when_two_vitals_are_low() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.hunger = 20
    pet.energy = 24

    derived = derive_state(pet)

    assert derived.needs_attention is True
    assert derived.critical_vitals == ["hunger", "energy"]


def test_sick_status_triggers_when_two_vitals_are_critical() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.hunger = 20
    pet.energy = 24

    sync_status(pet)

    assert pet.status == "sick"


def test_sick_status_recovers_after_all_vitals_clear_recovery_threshold() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.status = "sick"
    pet.hunger = 41
    pet.happiness = 55
    pet.energy = 64

    sync_status(pet)

    assert pet.status == "normal"


def test_streak_reaches_evolution_target() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.hunger = 100
    pet.happiness = 100
    pet.energy = 100

    while pet.healthy_streak < EVOLUTION_STREAK_TARGET:
        tick_pet_once(pet)
        if pet.healthy_streak < EVOLUTION_STREAK_TARGET and (
            pet.hunger <= 82 or pet.happiness <= 82 or pet.energy <= 82
        ):
            apply_vital_changes(pet, {"hunger": 18, "happiness": 18, "energy": 18})
            update_streak_after_action(pet)

    assert pet.status == "evolved"
    assert pet.healthy_streak == EVOLUTION_STREAK_TARGET


def test_supportive_action_buffer_keeps_evolution_progress_alive() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.healthy_streak = 4
    pet.hunger = EVOLUTION_ACTION_BUFFER_THRESHOLD
    pet.happiness = 96
    pet.energy = 74

    update_streak_after_action(pet)

    assert pet.healthy_streak == 4


def test_action_buffer_breaks_when_any_vital_drops_too_low() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.healthy_streak = 4
    pet.hunger = EVOLUTION_ACTION_BUFFER_THRESHOLD - 1
    pet.happiness = 96
    pet.energy = 74

    update_streak_after_action(pet)

    assert pet.healthy_streak == 0


def test_evolved_state_remains_permanent_after_decay() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.status = "evolved"
    pet.healthy_streak = EVOLUTION_STREAK_TARGET
    pet.hunger = 10
    pet.happiness = 15
    pet.energy = 12

    tick_pet_once(pet)

    assert pet.status == "evolved"
    assert pet.healthy_streak == EVOLUTION_STREAK_TARGET


def test_reaction_fallback_returns_default_copy_for_feed() -> None:
    pet = create_default_pet(datetime.now(timezone.utc))
    pet.hunger = 40
    pet.happiness = 40
    pet.energy = 40

    assert build_reaction_for_action("feed", pet) == "ChuChu munches happily and leans a little closer."


def test_invalid_loaded_pet_resets_to_fresh_defaults() -> None:
    now = datetime.now(timezone.utc)
    pet = create_default_pet(now - timedelta(hours=1))
    pet.status = "broken"
    pet.hunger = -400
    pet.last_reaction = "bad"

    repaired = repair_or_reset_loaded_pet(pet, now)

    assert repaired.status == "normal"
    assert repaired.hunger == DEFAULT_VITAL
    assert repaired.happiness == DEFAULT_VITAL
    assert repaired.energy == DEFAULT_VITAL
    assert repaired.last_reaction == DEFAULT_REACTION
    assert repaired.last_updated_at == now


def test_out_of_range_loaded_vitals_are_clamped_without_full_reset() -> None:
    now = datetime.now(timezone.utc)
    pet = create_default_pet(now - timedelta(minutes=5))
    pet.hunger = 1000
    pet.happiness = -5
    pet.energy = 40

    repaired = repair_or_reset_loaded_pet(pet, now)

    assert repaired.status == "normal"
    assert repaired.hunger == 100
    assert repaired.happiness == 0
    assert repaired.energy == 40


def test_reset_pet_fields_restores_clean_start() -> None:
    now = datetime.now(timezone.utc)
    pet = create_default_pet(now - timedelta(hours=1))
    pet.status = "sick"
    pet.hunger = 2
    pet.happiness = 3
    pet.energy = 4
    pet.total_ticks = 99

    reset_pet_fields(pet, now)

    assert pet.name == "ChuChu"
    assert pet.status == "normal"
    assert pet.hunger == DEFAULT_VITAL
    assert pet.happiness == DEFAULT_VITAL
    assert pet.energy == DEFAULT_VITAL
    assert pet.total_ticks == 0
