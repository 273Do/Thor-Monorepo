"use client";

import type { Control, UseFormRegister } from "react-hook-form";
import { Controller } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";

import type { SurveyAnswers } from "~/core/survey-schema";

type props = {
  /**
   * フォームコントロール
   */
  control: Control<SurveyAnswers>;
  /**
   * フォームフィールドの登録関数
   */
  register: UseFormRegister<SurveyAnswers>;
};

export const SurveyForm = ({ control, register }: props) => {
  const { t } = useTranslation();
  const q1Options = t("survey.q1Options", { returnObjects: true }) as string[];
  const q2Options = t("survey.q2Options", { returnObjects: true }) as string[];

  return (
    <div className="flex flex-col gap-8">
      {/* Question 1 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          {t("survey.q1")}
        </Label>
        <Controller
          name="chargingBeforeBedAnswer"
          control={control}
          render={({ field }) => (
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger className="w-full bg-card text-foreground">
                <SelectValue placeholder={t("survey.placeholder")} />
              </SelectTrigger>
              <SelectContent>
                {q1Options.map((value, i) => (
                  <SelectItem key={i} value={String(i)}>
                    {value}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
      </fieldset>

      {/* Question 2 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          {t("survey.q2")}
        </Label>
        <Controller
          name="carryingASmartphoneAnswer"
          control={control}
          render={({ field }) => (
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger className="w-full bg-card text-foreground">
                <SelectValue placeholder={t("survey.placeholder")} />
              </SelectTrigger>
              <SelectContent>
                {q2Options.map((value, i) => (
                  <SelectItem key={i} value={String(i)}>
                    {value}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
      </fieldset>

      {/* Question 3 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          {t("survey.q3")}
        </Label>
        <Input
          type="time"
          className="w-full cursor-pointer"
          {...register("bedtime")}
        />
      </fieldset>
    </div>
  );
};
