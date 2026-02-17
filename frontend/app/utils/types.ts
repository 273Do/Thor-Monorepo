// 歩数抽出関連のスキーマ
export type StepCountRecord = {
  start_date: string;
  end_date: string;
  value: number;
};

export type SleepAnalysisRecord = {
  start_date: string;
  end_date: string;
  value: string;
};

export type ExtractedSteps = {
  id: string;
  step_data: StepCountRecord[];
  sleep_data: SleepAnalysisRecord[] | null;
};

export type ExtractedStepsResponse = {
  data: ExtractedSteps;
};

// 睡眠推定関連のスキーマ
// フィードバック関連のスキーマ
