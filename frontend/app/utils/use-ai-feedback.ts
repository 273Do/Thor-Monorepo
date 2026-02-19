import useSWRMutation from "swr/mutation";

import { postAIFeedbackRequest } from "./api";

/**
 * AIからフィードバックを取得するフック
 */
export const useAIFeedback = () => {
  const { trigger, isMutating, data } = useSWRMutation(
    "/feedback",
    postAIFeedbackRequest
  );

  return {
    feedbackTrigger: trigger,
    isFeedbackMutating: isMutating,
    feedbackData: data,
  };
};
