import type {
  EstimateSleepRequest,
  EstimateSleepResponse,
  ExtractedSteps,
  ExtractedStepsResponse,
} from "./types";

import { API_ENDPOINT } from "~/core/constants";

/**
 * 歩数抽出のリクエストを送信する
 * @param path path
 * @param { arg } xmlファイル
 */
export const postExtractStepsRequest = async (
  path: string,
  { arg }: { arg: File }
): Promise<ExtractedSteps> => {
  const response = await fetch(`${API_ENDPOINT}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "text/xml",
    },
    body: arg,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const steps: ExtractedStepsResponse = await response.json();

  return steps.data;
};

/**
 * 睡眠推定のリクエストを送信する
 * @param path path
 * @param { arg } bodyリクエスト
 */
export const postEstimateSleepRequest = async (
  path: string,
  { arg }: { arg: EstimateSleepRequest }
): Promise<EstimateSleepResponse> => {
  const response = await fetch(`${API_ENDPOINT}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(arg),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const { data, models }: EstimateSleepResponse = await response.json();

  return { data, models };
};
