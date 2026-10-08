import pandas as pd
import ollama


def calculate_quality_score(df):
    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    missing_penalty = (missing_cells / total_cells) * 100

    duplicate_penalty = (
        (duplicate_rows / len(df)) * 100
        if len(df) > 0 else 0
    )

    score = 100 - missing_penalty - duplicate_penalty

    return round(max(score, 0), 2)


def generate_flags(df):

    flags = []

    # Missing values
    for column in df.columns:

        missing = df[column].isnull().sum()

        if missing > 0:

            percentage = (missing / len(df)) * 100

            if percentage >= 20:
                severity = "HIGH"

            elif percentage >= 5:
                severity = "MEDIUM"

            else:
                severity = "LOW"

            flags.append({
                "issue": "Missing values",
                "column": column,
                "count": int(missing),
                "percentage": round(percentage, 2),
                "severity": severity
            })


    # Outliers
    for column in df.select_dtypes(include="number").columns:

        data = df[column].dropna()

        if len(data) == 0:
            continue

        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((data < lower) | (data > upper)).sum()

        if outliers > 0:

            flags.append({
                "issue": "Outliers",
                "column": column,
                "count": int(outliers),
                "severity": "MEDIUM"
            })

    return flags


def generate_quality_report(df):

    report = {

        "dataset": {
            "rows": len(df),
            "columns": len(df.columns)
        },

        "quality_score": calculate_quality_score(df),

        "missing_values": (
            df.isnull()
            .sum()
            .loc[lambda x: x > 0]
            .to_dict()
        ),

        "duplicates": int(
            df.duplicated().sum()
        ),

        "flags": generate_flags(df)
    }

    return report


def make_decisions(report):

    decisions = []

    for flag in report["flags"]:

        if flag["issue"] == "Missing values":

            if flag["column"] == "Total Spent":

                decision = (
                    "Review - may be calculable "
                    "from Price Per Unit × Quantity"
                )

            elif flag["column"] == "Discount Applied":

                decision = (
                    "Flag for review - too many "
                    "missing values to safely assume"
                )

            else:

                decision = (
                    "Flag for review - do not "
                    "automatically fill"
                )

        elif flag["issue"] == "Outliers":

            decision = (
                "Flag for review - do not "
                "automatically remove"
            )

        else:

            decision = "Flag for review"

        decisions.append({

            "issue": flag["issue"],

            "column": flag["column"],

            "severity": flag["severity"],

            "decision": decision
        })

    return decisions


def clean_data(df):

    cleaned_df = df.copy()

    fixes = []

    # Remove duplicate rows
    duplicates = cleaned_df.duplicated().sum()

    if duplicates > 0:

        cleaned_df = cleaned_df.drop_duplicates()

        fixes.append(
            f"Removed {duplicates} duplicate rows"
        )


    # Calculate missing Total Spent
    mask = (
        cleaned_df["Total Spent"].isna()
        & cleaned_df["Price Per Unit"].notna()
        & cleaned_df["Quantity"].notna()
    )

    count = mask.sum()

    if count > 0:

        cleaned_df.loc[mask, "Total Spent"] = (

            cleaned_df.loc[mask, "Price Per Unit"]

            *

            cleaned_df.loc[mask, "Quantity"]

        )

        fixes.append(
            f"Calculated Total Spent for {count} rows"
        )

    return cleaned_df, fixes


def generate_ai_summary(report, decisions):

    prompt = f"""

You are a Data Quality Analyst.

Analyze the data quality report below.

Quality score:
{report["quality_score"]}

Flags:
{report["flags"]}

Decisions:
{decisions}

IMPORTANT RULES:

1. Do NOT invent problems.

2. Do NOT change the decisions made
   by the Data Quality Engine.

3. If a decision says "Flag for review",
   say it requires human review.

4. Do NOT say an issue is safe to fix
   unless the decision explicitly says
   it is safe to fix.

5. Do NOT recommend filling missing values
   just because their severity is LOW.

6. Clearly distinguish between detected
   problems and recommended actions.

Write a concise professional report with:

1. Overall Data Quality

2. Problems Found

3. Safe Automatic Fixes

4. Issues Requiring Human Review

5. Recommended Next Steps

"""

    response = ollama.chat(

        model="llama3.2:3b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]