AI Data Quality Agent

An AI-powered data quality application that automatically analyzes datasets, detects data-quality issues, makes cleaning decisions, and generates an AI-powered quality report.

FEATURES

• Upload CSV datasets
• Automatically analyze dataset structure
• Detect missing values
• Detect duplicate rows
• Detect statistical outliers using IQR
• Calculate a data quality score
• Make automated data-quality decisions
• Safely calculate missing Total Spent values when possible
• Flag risky issues for human review
• Generate AI-powered data quality reports
• Preview cleaned datasets
• Download cleaned datasets
• Interactive Streamlit web interface
• Uses a local LLM through Ollama, so no paid API is required

PROJECT ARCHITECTURE

CSV Dataset
↓
Pandas
↓
Data Quality Engine
↓
Missing Values / Duplicates / Outliers
↓
Decision Engine
↓
Safe Fixes / Human Review
↓
Ollama + Llama 3.2
↓
AI Quality Report
↓
Streamlit Dashboard

TECHNOLOGIES USED

• Python
• Pandas
• Streamlit
• Ollama
• Llama 3.2
• Git
• GitHub

PROJECT STRUCTURE

AI-Data-Quality-Agent/

├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    └── quality_checker.py

DATASET

The application was tested using a retail transaction dataset containing:

• 12,575 rows
• 11 columns
• Missing values
• Statistical outliers
• Transaction information
• Product information
• Payment information

The raw dataset is intentionally excluded from the GitHub repository.

EXAMPLE ANALYSIS

The tested dataset produced:

• Data Quality Score: 94.77/100
• Duplicate Rows: 0
• Missing Item: 1,213
• Missing Price Per Unit: 609
• Missing Quantity: 604
• Missing Total Spent: 604
• Missing Discount Applied: 4,199
• Total Spent outliers: 60

AI COMPONENT

The application uses Ollama with Llama 3.2 to generate a professional explanation of detected data-quality issues.

The Python data-quality engine performs the actual checks and decisions, while the local LLM is used for interpretation and report generation.

This approach keeps factual data-quality checks deterministic while using AI for natural-language analysis and reporting.

DATA CLEANING

The agent follows a safe-cleaning approach.

It can automatically perform fixes when the conditions are reliable, such as calculating missing Total Spent values when both Price Per Unit and Quantity are available.

Risky issues such as missing product information, missing payment-related information, or statistical outliers are flagged for human review instead of being automatically changed.

HOW TO RUN

1. Install dependencies

pip install -r requirements.txt

2. Start Ollama

Make sure Ollama is installed and run the local Llama 3.2 model:

ollama run llama3.2:3b

Keep Ollama running while using the application.

3. Start the Streamlit application

From the project directory:

streamlit run app.py

The application will open in your browser.

APPLICATION WORKFLOW

1. Upload a CSV dataset.
2. The application loads the dataset using Pandas.
3. The data-quality engine automatically checks the dataset.
4. Missing values and duplicates are detected.
5. Statistical outliers are identified using the IQR method.
6. A data-quality score is calculated.
7. The decision engine determines which issues can be safely handled and which require human review.
8. Safe cleaning operations are applied when appropriate.
9. Ollama generates an AI-powered quality report.
10. The cleaned dataset can be previewed and downloaded.

DATA & SECURITY

Raw datasets and local database files are excluded from the GitHub repository using .gitignore.

The application does not require a paid OpenAI API key because it uses a local Ollama model.

FUTURE IMPROVEMENTS

• Excel file support
• Advanced anomaly detection
• Automatic data-type validation
• Format consistency checks
• Interactive data-quality charts
• More automated cleaning rules
• Agent-based planning
• Tool calling
• LangGraph integration
• Automated data profiling
• Database support

AUTHOR

Yash Gulati

Data Analytics | Business Analytics | AI/LLM | Python | SQL | Power BI