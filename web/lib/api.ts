import type { PetAction, PetState } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8102/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export function fetchPet(): Promise<PetState> {
  return request<PetState>("/pet");
}

export function performAction(action: PetAction): Promise<PetState> {
  return request<PetState>("/pet/actions", {
    method: "POST",
    body: JSON.stringify({ action }),
  });
}

export function resetPet(): Promise<PetState> {
  return request<PetState>("/pet/reset", {
    method: "POST",
  });
}
