import { Board } from "@/components/Board";

// TODO: replace with a project-picker once the /projects UI is built.
const DEFAULT_PROJECT_ID = 1;

function App() {
  return (
    <main>
      <header style={{ padding: "1rem 1.5rem", borderBottom: "1px solid #e5e7eb" }}>
        <h1 style={{ margin: 0, fontSize: "1.25rem" }}>DevTrack</h1>
      </header>
      <Board projectId={DEFAULT_PROJECT_ID} />
    </main>
  );
}

export default App;
