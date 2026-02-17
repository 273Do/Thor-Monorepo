import useSWRMutation from "swr/mutation";

import { apiEndpoint } from "~/core/constants";

export type StepCountRecord = {
  start_date: string;
  end_date: string;
  value: number;
};

export type SleepAnalysisRecord = {
  start_date: string;
  end_date: string;
  value: string;
};

export type ExtractedSteps = {
  id: string;
  step_data: StepCountRecord[];
  sleep_data: SleepAnalysisRecord[] | null;
};

export type ExtractedStepsResponse = {
  data: ExtractedSteps;
};

/**
 * 歩数抽出のリクエストを送信する
 * @param url url
 * @param { arg } xmlファイル
 */
export const postExtractStepsRequest = async (
  url: string,
  { arg }: { arg: File }
): Promise<ExtractedSteps> => {
  const response = await fetch(`${apiEndpoint}${url}`, {
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
 * 抽出期間か範囲を指定してApple HealthcareのXMLデータから歩数を抽出するフック
 * @param q クエリパラメータ
 */
export const useExtractSteps = (q: string) => {
  // TODO: 各パラメータを引数に取るようにして内部でクエリを組み立てる
  // 抽出処理を手動でトリガーするための設定
  const { trigger, isMutating, data } = useSWRMutation(
    `/extract-steps?${q}`,
    postExtractStepsRequest
  );

  // TODO: id をlocalstorageに保存

  return { trigger, isMutating, data };
};
