import type { Issue, IssueStatus } from "@/types";

interface IssueCardProps {
  issue: Issue;
  onStatusChange: (id: number, status: IssueStatus) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

const PRIORITY_BADGE: Record<Issue["priority"], string> = {
  low: "priority-low",
  medium: "priority-medium",
  high: "priority-high",
  critical: "priority-critical",
};

const NEXT_STATUS: Partial<Record<IssueStatus, IssueStatus>> = {
  open: "in_progress",
  in_progress: "closed",
};

export function IssueCard({ issue, onStatusChange, onDelete }: IssueCardProps) {
  const next = NEXT_STATUS[issue.status];

  function handleAdvance() {
    if (next) {
      onStatusChange(issue.id, next).catch(() => {
        // error surface handled by parent via hook's error state
      });
    }
  }

  function handleDelete() {
    if (!window.confirm(`Delete "${issue.title}"?`)) return;
    onDelete(issue.id).catch(() => {
      // error surface handled by parent via hook's error state
    });
  }

  return (
    <article className="issue-card">
      <header className="issue-card__header">
        <span className={`issue-card__priority ${PRIORITY_BADGE[issue.priority]}`}>
          {issue.priority}
        </span>
        <button
          className="issue-card__delete"
          onClick={handleDelete}
          aria-label={`Delete issue "${issue.title}"`}
          title="Delete"
        >
          ✕
        </button>
      </header>

      <h3 className="issue-card__title">{issue.title}</h3>

      {issue.description && (
        <p className="issue-card__description">{issue.description}</p>
      )}

      {issue.assignee && (
        <p className="issue-card__assignee">👤 {issue.assignee.full_name}</p>
      )}

      {next && (
        <button
          className="issue-card__advance"
          onClick={handleAdvance}
          aria-label={`Move to ${next.replace("_", " ")}`}
        >
          Move to {next.replace("_", " ")}
        </button>
      )}
    </article>
  );
}
