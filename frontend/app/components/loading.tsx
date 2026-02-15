import { Loader2 } from "lucide-react";

import { Card, CardContent } from "./ui/card";

export const Loading = () => {
  return (
    <Card>
      <CardContent className="flex flex-col items-center gap-4 py-16">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <div className="text-center">
          <p className="font-medium text-foreground">データを分析中...</p>
          <p className="mt-1 text-sm text-muted-foreground">
            ヘルスデータとアンケート結果をもとに
            <br />
            睡眠パターンを推定しています
          </p>
        </div>
      </CardContent>
    </Card>
  );
};
