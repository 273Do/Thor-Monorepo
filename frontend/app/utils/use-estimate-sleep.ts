import useSWRMutation from "swr/mutation";

import { postEstimateSleepRequest } from "./api";

/**
 * 歩数データから睡眠状態を推定するフック
 */
export const useEstimateSleep = () => {
  const { trigger, isMutating, data } = useSWRMutation(
    "/estimate-sleep",
    postEstimateSleepRequest
  );

  return {
    estimateSleepTrigger: trigger,
    isEstimateSleepMutating: isMutating,
    estimateSleepData: data,
  };
};
