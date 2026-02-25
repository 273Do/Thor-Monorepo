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
import { LocaleSwitcher } from "~/components/locale-switcher";
import { ResultsView } from "~/components/result-view";
import { SurveyForm } from "~/components/survey-form";
import { DEFAULT_EXTRACT_STEP_QUERY } from "~/core/constants";
import {
  defaultSurveyValues,
  surveySchema,
  type SurveyAnswers,
} from "~/core/survey-schema";
import { useEstimateSleep } from "~/utils/use-estimate-sleep";
import { useExtractSteps } from "~/utils/use-extract-steps";

const Home = () => {
  const [file, setFile] = useState<File | null>(null);

  const {
    control,
    register,
    getValues,
    formState: { isValid },
  } = useForm<SurveyAnswers>({
    resolver: zodResolver(surveySchema),
    defaultValues: defaultSurveyValues,
    mode: "onChange",
  });

  // 歩数データ抽出処理
  const { extractStepTrigger, isExtractStepMutating, extractSteData } =
    useExtractSteps(DEFAULT_EXTRACT_STEP_QUERY);

  // 睡眠状態推定処理
  const { estimateSleepTrigger, isEstimateSleepMutating, estimateSleepData } =
    useEstimateSleep();

  const isLoading = isExtractStepMutating || isEstimateSleepMutating;
  const isFormComplete = isValid && file;

  // 処理リクエスト
  const handleSubmit = async () => {
    if (!isFormComplete) return;

    try {
      const extractStepResult = await extractStepTrigger(file);

      const { id, step_data } = extractStepResult;

      const surveyValues = getValues();

      let bedtime_answer;

      if (surveyValues.bedtime > "03:00" && surveyValues.bedtime < "20:45") {
        bedtime_answer = 1;
      } else bedtime_answer = 0;

      const result = await estimateSleepTrigger({
        id,
        step_data,
        answers: {
          charging_before_bed_answer: Number(
            surveyValues.chargingBeforeBedAnswer
          ),
          carrying_a_smartphone_answer: Number(
            surveyValues.carryingASmartphoneAnswer
          ),
          bedtime_answer,
        },
      });

      console.log(result);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-lg px-4 py-8 md:py-12">
        {/* Header */}
        <Header />

        {/* Input State */}
        {!estimateSleepData && !isLoading && (
          <div className="flex flex-col gap-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between">
                  <div>
                    <CardTitle className="text-base">アンケート</CardTitle>
                    <CardDescription>
                      睡眠に関する3つの質問にお答えください
                    </CardDescription>
                  </div>
                  <LocaleSwitcher />
                </div>
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
        {isLoading && (
          <Loading
            status={
              isExtractStepMutating
                ? "extract"
                : isEstimateSleepMutating
                  ? "estimate"
                  : "feedback"
            }
          />
        )}

        {/* Results State */}
        {extractSteData && estimateSleepData && !isLoading && (
          <ResultsView
            id={extractSteData.id}
            data={estimateSleepData.data}
            models={estimateSleepData.models}
          />
        )}
      </div>
    </main>
  );
};

export default Home;
