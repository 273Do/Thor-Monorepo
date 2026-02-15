"use client";

import { useState } from "react";

import { ArrowRight } from "lucide-react";

import { Button } from "~/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";

import { FileUpload } from "~/components/file-upload";
import { Header } from "~/components/header";
import { Loading } from "~/components/loading";
import { ResultsView } from "~/components/result-view";
import { SurveyForm, type SurveyAnswers } from "~/components/survey-form";

type AppState = "input" | "loading" | "results";

export default function Home() {
  const [state, setState] = useState<AppState>("input");
  const [answers, setAnswers] = useState<SurveyAnswers>({
    sleepQuality: "",
    caffeineIntake: "",
    screenTime: "",
  });
  const [file, setFile] = useState<File | null>(null);

  const isFormComplete =
    // answers.sleepQuality &&
    answers.caffeineIntake && answers.screenTime && file;

  const handleSubmit = () => {
    if (!isFormComplete) return;
    setState("loading");
    // Simulate analysis processing
    setTimeout(() => {
      setState("results");
    }, 2000);
  };

  const handleReset = () => {
    setState("input");
    setAnswers({ sleepQuality: "", caffeineIntake: "", screenTime: "" });
    setFile(null);
  };

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-lg px-4 py-8 md:py-12">
        {/* Header */}
        <Header />

        {/* Input State */}
        {state === "input" && (
          <div className="flex flex-col gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">アンケート</CardTitle>
                <CardDescription>
                  睡眠に関する3つの質問にお答えください
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SurveyForm answers={answers} onChange={setAnswers} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">データアップロード</CardTitle>
                <CardDescription>
                  iPhoneからエクスポートしたヘルスデータを添付してください。
                </CardDescription>
              </CardHeader>
              <CardContent>
                <FileUpload file={file} onFileChange={setFile} />
              </CardContent>
            </Card>

            <Button
              size="lg"
              onClick={handleSubmit}
              disabled={!isFormComplete}
              className="w-full gap-2"
            >
              分析を開始する
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        )}

        {/* Loading State */}
        {state === "loading" && <Loading />}

        {/* Results State */}
        {state === "results" && (
          <ResultsView answers={answers} onReset={handleReset} />
        )}
      </div>
    </main>
  );
}
