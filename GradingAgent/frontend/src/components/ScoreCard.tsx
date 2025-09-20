import { EssayResponse } from "../types/grading";

export default function ScoreCard({ data }: { data: EssayResponse }) {
  const rows = [
    ["Relevance", data.relevance_score],
    ["Grammar", data.grammar_score],
    ["Structure", data.structure_score],
    ["Depth", data.depth_score],
    ["Final", data.final_score],
  ];

  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Result</h3>
        <span className="text-2xl font-bold">{data.grade}</span>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
        {rows.map(([label, val]) => (
          <div key={label as string} className="flex justify-between border-b py-1">
            <span>{label}</span>
            <span>{(val as number).toFixed(2)}</span>
          </div>
        ))}
      </div>
      <details className="mt-3">
        <summary className="cursor-pointer text-sm text-gray-600">Essay</summary>
        <pre className="whitespace-pre-wrap text-sm mt-2">{data.essay}</pre>
      </details>
    </div>
  );
}
