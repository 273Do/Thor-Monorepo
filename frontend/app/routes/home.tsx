"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";
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
import { SurveyForm } from "~/components/survey-form";
import { DEFAULT_EXTRACT_STEP_QUERY } from "~/core/constants";
import {
  defaultSurveyValues,
  surveySchema,
  type SurveyAnswers,
} from "~/core/survey-schema";
import { useExtractSteps } from "~/utils/use-extract-steps";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  const {
    control,
    register,
    reset,
    getValues,
    formState: { isValid },
  } = useForm<SurveyAnswers>({
    resolver: zodResolver(surveySchema),
    defaultValues: defaultSurveyValues,
    mode: "onChange",
  });

  const { trigger, isMutating, data } = useExtractSteps(
    DEFAULT_EXTRACT_STEP_QUERY
  );

  const isFormComplete = isValid && file;

  const handleSubmit = async () => {
    if (!isFormComplete) return;
    await trigger(file);
  };

  const handleReset = () => {
    setFile(null);
    reset(defaultSurveyValues);
  };

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-lg px-4 py-8 md:py-12">
        {/* Header */}
        <Header />

        {/* Input State */}
        {!data && !isMutating && (
          <div className="flex flex-col gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">アンケート</CardTitle>
                <CardDescription>
                  睡眠に関する3つの質問にお答えください
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SurveyForm control={control} register={register} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">
                  ヘルスデータアップロード
                </CardTitle>
                <CardDescription>
                  iPhoneの「ヘルスケア」アプリからエクスポートした XML
                  ファイルをアップロードしてください。
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
        {isMutating && <Loading />}

        {/* Results State */}
        {data && !isMutating && (
          <ResultsView answers={getValues()} onReset={handleReset} />
        )}
      </div>
    </main>
  );
}
