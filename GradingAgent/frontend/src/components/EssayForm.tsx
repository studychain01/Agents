import { useState } from "react";

type Props = {
  onSubmit: (essay: string) => Promise<void> | void;
  loading?: boolean;
};

export default function EssayForm({ onSubmit, loading }: Props) {
  const [text, setText] = useState("");

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium">Paste your essay</label>
      <textarea
        className="w-full h-48 p-3 border rounded-lg focus:outline-none"
        placeholder="Write or paste your essay here…"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div className="flex gap-2">
        <button
          onClick={() => onSubmit(text)}
          disabled={loading || !text.trim()}
          className="px-4 py-2 rounded-lg bg-black text-white disabled:opacity-50"
        >
          {loading ? "Grading…" : "Grade Essay"}
        </button>
        <button
          onClick={() => setText("")}
          className="px-4 py-2 rounded-lg border"
          type="button"
        >
          Clear
        </button>
      </div>
    </div>
  );
}
