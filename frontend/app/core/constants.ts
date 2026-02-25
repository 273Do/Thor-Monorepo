import type { MonthsParams } from "~/utils/use-extract-steps";

export const API_ENDPOINT: string = import.meta.env.VITE_BACKEND_ENDPOINT;

export const DEFAULT_EXTRACT_STEP_QUERY: MonthsParams = {
  includeRecordedSleep: false,
  monthsOfExtract: 1,
};

export const NON_IPHONE_USERS_URL: string =
  "https://github.com/273Do/Thor-Monorepo/tree/feature/%2320-frontend-connecting-to-backend?tab=readme-ov-file#iphone-%E7%AB%AF%E6%9C%AB%E4%BB%A5%E5%A4%96%E3%81%AE%E6%96%B9%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6";
