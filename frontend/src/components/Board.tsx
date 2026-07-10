import { useIssues } from "@/hooks/useIssues";
import { IssueCard } from "@/components/IssueCard";
import { NewIssueForm } from "@/components/NewIssueForm";
import {
  ISSUE_STATUSES,
  ISSUE_STATUS_LABELS,
  type Issue,
  type IssueStatus,
} from "@/types";

interface BoardProps {
  projectId: number;
}

type IssuesByStatus = Record<IssueStatus, Issue[]>;

function groupByStatus(issues: Issue[]): IssuesByStatus {
  return issues.reduce<IssuesByStatus>(
    (acc, issue) => {
      acc[issue.status].push(issue);
      return acc;
    },
    { open: [], in_progress: [], closed: [] }
  );
}

export function Board({ projectId }: BoardProps) {
  const { issues, loading, error, createIssue, updateStatus, deleteIssue } =
    useIssues({ projectId });

  const columns = groupByStatus(issues);

  return (
    <div className="board">
      <aside className="board__sidebar">
        <NewIssueForm projectId={projectId} onSubmit={createIssue} />
      </aside>

      <section className="board__columns" aria-label="Issue board">
        {loading && <p className="board__loading" aria-live="polite">Loading…</p>}
        {error && (
          <p className="board__error" role="alert">
            {error}
          </p>
        )}

        {ISSUE_STATUSES.map((status) => (
          <div key={status} className="board__column">
            <h2 className="board__column-heading">
              {ISSUE_STATUS_LABELS[status]}
              <span className="board__column-count">
                {columns[status].length}
              </span>
            </h2>

            <ul className="board__cards" aria-label={`${ISSUE_STATUS_LABELS[status]} issues`}>
              {columns[status].map((issue) => (
                <li key={issue.id}>
                  <IssueCard
                    issue={issue}
                    onStatusChange={updateStatus}
                    onDelete={deleteIssue}
                  />
                </li>
              ))}

              {columns[status].length === 0 && !loading && (
                <li className="board__empty">No issues</li>
              )}
            </ul>
          </div>
        ))}
      </section>
    </div>
  );
}
