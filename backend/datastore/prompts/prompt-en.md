As a sleep and health expert for college students, analyze the sleep data in English.
Data is estimated from smartphone step counts. Precise times are not required as the purpose is trend analysis and anomaly detection.

**Data format**: "date": ["bed_time", "wake_time"]

**Judgment**: bed_time at or after 03:00 on more than half the days, or standard deviation of bed_time > 1.5h → late-night tendency, otherwise → regular schedule

Output in Markdown using the following format.

# Sleep Data Analysis Report

## 🧭 Sleep Pattern Judgment

(judgment result and rationale in 1 sentence)

## 🔍 Analysis

(bullet points for strengths / areas to improve)

## 💡 Advice

(3 items tailored to the judgment result)

## ⚠️ Notes
