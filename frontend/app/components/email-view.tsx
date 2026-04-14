import { useTranslation } from "react-i18next";

import { ArrowLeft } from "lucide-react";

import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";

type Props = {
  /**
   * メールアドレス
   */
  email: string;
};

export const EmailView = ({ email }: Props) => {
  const { t } = useTranslation();

  const handleReset = () => {
    window.location.reload();
  };

  return (
    <div className="flex flex-col items-center gap-6">
      <Card>
        <CardContent className="flex flex-col items-center gap-4 py-16">
          <div className="text-center">
            <p className="font-medium text-foreground">
              {t("email.sentTitle")}
            </p>
            <p
              className="mt-1 text-sm text-muted-foreground"
              style={{ whiteSpace: "pre-line" }}
            >
              {t("email.sentDescription", { email })}
            </p>
          </div>
        </CardContent>
      </Card>
      <Button variant="outline" className="w-full" onClick={handleReset}>
        <ArrowLeft className="size-4" />
        {t("aiFeedback.backToForm")}
      </Button>
    </div>
  );
};
