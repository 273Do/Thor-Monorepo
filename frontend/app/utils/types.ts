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
export type Answers = {
  charging_before_bed_answer: number;
  carrying_a_smartphone_answer: number;
  bedtime_answer: number;
};

export type EstimateSleepRequest = {
  id: string;
  answers: Answers;
  step_data: StepCountRecord[];
};

export type DailyEstimateSleepRecord = {
  date: string;
  bed_time: string;
  wake_time: string;
  is_default_time: [boolean, boolean];
};

export type EstimateSleepResponse = {
  data: DailyEstimateSleepRecord[];
  models: string[];
};

export type LanguagesType = "ja" | "en";

// email経由の解析関連のスキーマ
export type ViaEmailRequest =
  | {
      answers: Answers;
      email_to: string;
    }
  | LLMFeedbackBase;

export type ViaEmailArg = {
  xmlFile: File;
  req: ViaEmailRequest;
};

// フィードバック関連のスキーマ
export type LLMFeedbackRequest =
  | {
      id: string;
      llm: string;
    }
  | LLMFeedbackBase;

export type LLMFeedbackBase = {
  lang: LanguagesType;
  is_specialized: boolean;
};

export type LLMFeedbackResponse = {
  data: string;
};
