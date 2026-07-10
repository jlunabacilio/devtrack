import { useCallback, useEffect, useReducer } from "react";
import { issueService } from "@/services/issueService";
import type { Issue, IssueCreate, IssueStatus } from "@/types";

// ---------------------------------------------------------------------------
// State shape
// ---------------------------------------------------------------------------

interface IssuesState {
  issues: Issue[];
  loading: boolean;
  error: string | null;
}

// ---------------------------------------------------------------------------
// Reducer
// ---------------------------------------------------------------------------

type IssuesAction =
  | { type: "FETCH_START" }
  | { type: "FETCH_SUCCESS"; payload: Issue[] }
  | { type: "FETCH_ERROR"; payload: string }
  | { type: "UPSERT"; payload: Issue }
  | { type: "REMOVE"; payload: number };

function reducer(state: IssuesState, action: IssuesAction): IssuesState {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true, error: null };
    case "FETCH_SUCCESS":
      return { issues: action.payload, loading: false, error: null };
    case "FETCH_ERROR":
      return { ...state, loading: false, error: action.payload };
    case "UPSERT": {
      const exists = state.issues.some((i) => i.id === action.payload.id);
      const issues = exists
        ? state.issues.map((i) => (i.id === action.payload.id ? action.payload : i))
        : [action.payload, ...state.issues];
      return { ...state, issues };
    }
    case "REMOVE":
      return { ...state, issues: state.issues.filter((i) => i.id !== action.payload) };
    default:
      return state;
  }
}

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

interface UseIssuesOptions {
  projectId?: number;
  status?: IssueStatus;
}

interface UseIssuesReturn {
  issues: Issue[];
  loading: boolean;
  error: string | null;
  createIssue: (payload: IssueCreate) => Promise<void>;
  updateStatus: (id: number, status: IssueStatus) => Promise<void>;
  deleteIssue: (id: number) => Promise<void>;
  refresh: () => void;
}

export function useIssues({ projectId, status }: UseIssuesOptions = {}): UseIssuesReturn {
  const [state, dispatch] = useReducer(reducer, {
    issues: [],
    loading: false,
    error: null,
  });

  const fetch = useCallback(() => {
    dispatch({ type: "FETCH_START" });
    issueService
      .list(projectId, status)
      .then((data) => dispatch({ type: "FETCH_SUCCESS", payload: data }))
      .catch((err: unknown) =>
        dispatch({
          type: "FETCH_ERROR",
          payload: err instanceof Error ? err.message : "Unknown error",
        })
      );
  }, [projectId, status]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const createIssue = useCallback(
    async (payload: IssueCreate): Promise<void> => {
      const issue = await issueService.create(payload);
      dispatch({ type: "UPSERT", payload: issue });
    },
    []
  );

  const updateStatus = useCallback(
    async (id: number, newStatus: IssueStatus): Promise<void> => {
      const issue = await issueService.updateStatus(id, { status: newStatus });
      dispatch({ type: "UPSERT", payload: issue });
    },
    []
  );

  const deleteIssue = useCallback(async (id: number): Promise<void> => {
    await issueService.delete(id);
    dispatch({ type: "REMOVE", payload: id });
  }, []);

  return {
    issues: state.issues,
    loading: state.loading,
    error: state.error,
    createIssue,
    updateStatus,
    deleteIssue,
    refresh: fetch,
  };
}
