export type PetStatus = "normal" | "sick" | "evolved";
export type PetAction = "feed" | "play" | "rest";

export interface PetState {
  id: number;
  name: string;
  hunger: number;
  happiness: number;
  energy: number;
  status: PetStatus;
  last_reaction: string;
  last_updated_at: string;
  healthy_streak: number;
  total_ticks: number;
  needs_attention: boolean;
  critical_vitals: string[];
  evolution_progress: number;
  evolution_target: number;
  tick_interval_seconds: number;
}
