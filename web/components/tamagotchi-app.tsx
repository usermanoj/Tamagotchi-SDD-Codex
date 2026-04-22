"use client";

import Image from "next/image";
import { startTransition, useEffect, useMemo, useRef, useState } from "react";

import { fetchPet, performAction, resetPet } from "../lib/api";
import type { PetAction, PetState, PetStatus } from "../lib/types";

const EVOLUTION_THRESHOLD = 80;
const EVOLUTION_BUFFER_THRESHOLD = 70;

const actionCopy: Array<{ action: PetAction; label: string; hint: string }> = [
  { action: "feed", label: "Feed", hint: "Best for lifting Hunger while keeping an evolution run stable." },
  { action: "play", label: "Play", hint: "Big Happiness boost. Use it when the other vitals are already strong." },
  { action: "rest", label: "Rest", hint: "Safest recovery move for Energy and long streaks." },
];

const vitalMeta = [
  { key: "hunger", label: "Hunger" },
  { key: "happiness", label: "Happiness" },
  { key: "energy", label: "Energy" },
] as const;

const statePath: Array<{ status: PetStatus; label: string; detail: string }> = [
  { status: "normal", label: "Normal", detail: "Balanced and happy." },
  { status: "sick", label: "Sick", detail: "Two low vitals need rescue." },
  { status: "evolved", label: "Evolved", detail: "Permanent special form." },
];

const artworkByStatus: Record<PetStatus, { src: string; alt: string }> = {
  normal: {
    src: "/chuchu/normal.png",
    alt: "ChuChu sitting happily and looking healthy.",
  },
  sick: {
    src: "/chuchu/sick.png",
    alt: "ChuChu looking unwell under a small blue blanket.",
  },
  evolved: {
    src: "/chuchu/evolved.png",
    alt: "ChuChu glowing softly with a star on the collar.",
  },
};

function formatSyncTime(value: string) {
  return new Intl.DateTimeFormat("en-SG", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date(value));
}

function titleCase(value: string) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

export function TamagotchiApp() {
  const [pet, setPet] = useState<PetState | null>(null);
  const [loading, setLoading] = useState(true);
  const [pendingAction, setPendingAction] = useState<PetAction | "reset" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const mounted = useRef(false);

  async function refreshPet(options?: { silent?: boolean }) {
    try {
      const result = await fetchPet();
      startTransition(() => {
        setPet(result);
        setError(null);
        setLoading(false);
      });
    } catch (fetchError) {
      startTransition(() => {
        setError(fetchError instanceof Error ? fetchError.message : "Unable to reach the backend.");
        if (!options?.silent) {
          setLoading(false);
        }
      });
    }
  }

  useEffect(() => {
    mounted.current = true;
    void refreshPet();

    const intervalId = window.setInterval(() => {
      void refreshPet({ silent: true });
    }, 2000);

    return () => {
      mounted.current = false;
      window.clearInterval(intervalId);
    };
  }, []);

  async function handleAction(action: PetAction) {
    setPendingAction(action);
    try {
      const result = await performAction(action);
      startTransition(() => {
        setPet(result);
        setError(null);
      });
    } catch (actionError) {
      startTransition(() => {
        setError(actionError instanceof Error ? actionError.message : "Action failed.");
      });
    } finally {
      if (mounted.current) {
        setPendingAction(null);
      }
    }
  }

  async function handleReset() {
    if (!window.confirm("Reset ChuChu and start a new care loop?")) {
      return;
    }

    setPendingAction("reset");
    try {
      const result = await resetPet();
      startTransition(() => {
        setPet(result);
        setError(null);
      });
    } catch (resetError) {
      startTransition(() => {
        setError(resetError instanceof Error ? resetError.message : "Reset failed.");
      });
    } finally {
      if (mounted.current) {
        setPendingAction(null);
      }
    }
  }

  const highlightedStatus = useMemo(() => {
    if (!pet) {
      return "normal";
    }

    if (pet.status === "sick") {
      return "sick";
    }

    if (pet.status === "evolved") {
      return "evolved";
    }

    if (pet.critical_vitals.length > 0) {
      return "warning";
    }

    return "normal";
  }, [pet]);

  const artworkStatus: PetStatus = pet?.status ?? "normal";
  const artwork = artworkByStatus[artworkStatus];
  const evolutionTarget = pet?.evolution_target ?? 6;
  const evolutionProgress = pet?.evolution_progress ?? 0;
  const evolutionRatio = Math.min(100, Math.round((evolutionProgress / evolutionTarget) * 100));
  const remainingEvolutionTicks = Math.max(0, evolutionTarget - evolutionProgress);
  const isHealthyForEvolution = Boolean(
    pet &&
      pet.hunger >= EVOLUTION_THRESHOLD &&
      pet.happiness >= EVOLUTION_THRESHOLD &&
      pet.energy >= EVOLUTION_THRESHOLD &&
      pet.status !== "evolved",
  );
  const isEvolutionProgressBuffered = Boolean(
    pet &&
      pet.status !== "evolved" &&
      evolutionProgress > 0 &&
      !isHealthyForEvolution &&
      pet.hunger >= EVOLUTION_BUFFER_THRESHOLD &&
      pet.happiness >= EVOLUTION_BUFFER_THRESHOLD &&
      pet.energy >= EVOLUTION_BUFFER_THRESHOLD,
  );
  const evolutionStatusTone = pet?.status === "evolved"
    ? "lock"
    : isHealthyForEvolution
      ? "open"
      : isEvolutionProgressBuffered
        ? "buffer"
        : "closed";
  const evolutionStatusLabel = pet?.status === "evolved"
    ? "Permanent"
    : isHealthyForEvolution
      ? "Window Open"
      : isEvolutionProgressBuffered
        ? "Recover Fast"
        : "Closed";
  const evolutionMessage = pet?.status === "evolved"
    ? "ChuChu reached the special evolved form and keeps it until reset."
    : isHealthyForEvolution && remainingEvolutionTicks === 1
      ? "One more steady tick will push ChuChu into the evolved state."
      : isHealthyForEvolution
        ? `Evolution window open. Keep all three vitals at 80+ for ${remainingEvolutionTicks} more steady ticks.`
        : isEvolutionProgressBuffered
          ? "Progress is still alive. Lift every vital back above 80 before the next tick."
          : "Bring Hunger, Happiness, and Energy all to 80+ to start the evolution run.";

  return (
    <main className="page-shell">
      <div className="ambient ambient-a" />
      <div className="ambient ambient-b" />
      <div className="ambient ambient-c" />

      <div className="page-grid">
        <section className={`hero-card ${pet?.status === "evolved" ? "hero-card-evolved" : ""}`}>
          <div className="hero-header">
            <div>
              <p className="eyebrow">Spec-Driven MVP</p>
              <h1>ChuChu</h1>
            </div>
            <span className={`status-pill status-${highlightedStatus}`}>
              {pet ? titleCase(pet.status) : "Loading"}
            </span>
          </div>

          <p className="hero-copy">
            A living pet loop with timed vitals, backend persistence, visible state transitions, and a deliberately
            scoped spec-first implementation.
          </p>

          <div className="state-path">
            {statePath.map((step) => (
              <article
                key={step.status}
                className={`state-step ${pet?.status === step.status ? "state-step-active" : ""}`}
              >
                <span>{step.label}</span>
                <p>{step.detail}</p>
              </article>
            ))}
          </div>

          {pet?.status === "evolved" ? (
            <div className="evolved-banner">ChuChu Evolved!</div>
          ) : null}

          <div className={`avatar-frame avatar-${highlightedStatus}`}>
            <div className="avatar-illustration-shell">
              <Image
                src={artwork.src}
                alt={artwork.alt}
                fill
                priority
                sizes="(max-width: 980px) 100vw, 430px"
                className="avatar-illustration"
              />
            </div>
            <div className="avatar-stage-glow" />
          </div>

          <div className="hero-footnotes">
            <div className="metric-chip">
              <span>Sync</span>
              <strong>{pet ? formatSyncTime(pet.last_updated_at) : "--:--:--"}</strong>
            </div>
            <div className="metric-chip">
              <span>Ticks</span>
              <strong>{pet ? pet.total_ticks : 0}</strong>
            </div>
            <div className="metric-chip">
              <span>Evolution</span>
              <strong>
                {pet?.status === "evolved"
                  ? "Permanent"
                  : `${pet?.evolution_progress ?? 0}/${pet?.evolution_target ?? 12}`}
              </strong>
            </div>
          </div>
        </section>

        <section className="panel-stack">
          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="panel-kicker">Live Vitals</p>
                <h2>Needs at a glance</h2>
              </div>
              {pet?.needs_attention ? <span className="attention-flag">Needs care</span> : null}
            </div>

            {loading ? <p className="placeholder-copy">Loading ChuChu from the backend...</p> : null}
            {error ? <p className="error-copy">{error}</p> : null}

            <div className="vitals-grid">
              {pet
                ? vitalMeta.map((item) => {
                    const value = pet[item.key];
                    const tone = value <= 25 ? "critical" : value <= 50 ? "warning" : "healthy";

                    return (
                      <article key={item.key} className={`vital-card vital-${tone}`}>
                        <div className="vital-row">
                          <span>{item.label}</span>
                          <strong>{value}</strong>
                        </div>
                        <div className="vital-track">
                          <div className="vital-fill" style={{ width: `${value}%` }} />
                        </div>
                      </article>
                    );
                  })
                : null}
            </div>

            <div className="insight-grid">
              <article className="insight-card">
                <span className="insight-label">Current reaction</span>
                <p>{pet?.last_reaction ?? "Waiting for ChuChu..."}</p>
              </article>
              <article className="insight-card">
                <span className="insight-label">Critical vitals</span>
                <p>{pet?.critical_vitals.length ? pet.critical_vitals.map(titleCase).join(", ") : "None"}</p>
              </article>
            </div>

            <article className={`evolution-card ${pet?.status === "evolved" ? "evolution-card-evolved" : ""}`}>
              <div className="evolution-card-header">
                <span className="insight-label">Well Cared For</span>
                <strong>
                  {pet?.status === "evolved" ? "Evolved" : `${evolutionProgress}/${evolutionTarget}`}
                </strong>
              </div>
              <div className="evolution-status-row">
                <span className={`evolution-status-pill evolution-status-${evolutionStatusTone}`}>
                  {evolutionStatusLabel}
                </span>
                <span className="evolution-next-step">
                  {pet?.status === "evolved"
                    ? "Special form unlocked"
                    : `${remainingEvolutionTicks} steady ${remainingEvolutionTicks === 1 ? "tick" : "ticks"} to go`}
                </span>
              </div>
              <div className="evolution-track">
                <div
                  className="evolution-fill"
                  style={{ width: `${pet?.status === "evolved" ? 100 : evolutionRatio}%` }}
                />
              </div>
              <p>{evolutionMessage}</p>
            </article>
          </section>

          <section className="panel">
            <div className="panel-heading">
              <div>
                <p className="panel-kicker">Care Loop</p>
                <h2>Keep the balance going</h2>
              </div>
              <button className="ghost-button" onClick={handleReset} disabled={pendingAction !== null}>
                {pendingAction === "reset" ? "Resetting..." : "Reset"}
              </button>
            </div>

            <div className="action-grid">
              {actionCopy.map((item) => (
                <button
                  key={item.action}
                  className="action-card"
                  onClick={() => void handleAction(item.action)}
                  disabled={pendingAction !== null}
                >
                  <div className="action-title-row">
                    <strong>{item.label}</strong>
                    <span>{pendingAction === item.action ? "Working..." : "Action"}</span>
                  </div>
                  <p>{item.hint}</p>
                </button>
              ))}
            </div>

            <div className="rules-note">
              <p>
                Vitals decay every {pet?.tick_interval_seconds ?? 5} seconds. Offline decay is capped at 8 hours.
                Evolution is permanent once ChuChu earns it through sustained good care, and quick recovery combos can
                still save an active evolution run.
              </p>
            </div>
          </section>
        </section>
      </div>
    </main>
  );
}
