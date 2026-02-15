"use client";

import { Label } from "~/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";

export type SurveyAnswers = {
  sleepQuality: string;
  caffeineIntake: string;
  screenTime: string;
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
          Q1. 最近の睡眠の質をどう感じていますか？
        </Label>
      </fieldset>

      {/* Question 2 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q2. 1日のカフェイン摂取量はどのくらいですか？
        </Label>
        <Select
          value={answers.caffeineIntake}
          onValueChange={(v) => onChange({ ...answers, caffeineIntake: v })}
        >
          <SelectTrigger className="w-full bg-card text-foreground">
            <SelectValue placeholder="選択してください" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="none">飲まない</SelectItem>
            <SelectItem value="1-2">1〜2杯</SelectItem>
            <SelectItem value="3-4">3〜4杯</SelectItem>
            <SelectItem value="5+">5杯以上</SelectItem>
          </SelectContent>
        </Select>
      </fieldset>

      {/* Question 3 */}
      <fieldset className="flex flex-col gap-3">
        <Label className="text-sm font-semibold text-foreground">
          Q3. 就寝前のスクリーンタイムはどのくらいですか？
        </Label>
        <Select
          value={answers.screenTime}
          onValueChange={(v) => onChange({ ...answers, screenTime: v })}
        >
          <SelectTrigger className="w-full bg-card text-foreground">
            <SelectValue placeholder="選択してください" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="none">ほぼなし</SelectItem>
            <SelectItem value="30min">30分未満</SelectItem>
            <SelectItem value="1hour">30分〜1時間</SelectItem>
            <SelectItem value="2hour+">1時間以上</SelectItem>
          </SelectContent>
        </Select>
      </fieldset>
    </div>
  );
}
