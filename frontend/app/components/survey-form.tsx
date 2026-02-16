"use client";

import type { Control, UseFormRegister } from "react-hook-form";
import { Controller } from "react-hook-form";

import { Input } from "~/components/ui/input";
import { Label } from "~/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";

import {
  carryingASmartphoneAnswer,
  chargingBeforeBedAnswer,
} from "~/core/constants";
import type { SurveyAnswers } from "~/core/survey-schema";

type SurveyFormProps = {
  control: Control<SurveyAnswers>;
  register: UseFormRegister<SurveyAnswers>;
};

export function SurveyForm({ control, register }: SurveyFormProps) {
  return (
    <div className="flex flex-col gap-8">
      {/* Question 1 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q1. 就寝何時間前にスマートフォンの充電を始めますか？
        </Label>
        <Controller
          name="chargingBeforeBedAnswer"
          control={control}
          render={({ field }) => (
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger className="w-full bg-card text-foreground">
                <SelectValue placeholder="選択してください" />
              </SelectTrigger>
              <SelectContent>
                {chargingBeforeBedAnswer.map((value, i) => (
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
          Q2. 家の中でスマートフォンを持ち歩きますか？
        </Label>
        <Controller
          name="carryingASmartphoneAnswer"
          control={control}
          render={({ field }) => (
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger className="w-full bg-card text-foreground">
                <SelectValue placeholder="選択してください" />
              </SelectTrigger>
              <SelectContent>
                {carryingASmartphoneAnswer.map((value, i) => (
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
          Q3. 普段は何時ごろに就寝しますか？
        </Label>
        <Input
          type="time"
          className="w-full cursor-pointer"
          {...register("bedtime")}
        />
      </fieldset>
    </div>
  );
}
