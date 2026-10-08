import sys
from pathlib import Path

import streamlit as st
import pandas as pd


# Find src folder
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))


# Import data quality functions
from quality_checker import (
    generate_quality_report,
    generate_flags,
    calculate_quality_score,
    make_decisions,
    clean_data,
    generate_ai_summary
)


# Page settings
st.set_page_config(
    page_title="AI Data Quality Agent",
    page_icon="🤖",
    layout="wide"
)


# Title
st.title("🤖 AI Data Quality Agent")

st.write(
    "Upload a CSV dataset and let the AI agent "
    "automatically detect data-quality problems, "
    "make decisions, and generate a quality report."
)


# Upload dataset
uploaded_file = st.file_uploader(
    "📂 Upload CSV Dataset",
    type=["csv"]
)


if uploaded_file:

    # Load dataset
    df = pd.read_csv(uploaded_file)

    st.success(
        f"Dataset loaded successfully: "
        f"{len(df):,} rows × {len(df.columns)} columns"
    )


    # Preview
    with st.expander("👀 Preview Dataset"):

        st.dataframe(
            df.head(10),
            use_container_width=True
        )


    # Analyze button
    if st.button(
        "🔍 Analyze Dataset",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "AI Data Quality Agent is analyzing the dataset..."
        ):

            # Generate report
            final_report = generate_quality_report(df)

            # Detect issues
            flags = generate_flags(df)

            # Calculate score
            score = calculate_quality_score(df)


            # Agent decisions
            decisions = make_decisions(
                final_report
            )


            # Automatic cleaning
            cleaned_df, fixes = clean_data(df)


            # AI explanation
            ai_summary = generate_ai_summary(
                final_report,
                decisions
            )


        st.success("Analysis completed successfully! 🎉")


        # --------------------------------
        # QUALITY SCORE
        # --------------------------------

        st.subheader("📊 Data Quality Score")

        st.metric(
            "Overall Quality Score",
            f"{score}/100"
        )


        # --------------------------------
        # DATASET INFORMATION
        # --------------------------------

        st.subheader("📁 Dataset Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rows",
                f"{len(df):,}"
            )

        with col2:

            st.metric(
                "Columns",
                len(df.columns)
            )

        with col3:

            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )


        # --------------------------------
        # ISSUES DETECTED
        # --------------------------------

        st.subheader("⚠️ Issues Detected")

        if flags:

            for flag in flags:

                st.write(
                    f"**{flag['issue']}** | "
                    f"Column: **{flag['column']}** | "
                    f"Severity: **{flag['severity']}** | "
                    f"Count: **{flag['count']:,}**"
                )

        else:

            st.success(
                "No major data-quality issues detected."
            )


        # --------------------------------
        # AGENT DECISIONS
        # --------------------------------

        st.subheader("🤖 Agent Decisions")

        for decision in decisions:

            st.write(
                f"**{decision['column']}** → "
                f"{decision['decision']}"
            )


        # --------------------------------
        # AUTOMATIC FIXES
        # --------------------------------

        st.subheader("🛠️ Automatic Fixes")

        if fixes:

            for fix in fixes:

                st.success(
                    f"✅ {fix}"
                )

        else:

            st.info(
                "No automatic fixes were applied."
            )


        # --------------------------------
        # AI REPORT
        # --------------------------------

        st.subheader("🧠 AI Data Quality Report")

        st.markdown(ai_summary)


        # --------------------------------
        # CLEANED DATA
        # --------------------------------

        st.subheader("👀 Cleaned Dataset Preview")

        st.dataframe(
            cleaned_df.head(20),
            use_container_width=True
        )


        # --------------------------------
        # DOWNLOAD
        # --------------------------------

        st.subheader("📥 Download Cleaned Dataset")

        csv = cleaned_df.to_csv(
            index=False
        )

        st.download_button(
            label="⬇️ Download Cleaned CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )


# Footer
st.divider()

st.caption(
    "Built with Python • Pandas • Streamlit • "
    "Ollama • Llama 3.2"
)