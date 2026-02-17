import type { ExtractedSteps, ExtractedStepsResponse } from "./types";

import { API_ENDPOINT } from "~/core/constants";

/**
 * 歩数抽出のリクエストを送信する
 * @param url url
 * @param { arg } xmlファイル
 */
export const postExtractStepsRequest = async (
  url: string,
  { arg }: { arg: File }
): Promise<ExtractedSteps> => {
  const response = await fetch(`${API_ENDPOINT}${url}`, {
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
