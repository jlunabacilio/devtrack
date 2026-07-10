import type { Issue, IssueCreate, IssueStatus, IssueStatusUpdate } from "@/types";

const BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(
      typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail)
    );
  }

  // 204 No Content — return nothing
  if (res.status === 204) return undefined as T;

  return res.json() as Promise<T>;
}

export const issueService = {
  list(projectId?: number, status?: IssueStatus): Promise<Issue[]> {
    const params = new URLSearchParams();
    if (projectId !== undefined) params.set("project_id", String(projectId));
    if (status !== undefined) params.set("status", status);
    const qs = params.size > 0 ? `?${params.toString()}` : "";
    return request<Issue[]>(`/issues${qs}`);
  },

  create(payload: IssueCreate): Promise<Issue> {
    return request<Issue>("/issues", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  updateStatus(id: number, payload: IssueStatusUpdate): Promise<Issue> {
    return request<Issue>(`/issues/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    });
  },

  delete(id: number): Promise<void> {
    return request<void>(`/issues/${id}`, { method: "DELETE" });
  },
};
