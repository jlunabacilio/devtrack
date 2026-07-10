import { useState, type FormEvent } from "react";
import type { IssueCreate, IssuePriority } from "@/types";
import { ISSUE_PRIORITIES } from "@/types";

interface NewIssueFormProps {
  projectId: number;
  onSubmit: (payload: IssueCreate) => Promise<void>;
}

interface FormFields {
  title: string;
  description: string;
  priority: IssuePriority;
}

const DEFAULT_FIELDS: FormFields = {
  title: "",
  description: "",
  priority: "medium",
};

export function NewIssueForm({ projectId, onSubmit }: NewIssueFormProps) {
  const [fields, setFields] = useState<FormFields>(DEFAULT_FIELDS);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    const { name, value } = e.target;
    setFields((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!fields.title.trim()) {
      setError("Title is required");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await onSubmit({
        title: fields.title.trim(),
        description: fields.description.trim() || undefined,
        priority: fields.priority,
        project_id: projectId,
      });
      setFields(DEFAULT_FIELDS);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create issue");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="new-issue-form" onSubmit={handleSubmit} noValidate>
      <h2 className="new-issue-form__heading">New Issue</h2>

      {error && <p className="new-issue-form__error" role="alert">{error}</p>}

      <label className="new-issue-form__label" htmlFor="title">
        Title <span aria-hidden="true">*</span>
      </label>
      <input
        id="title"
        name="title"
        className="new-issue-form__input"
        type="text"
        value={fields.title}
        onChange={handleChange}
        required
        maxLength={500}
        placeholder="Short summary of the issue"
      />

      <label className="new-issue-form__label" htmlFor="description">
        Description
      </label>
      <textarea
        id="description"
        name="description"
        className="new-issue-form__textarea"
        value={fields.description}
        onChange={handleChange}
        rows={3}
        placeholder="Optional details"
      />

      <label className="new-issue-form__label" htmlFor="priority">
        Priority
      </label>
      <select
        id="priority"
        name="priority"
        className="new-issue-form__select"
        value={fields.priority}
        onChange={handleChange}
      >
        {ISSUE_PRIORITIES.map((p) => (
          <option key={p} value={p}>
            {p.charAt(0).toUpperCase() + p.slice(1)}
          </option>
        ))}
      </select>

      <button
        className="new-issue-form__submit"
        type="submit"
        disabled={submitting}
      >
        {submitting ? "Creating…" : "Create Issue"}
      </button>
    </form>
  );
}
