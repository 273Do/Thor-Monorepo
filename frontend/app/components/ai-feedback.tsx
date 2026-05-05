import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import ReactMarkdown from "react-markdown";

import { ArrowLeft, Bot, RefreshCw } from "lucide-react";
import remarkGfm from "remark-gfm";

import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";

import { Loading } from "./loading";
import { Button } from "./ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Separator } from "./ui/separator";

import type { LanguagesType } from "~/utils/types";
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
  const { t, i18n } = useTranslation();
  const { feedbackTrigger, isFeedbackMutating, feedbackData } = useAIFeedback();

  const initialModel = models[1];
  const selectLLMRef = useRef<string>(initialModel);

  const triggerFeedback = () => {
    feedbackTrigger({
      id,
      llm: selectLLMRef.current,
      lang: i18n.language as LanguagesType,
      is_specialized: false,
    });
  };

  const handleReset = () => {
    window.location.reload();
  };

  useEffect(() => {
    triggerFeedback();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      {feedbackData && !isFeedbackMutating ? (
        <>
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                  <Bot className="h-4 w-4 text-primary" />
                </div>
                <CardTitle className="text-base">
                  {t("aiFeedback.title")}
                </CardTitle>
              </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div id="md">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {feedbackData}
                </ReactMarkdown>
              </div>

              <Separator />

              <div className="flex items-center gap-3">
                <Select
                  defaultValue={initialModel}
                  onValueChange={(v) => {
                    selectLLMRef.current = v;
                  }}
                >
                  <SelectTrigger className="w-full bg-card text-foreground">
                    <SelectValue defaultValue={initialModel} />
                  </SelectTrigger>
                  <SelectContent>
                    {models.map((value, i) => (
                      <SelectItem key={i} value={String(value)}>
                        {value}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button className="shrink-0 gap-2" onClick={triggerFeedback}>
                  <RefreshCw className="size-4" />
                  {t("aiFeedback.regenerate")}
                </Button>
              </div>
            </CardContent>
          </Card>
          {/* Reset */}

          <Button variant="outline" className="w-full" onClick={handleReset}>
            <ArrowLeft className="size-4" />
            {t("aiFeedback.backToForm")}
          </Button>
        </>
      ) : (
        <Loading status="feedback" />
      )}
    </>
  );
};
