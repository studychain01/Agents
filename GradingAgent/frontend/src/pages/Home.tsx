import { useState } from "react";
import EssayForm from "../components/EssayForm";
import ScoreCard from "../components/ScoreCard";
import { gradeEssay } from "../api/client";
import { EssayResponse } from "../types/grading";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EssayResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(essay: string) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await gradeEssay(essay);
      setResult(data as EssayResponse);
    } catch (e: any) {
      setError(e.message ?? "Failed to grade essay.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Essay Grading</h1>
      <EssayForm onSubmit={handleSubmit} loading={loading} />
      {error && <div className="text-red-600">{error}</div>}
      {result && <ScoreCard data={result} />}
    </div>
  );
}
