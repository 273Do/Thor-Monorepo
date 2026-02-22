import useSWRMutation from "swr/mutation";

import { postExtractStepsRequest } from "./api";

export type MonthsParams = {
  includeRecordedSleep: boolean;
  monthsOfExtract: number;
};

export type DateRangeParams = {
  includeRecordedSleep: boolean;
  startDateOfExtract: Date;
  endDateOfExtract: Date;
};

type ExtractStepsParams = MonthsParams | DateRangeParams;

/**
 * クエリパラメータの作成
 * @param params クエリパラメータ（月数指定 or 日付範囲指定）
 */
const buildQuery = (params: ExtractStepsParams): string => {
  if ("monthsOfExtract" in params) {
    return `months_of_extract=${params.monthsOfExtract}&include_recorded_sleep=${params.includeRecordedSleep}`;
  }
  return `start_date_of_extract=${params.startDateOfExtract.toISOString()}&end_date_of_extract=${params.endDateOfExtract.toISOString()}&include_recorded_sleep=${params.includeRecordedSleep}`;
};

/**
 * 抽出期間か範囲を指定してApple HealthcareのXMLデータから歩数を抽出するフック
 * @param params クエリパラメータ（月数指定 or 日付範囲指定）
 */
export const useExtractSteps = (params: ExtractStepsParams) => {
  const q = buildQuery(params);

  const { trigger, isMutating, data } = useSWRMutation(
    `/extract-steps?${q}`,
    postExtractStepsRequest
  );

  // TODO: id をlocalstorageに保存

  return {
    extractStepTrigger: trigger,
    isExtractStepMutating: isMutating,
    extractSteData: data,
  };
};
