// Shared TypeScript interfaces and type aliases — mirrors backend Pydantic schemas.

export type IssueStatus = "open" | "in_progress" | "closed";
export type IssuePriority = "low" | "medium" | "high" | "critical";
export type UserRole = "admin" | "member";

export const ISSUE_STATUSES: IssueStatus[] = ["open", "in_progress", "closed"];
export const ISSUE_STATUS_LABELS: Record<IssueStatus, string> = {
  open: "Open",
  in_progress: "In Progress",
  closed: "Closed",
};

export const ISSUE_PRIORITIES: IssuePriority[] = ["low", "medium", "high", "critical"];

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string | null;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface Issue {
  id: number;
  title: string;
  description: string | null;
  status: IssueStatus;
  priority: IssuePriority;
  project_id: number;
  assignee_id: number | null;
  assignee: User | null;
  created_at: string;
  updated_at: string;
}

export interface IssueCreate {
  title: string;
  description?: string;
  status?: IssueStatus;
  priority?: IssuePriority;
  project_id: number;
  assignee_id?: number | null;
}

export interface IssueStatusUpdate {
  status: IssueStatus;
}

export interface ApiError {
  detail: string;
}
