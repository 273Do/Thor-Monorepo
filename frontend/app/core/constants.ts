import type { MonthsParams } from "~/utils/use-extract-steps";

export const CHARGING_BEFORE_BED_ANSWER = [
  "就寝直前",
  "15分前程度",
  "30分前程度",
  "1時間前程度",
  "充電しない",
] as const;

export const CARRYING_A_SMARTPHONE_ANSWER = [
  "よく持ち歩く",
  "持ち歩く",
  "あまり持ち歩かない",
] as const;

export const API_ENDPOINT: string = import.meta.env.VITE_BACKEND_ENDPOINT;

export const DEFAULT_EXTRACT_STEP_QUERY: MonthsParams = {
  includeRecordedSleep: false,
  monthsOfExtract: 1,
};
