"use client";

import { useTranslation } from "react-i18next";

import { Moon, Clock } from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

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

import { AIFeedback } from "./ai-feedback";

import {
  calcAverageTime,
  numberToTime,
  toChartData,
} from "~/lib/time-functions";
import type { DailyEstimateSleepRecord } from "~/utils/types";

type props = {
  /**
   * id
   */
  id: string;
  /**
   * 解析結果
   */
  data: DailyEstimateSleepRecord[];
  /**
   * フィードバックに使用できる LLM の種類
   */
  models: string[];
};

export const ResultsView = ({ id, data, models }: props) => {
  const { t } = useTranslation();

  const sleepChartConfig: ChartConfig = {
    sleepHours: {
      label: t("results.sleepChart.title"),
      color: "var(--primary)",
    },
  };

  const bedtimeWaketimeChartConfig: ChartConfig = {
    bedtime: {
      label: t("results.bedtimeChart.bedtime"),
      color: "var(--primary)",
    },
    waketime: {
      label: t("results.bedtimeChart.waketime"),
      color: "var(--muted-foreground)",
    },
  };

  const chartData = toChartData(data);

  // 平均睡眠時間の計算（これは単純な算術平均でOK）
  const avgSleepHours =
    chartData.length > 0
      ? (
          chartData.reduce((sum, d) => sum + d.sleepHours, 0) / chartData.length
        ).toFixed(1)
      : "–";

  // 平均就寝時刻の計算（循環を考慮）
  const avgBedtime =
    chartData.length > 0
      ? numberToTime(calcAverageTime(chartData.map((d) => d.bedtime)))
      : "–";

  // 平均起床時刻の計算（循環を考慮）
  const avgWakeime =
    chartData.length > 0
      ? numberToTime(calcAverageTime(chartData.map((d) => d.waketime)))
      : "–";

  return (
    <div className="flex flex-col gap-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-5 gap-4">
        <Card className="col-span-2 justify-center">
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <Moon className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">
                {t("results.avgSleepHours")}
              </p>
              <p className="text-xl font-bold text-foreground">
                {avgSleepHours}
                <span className="text-sm font-normal text-muted-foreground">
                  {" "}
                  {t("results.hours")}
                </span>
              </p>
            </div>
          </CardContent>
        </Card>
        <Card className="col-span-3 justify-center">
          <CardContent className="flex items-center gap-3 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <Clock className="h-5 w-5 text-primary" />
            </div>
            <div className="flex gap-4">
              <div>
                <p className="text-xs text-muted-foreground">
                  {t("results.avgBedtime")}
                </p>
                <p className="text-xl font-bold text-foreground">
                  {avgBedtime}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">
                  {t("results.avgWaketime")}
                </p>
                <p className="text-xl font-bold text-foreground">
                  {avgWakeime}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bedtime & Waketime Line Chart */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">
            {t("results.bedtimeChart.title")}
          </CardTitle>
          <CardDescription>
            {t("results.bedtimeChart.description")}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer
            config={bedtimeWaketimeChartConfig}
            className="h-[200px] w-full"
          >
            <LineChart data={chartData} accessibilityLayer>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
              />
              <YAxis
                // データの最小値から -1時間、最大値から +1時間の範囲に自動設定
                domain={([dataMin, dataMax]) => {
                  const min = Math.floor(dataMin - 1);
                  const max = Math.ceil(dataMax + 1);
                  return [min, max];
                }}
                reversed
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                interval="preserveStartEnd"
                tickFormatter={(v: number) => numberToTime(v)}
              />
              <ChartTooltip
                content={
                  <ChartTooltipContent
                    indicator="dot"
                    formatter={(value, name, item) => (
                      <>
                        <div
                          className="size-2.5 shrink-0 rounded-[2px]"
                          style={{ backgroundColor: item.color }}
                        />
                        <span className="text-muted-foreground">
                          {name === "bedtime"
                            ? t("results.bedtimeChart.bedtime")
                            : t("results.bedtimeChart.waketime")}
                        </span>
                        <span className="ml-auto font-mono font-medium text-foreground tabular-nums">
                          {numberToTime(Number(value))}
                        </span>
                      </>
                    )}
                  />
                }
              />
              <Line
                type="monotone"
                dataKey="bedtime"
                stroke="var(--color-bedtime)"
                strokeWidth={1}
                dot={{ fill: "var(--color-bedtime)", r: 2.5 }}
              />
              <Line
                type="monotone"
                dataKey="waketime"
                stroke="var(--color-waketime)"
                strokeWidth={1}
                dot={{ fill: "var(--color-waketime)", r: 2.5 }}
              />
            </LineChart>
          </ChartContainer>
        </CardContent>
      </Card>

      {/* Sleep Duration Bar Chart */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">
            {t("results.sleepChart.title")}
          </CardTitle>
          <CardDescription>
            {t("results.sleepChart.description")}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={sleepChartConfig} className="h-50 w-full">
            <BarChart data={chartData} accessibilityLayer>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
              />
              <YAxis
                domain={[0, (dataMax: number) => Math.ceil(dataMax + 1)]}
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(v: number) => `${v}h`}
              />
              <ChartTooltip
                content={
                  <ChartTooltipContent
                    indicator="dot"
                    formatter={(value, _name, item) => (
                      <>
                        <div
                          className="size-2.5 shrink-0 rounded-[2px]"
                          style={{ backgroundColor: item.color }}
                        />
                        <span className="text-muted-foreground">
                          {t("results.sleepChart.sleep")}
                        </span>
                        <span className="ml-auto font-mono font-medium text-foreground tabular-nums">
                          {Number(value).toFixed(1)}
                          {t("results.hours")}
                        </span>
                      </>
                    )}
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

      <Separator />

      {/* AI Feedback */}
      <AIFeedback id={id} models={models} />
    </div>
  );
};
