import type {
  EstimateSleepRequest,
  EstimateSleepResponse,
  ExtractedSteps,
  ExtractedStepsResponse,
  LLMFeedbackRequest,
  LLMFeedbackResponse,
  ViaEmailArg,
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

  const { data }: ExtractedStepsResponse = await response.json();

  return data;
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

/**
 * AIからフィードバックを取得する
 * @param path path
 * @param { arg } bodyリクエスト
 */
export const postAIFeedbackRequest = async (
  path: string,
  { arg }: { arg: LLMFeedbackRequest }
) => {
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

  const { data }: LLMFeedbackResponse = await response.json();

  return data;
};

/**
 * email経由で解析〜フィードバックまでを行う
 * @param path path
 * @param { arg } bodyリクエスト
 */
export const postViaEmail = async (
  path: string,
  { arg }: { arg: ViaEmailArg }
): Promise<void> => {
  const formData = new FormData();
  formData.append("xml_file", arg.xmlFile);
  formData.append("req", JSON.stringify(arg.req));

  const response = await fetch(`${API_ENDPOINT}${path}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
};
