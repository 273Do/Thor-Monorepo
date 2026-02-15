"use client";

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

export type SurveyAnswers = {
  chargingBeforeBedAnswer: string;
  carryingASmartphoneAnswer: string;
  bedtime: string;
};

type SurveyFormProps = {
  answers: SurveyAnswers;
  onChange: (answers: SurveyAnswers) => void;
};

export function SurveyForm({ answers, onChange }: SurveyFormProps) {
  return (
    <div className="flex flex-col gap-8">
      {/* Question 1 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q1. 就寝何時間前にスマートフォンの充電を始めますか？
        </Label>
        <Select
          value={answers.chargingBeforeBedAnswer}
          onValueChange={(v) =>
            onChange({ ...answers, chargingBeforeBedAnswer: v })
          }
        >
          <SelectTrigger className="w-full bg-card text-foreground">
            <SelectValue placeholder="選択してください" />
          </SelectTrigger>
          <SelectContent>
            {chargingBeforeBedAnswer.map((value, i) => (
              <SelectItem value={String(i)}>{value}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </fieldset>

      {/* Question 2 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q2. 家の中でスマートフォンを持ち歩きますか？
        </Label>
        <Select
          value={answers.carryingASmartphoneAnswer}
          onValueChange={(v) =>
            onChange({ ...answers, carryingASmartphoneAnswer: v })
          }
        >
          <SelectTrigger className="w-full bg-card text-foreground">
            <SelectValue placeholder="選択してください" />
          </SelectTrigger>
          <SelectContent>
            {carryingASmartphoneAnswer.map((value, i) => (
              <SelectItem value={String(i)}>{value}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </fieldset>

      {/* Question 3 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q3. 普段は何時ごろに就寝しますか？
        </Label>
        <Input type="time" className="w-1/3 cursor-pointer" />
      </fieldset>
    </div>
  );
}
