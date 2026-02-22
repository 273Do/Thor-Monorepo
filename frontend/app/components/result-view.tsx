"use client";

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

const sleepChartConfig: ChartConfig = {
  sleepHours: {
    label: "睡眠時間",
    color: "var(--primary)",
  },
};

const bedtimeWaketimeChartConfig: ChartConfig = {
  bedtime: {
    label: "就寝時刻",
    color: "var(--primary)",
  },
  waketime: {
    label: "起床時刻",
    color: "var(--muted-foreground)",
  },
};

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
              <p className="text-xs text-muted-foreground">平均睡眠時間</p>
              <p className="text-xl font-bold text-foreground">
                {avgSleepHours}
                <span className="text-sm font-normal text-muted-foreground">
                  {" "}
                  時間
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
                <p className="text-xs text-muted-foreground">平均就寝</p>
                <p className="text-xl font-bold text-foreground">
                  {avgBedtime}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">平均起床</p>
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
          <CardTitle className="text-base">就寝・起床時刻</CardTitle>
          <CardDescription>就寝時刻と起床時刻の推移</CardDescription>
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
                          {name === "bedtime" ? "就寝時刻" : "起床時刻"}
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
          <CardTitle className="text-base">睡眠時間</CardTitle>
          <CardDescription>1日あたりの睡眠時間の推移</CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer
            config={sleepChartConfig}
            className="h-[200px] w-full"
          >
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
                        <span className="text-muted-foreground">睡眠</span>
                        <span className="ml-auto font-mono font-medium text-foreground tabular-nums">
                          {Number(value).toFixed(1)}時間
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
