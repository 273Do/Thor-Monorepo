import { z } from "zod";

export const surveySchema = z.object({
  chargingBeforeBedAnswer: z.string().min(1),
  carryingASmartphoneAnswer: z.string().min(1),
  bedtime: z.string().min(1),
  email: z.union([z.literal(""), z.string().email()]).optional(),
});

export type SurveyAnswers = z.infer<typeof surveySchema>;

export const defaultSurveyValues: SurveyAnswers = {
  chargingBeforeBedAnswer: "",
  carryingASmartphoneAnswer: "",
  bedtime: "",
  email: "",
};
