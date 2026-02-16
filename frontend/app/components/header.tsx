import { Moon } from "lucide-react";

export const Header = () => {
  return (
    <header className="mb-8 flex flex-col items-center gap-3 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary text-primary-foreground">
        <Moon className="h-6 w-6" />
      </div>
      <div>
        <h1 className="text-xl font-bold tracking-tight text-foreground">
          Sleep Insight
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          ヘルスデータから睡眠を分析
        </p>
      </div>
    </header>
  );
};
