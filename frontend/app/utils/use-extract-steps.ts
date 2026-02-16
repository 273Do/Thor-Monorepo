import useSWRMutation from "swr/mutation";

import { apiEndpoint } from "~/core/constants";

/**
 * 歩数抽出のリクエストを送信する
 * @param url url
 * @param { arg } xmlファイル
 */
export const postExtractStepsRequest = async (
  url: string,
  { arg }: { arg: File }
): Promise<Response> => {
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

  return response;
};

/**
 * 抽出期間か範囲を指定してApple HealthcareのXMLデータから歩数を抽出するフック
 * @param q クエリパラメータ
 */
export const useExtractSteps = (q: string) => {
  // TODO: 各パラメータを引数に取るようにして内部でクエリを組み立てる
  const { trigger, isMutating, data } = useSWRMutation(
    `/extract-steps?${q}`,
    postExtractStepsRequest
  );

  return { trigger, isMutating, data };
};
