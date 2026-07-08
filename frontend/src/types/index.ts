// Shared TypeScript interfaces and type aliases used across the app.

export interface Issue {
  id: number;
  title: string;
  description: string | null;
  status: "open" | "in_progress" | "closed";
  created_at: string;
  updated_at: string;
}
