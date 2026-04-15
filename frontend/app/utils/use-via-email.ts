import useSWRMutation from "swr/mutation";

import { postViaEmail } from "./api";
import { buildQuery, type ExtractStepsParams } from "./use-extract-steps";

/**
 * email経由で解析〜フィードバック送信を行うフック
 * @param params クエリパラメータ（月数指定 or 日付範囲指定）
 */
export const useViaEmail = (params: ExtractStepsParams) => {
  const q = buildQuery(params);

  const { trigger } = useSWRMutation(`/via-email?${q}`, postViaEmail);

  return {
    viaEmailTrigger: trigger,
  };
};
