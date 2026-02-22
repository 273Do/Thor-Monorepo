import type { DailyEstimateSleepRecord } from "~/utils/types";

/**
 * "HH:MM" 形式の時刻を 00:00 中心の数値に変換する
 * @param time 時間
 */
const timeToNumber = (time: string): number => {
  const [h, m] = time.split(":").map(Number);
  return (h >= 20 ? h - 24 : h) + m / 60;
};

/**
 * 数値を "HH:MM" 形式に戻す
 * @param v 時刻の数値表現
 */
export const numberToTime = (v: number): string => {
  const totalMinutes = Math.round(((v % 24) + 24) * 60) % (24 * 60);
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
};

/**
 * 睡眠時間（時間）を計算する
 * @param bed 就寝時刻
 * @param wake 起床時刻
 */
export const calcSleepHours = (bed: string, wake: string): number => {
  const bedNum = timeToNumber(bed);
  const wakeNum = timeToNumber(wake);
  const diff = wakeNum - bedNum;
  return diff < 0 ? diff + 24 : diff;
};

/**
 * 時刻（数値）の配列から、循環を考慮した平均時刻を計算する
 * @param times 時刻の数値配列
 */
export const calcAverageTime = (times: number[]): number => {
  if (times.length === 0) return 0;
  const base = times[0]!;
  const relativeSum = times.reduce((sum, t) => {
    let diff = t - base;
    if (diff > 12) diff -= 24;
    if (diff < -12) diff += 24;
    return sum + diff;
  }, 0);
  return base + relativeSum / times.length;
};

type ChartData = {
  date: string;
  bedtime: number;
  waketime: number;
  sleepHours: number;
};

/**
 * APIレスポンスをチャート用データに変換する
 * @param records 睡眠推定レコードの配列
 */
export const toChartData = (records: DailyEstimateSleepRecord[]): ChartData[] =>
  records.map((r) => ({
    date: new Date(r.date).toLocaleDateString("ja-JP", {
      month: "numeric",
      day: "numeric",
    }),
    bedtime: timeToNumber(r.bed_time),
    waketime: timeToNumber(r.wake_time),
    sleepHours: calcSleepHours(r.bed_time, r.wake_time),
  }));
