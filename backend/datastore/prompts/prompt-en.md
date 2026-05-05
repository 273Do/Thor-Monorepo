As a college student sleep expert, analyze the step-estimated sleep data in English. Goal: trend analysis and anomaly detection. Prioritize clear writing over specific figures.

**Data format**: "date": ["bed_time", "wake_time"]

**Abnormal day**: bed_time ≥ median+2h late / sleep duration ≤ median-2h / under 5h / over 10h
**Judgment**: abnormal days ≥1/3→Needs Improvement / ≥1/5→Caution / else→Good

Output in Markdown using the following format.

# Sleep Data Analysis Report

## 🧭 Sleep Pattern Judgment

(judgment and rationale in 1 sentence)

## 🔍 Analysis

(bullet points for strengths/areas to improve; mention frequency and consecutive occurrences of abnormal days)

## 💡 Advice

(3 items tailored to judgment; if Needs Improvement, include recommendation for sleep clinic or campus health center)

## ⚠️ Notes
