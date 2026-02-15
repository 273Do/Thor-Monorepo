"use client";

import { Moon, Clock, Brain } from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

import { Button } from "~/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "~/components/ui/chart";
import { Separator } from "~/components/ui/separator";

import type { SurveyAnswers } from "./survey-form";

// Generate mock sleep data for 7 days
function generateSleepData(answers: SurveyAnswers) {
  const days = ["月", "火", "水", "木", "金", "土", "日"];

  const qualityOffset =
    answers.sleepQuality === "good"
      ? 0.5
      : answers.sleepQuality === "bad"
        ? -0.8
        : 0;
  const caffeineOffset =
    answers.caffeineIntake === "none"
      ? 0.3
      : answers.caffeineIntake === "5+"
        ? -0.6
        : answers.caffeineIntake === "3-4"
          ? -0.3
          : 0;
  const screenOffset =
    answers.screenTime === "none"
      ? 0.2
      : answers.screenTime === "2hour+"
        ? -0.5
        : answers.screenTime === "1hour"
          ? -0.2
          : 0;

  return days.map((day) => {
    const baseSleep = 6.5 + qualityOffset + caffeineOffset + screenOffset;
    const variance = (Math.random() - 0.5) * 1.5;
    const sleepHours = Math.max(4, Math.min(9, baseSleep + variance));

    const baseBedtime = 23.5 - screenOffset * 0.5;
    const bedtimeVariance = (Math.random() - 0.5) * 1.5;
    const bedtime = Math.max(22, Math.min(26, baseBedtime + bedtimeVariance));

    return {
      day,
      sleepHours: Math.round(sleepHours * 10) / 10,
      bedtime: Math.round(bedtime * 10) / 10,
      bedtimeLabel: formatBedtime(
        Math.round((baseBedtime + bedtimeVariance) * 10) / 10
      ),
    };
  });
}

function formatBedtime(hours: number): string {
  const h = Math.floor(hours) % 24;
  const m = Math.round((hours % 1) * 60);
  return `${h}:${m.toString().padStart(2, "0")}`;
}

function generateFeedback(answers: SurveyAnswers): string {
  const feedbacks: string[] = [];

  if (answers.sleepQuality === "bad") {
    feedbacks.push(
      "睡眠の質が低下している可能性があります。就寝・起床時刻を一定に保つことを心がけましょう。"
    );
  } else if (answers.sleepQuality === "good") {
    feedbacks.push(
      "睡眠の質は良好な状態です。この調子を維持していきましょう。"
    );
  } else {
    feedbacks.push(
      "睡眠の質は平均的です。少しの改善で大きな変化が期待できます。"
    );
  }

  if (answers.caffeineIntake === "3-4" || answers.caffeineIntake === "5+") {
    feedbacks.push(
      "カフェイン摂取量が多いため、午後3時以降のカフェインを控えることで、入眠がスムーズになる可能性があります。"
    );
  }

  if (answers.screenTime === "1hour" || answers.screenTime === "2hour+") {
    feedbacks.push(
      "就寝前のスクリーンタイムが長い傾向にあります。ブルーライトは睡眠ホルモン（メラトニン）の分泌を抑制するため、就寝30分前にはデバイスを手放すことをおすすめします。"
    );
  }

  feedbacks.push(
    "ヘルスデータの分析から、週の後半にかけて睡眠時間が短くなる傾向が見られます。週末に睡眠負債を貯めないよう、平日から十分な睡眠時間を確保しましょう。"
  );

  return feedbacks.join("\n\n");
}

const sleepChartConfig: ChartConfig = {
  sleepHours: {
    label: "睡眠時間",
    color: "hsl(var(--chart-1))",
  },
};

const bedtimeChartConfig: ChartConfig = {
  bedtime: {
    label: "就寝時刻",
    color: "hsl(var(--chart-2))",
  },
};

type ResultsViewProps = {
  answers: SurveyAnswers;
  onReset: () => void;
};

export function ResultsView({ answers, onReset }: ResultsViewProps) {
  const data = generateSleepData(answers);
  const feedback = generateFeedback(answers);
  const avgSleep =
    Math.round(
      (data.reduce((sum, d) => sum + d.sleepHours, 0) / data.length) * 10
    ) / 10;
  const avgBedtime = data.reduce((sum, d) => sum + d.bedtime, 0) / data.length;

  return (
    <div className="flex flex-col gap-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <Moon className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">平均睡眠時間</p>
              <p className="text-xl font-bold text-foreground">
                {avgSleep}
                <span className="text-sm font-normal text-muted-foreground">
                  {" "}
                  時間
                </span>
              </p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent/10">
              <Clock className="h-5 w-5 text-accent" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">平均就寝時刻</p>
              <p className="text-xl font-bold text-foreground">
                {formatBedtime(avgBedtime)}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sleep Duration Chart */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">睡眠時間（過去7日間）</CardTitle>
          <CardDescription>1日あたりの睡眠時間の推移</CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer
            config={sleepChartConfig}
            className="h-[200px] w-full"
          >
            <BarChart data={data} accessibilityLayer>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis
                dataKey="day"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
              />
              <YAxis
                domain={[0, 10]}
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(v) => `${v}h`}
              />
              <ChartTooltip
                content={
                  <ChartTooltipContent
                    formatter={(value) => [`${value} 時間`, "睡眠時間"]}
                  />
                }
              />
              <Bar
                dataKey="sleepHours"
                fill="var(--color-sleepHours)"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>

      {/* Bedtime Chart */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">就寝時刻（過去7日間）</CardTitle>
          <CardDescription>就寝時刻の推移</CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer
            config={bedtimeChartConfig}
            className="h-[200px] w-full"
          >
            <LineChart data={data} accessibilityLayer>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis
                dataKey="day"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
              />
              <YAxis
                domain={[22, 26]}
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(v) => {
                  const h = Math.floor(v) % 24;
                  return `${h}:00`;
                }}
                reversed
              />
              <ChartTooltip
                content={
                  <ChartTooltipContent
                    formatter={(value) => {
                      const v = Number(value);
                      const h = Math.floor(v) % 24;
                      const m = Math.round((v % 1) * 60);
                      return [
                        `${h}:${m.toString().padStart(2, "0")}`,
                        "就寝時刻",
                      ];
                    }}
                  />
                }
              />
              <Line
                type="monotone"
                dataKey="bedtime"
                stroke="var(--color-bedtime)"
                strokeWidth={2}
                dot={{
                  fill: "var(--color-bedtime)",
                  r: 4,
                }}
              />
            </LineChart>
          </ChartContainer>
        </CardContent>
      </Card>

      <Separator />

      {/* AI Feedback */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <Brain className="h-4 w-4 text-primary" />
            </div>
            <CardTitle className="text-base">AI フィードバック</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-sm leading-relaxed whitespace-pre-line text-foreground/80">
            {feedback}
          </div>
        </CardContent>
      </Card>

      {/* Reset */}
      <Button variant="outline" onClick={onReset} className="w-full">
        もう一度分析する
      </Button>
    </div>
  );
}
