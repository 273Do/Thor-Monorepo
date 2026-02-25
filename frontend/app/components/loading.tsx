import { useTranslation } from "react-i18next";

import { Loader2 } from "lucide-react";

import { Card, CardContent } from "./ui/card";

type props = {
  /**
   * 処理のステータス状態
   */
  status: "extract" | "estimate" | "feedback";
};

export const Loading = ({ status }: props) => {
  const { t } = useTranslation();

  const statusText =
    status === "extract"
      ? t("loading.extractStatus")
      : status === "estimate"
        ? t("loading.estimateStatus")
        : t("loading.feedbackStatus");

  return (
    <Card>
      <CardContent className="flex flex-col items-center gap-4 py-16">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <div className="text-center">
          <p className="font-medium text-foreground">{statusText}...</p>

          <p
            className="mt-1 text-sm text-muted-foreground"
            style={{ whiteSpace: "pre-line" }}
          >
            {status === "feedback"
              ? t("loading.feedbackDesc")
              : t("loading.healthDesc")}
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
