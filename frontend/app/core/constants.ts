import type { MonthsParams } from "~/utils/use-extract-steps";

export const chargingBeforeBedAnswer = [
  "就寝直前",
  "15分前程度",
  "30分前程度",
  "1時間前程度",
  "充電しない",
] as const;

export const carryingASmartphoneAnswer = [
  "よく持ち歩く",
  "持ち歩く",
  "あまり持ち歩かない",
] as const;

export const apiEndpoint: string = import.meta.env.VITE_BACKEND_ENDPOINT;

export const defaultExtractStepsQuery: MonthsParams = {
  includeRecordedSleep: false,
  monthsOfExtract: 1,
};
