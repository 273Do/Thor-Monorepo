import { useEffect } from "react";

import { Bot } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";

import { Loading } from "./loading";

import { useAIFeedback } from "~/utils/use-ai-feedback";

type props = {
  /**
   * id
   */
  id: string;
  /**
   * models
   */
  models: string[];
};
export const AIFeedback = ({ id, models }: props) => {
  // TODO: マウント時にFBを取得

  const { feedbackTrigger, isFeedbackMutating, feedbackData } = useAIFeedback();

  useEffect(() => {
    feedbackTrigger({
      id,
      llm: models[0],
      lang: "ja",
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      {feedbackData && !isFeedbackMutating ? (
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <Bot className="h-4 w-4 text-primary" />
              </div>
              <CardTitle className="text-base">AI フィードバック</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-sm leading-relaxed whitespace-pre-line text-foreground/80">
              {feedbackData}
            </div>
          </CardContent>
        </Card>
      ) : (
        <Loading status="feedback" />
      )}
    </>
  );
};
