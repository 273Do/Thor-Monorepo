import { Loader2 } from "lucide-react";

import { Card, CardContent } from "./ui/card";

type props = {
  /**
   * 処理のステータス状態
   */
  status: "extract" | "estimate" | "feedback";
};

export const Loading = ({ status }: props) => {
  let statusText = "";

  if (status === "extract") statusText = "ヘルスデータを抽出中";
  else if (status === "estimate") statusText = "睡眠状態を推定中";
  else statusText = "フィードバックを生成中";

  return (
    <Card>
      <CardContent className="flex flex-col items-center gap-4 py-16">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <div className="text-center">
          <p className="font-medium text-foreground">{statusText}...</p>

          {status === "feedback" ? (
            <p className="mt-1 text-sm text-muted-foreground">
              睡眠推定結果をもとに
              <br />
              フィードバックを生成しています
              <br />
              (少し時間がかかります)
            </p>
          ) : (
            <p className="mt-1 text-sm text-muted-foreground">
              ヘルスデータとアンケート結果をもとに
              <br />
              睡眠パターンを推定しています
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
