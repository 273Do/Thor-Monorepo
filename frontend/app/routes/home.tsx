"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight, Mail } from "lucide-react";

import { Button } from "~/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { Input } from "~/components/ui/input";

import { EmailView } from "~/components/email-view";
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
import type { LanguagesType } from "~/utils/types";
import { useEstimateSleep } from "~/utils/use-estimate-sleep";
import { useExtractSteps } from "~/utils/use-extract-steps";
import { useViaEmail } from "~/utils/use-via-email";

const Home = () => {
  const { t, i18n } = useTranslation();
  const [file, setFile] = useState<File | null>(null);
  const [emailValue, setEmailValue] = useState<string>("");

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

  // email経由の解析処理
  const { viaEmailTrigger } = useViaEmail(DEFAULT_EXTRACT_STEP_QUERY);

  const isLoading = isExtractStepMutating || isEstimateSleepMutating;
  const isFormComplete = isValid && file;

  // 処理リクエスト
  const handleSubmit = async () => {
    if (!isFormComplete) return;

    const {
      chargingBeforeBedAnswer,
      carryingASmartphoneAnswer,
      bedtime,
      email,
    } = getValues();

    setEmailValue(email || "");

    let bedtime_answer;

    if (bedtime > "03:00" && bedtime < "20:45") {
      bedtime_answer = 1;
    } else bedtime_answer = 0;

    if (email) {
      await viaEmailTrigger({
        xmlFile: file,
        req: {
          answers: {
            charging_before_bed_answer: Number(chargingBeforeBedAnswer),
            carrying_a_smartphone_answer: Number(carryingASmartphoneAnswer),
            bedtime_answer,
          },
          lang: i18n.language as LanguagesType,
          email_to: email,
        },
      });
    } else {
      try {
        const extractStepResult = await extractStepTrigger(file);

        const { id, step_data } = extractStepResult;

        await estimateSleepTrigger({
          id,
          step_data,
          answers: {
            charging_before_bed_answer: Number(chargingBeforeBedAnswer),
            carrying_a_smartphone_answer: Number(carryingASmartphoneAnswer),
            bedtime_answer,
          },
        });
      } catch (error) {
        console.error(error);
      }
    }
  };

  return (
    <main className="min-h-screen">
      <div className="mx-auto max-w-lg px-4 py-8 md:py-12">
        {/* Header */}
        <Header />

        {/* Input State */}
        {!estimateSleepData && !isLoading && !emailValue && (
          <div className="flex flex-col gap-6">
            <Card>
              <CardHeader>
                <div className="flex justify-between">
                  <div>
                    <CardTitle className="text-base">
                      {t("survey.title")}
                    </CardTitle>
                    <CardDescription>{t("survey.description")}</CardDescription>
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
                <CardTitle className="text-base">{t("upload.title")}</CardTitle>
                <CardDescription>{t("upload.description")}</CardDescription>
                <CardDescription>{t("upload.privacy")}</CardDescription>
              </CardHeader>
              <CardContent>
                <FileUpload file={file} onFileChange={setFile} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">{t("email.title")}</CardTitle>
                <CardDescription>{t("email.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-2">
                  <div className="relative">
                    <Mail className="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      id="email"
                      type="email"
                      placeholder={t("email.placeholder")}
                      className="bg-card pl-10"
                      {...register("email")}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Button
              size="lg"
              onClick={handleSubmit}
              disabled={!isFormComplete}
              className="w-full gap-2"
            >
              {t("analyzeButton")}
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        )}

        {/* Loading State */}
        {!emailValue && isLoading && (
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

        {/* Email View */}
        {emailValue && <EmailView email={emailValue} />}

        {/* Results State */}
        {extractSteData && estimateSleepData && !emailValue && !isLoading && (
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
