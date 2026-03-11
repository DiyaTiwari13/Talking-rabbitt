import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Talking Rabbitt AI", layout="wide")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🐰 Talking Rabbitt AI")
st.sidebar.info(
"""
Conversational AI for Business Data
Upload your dataset and ask questions like:

• Which region has highest revenue?
• What is the average revenue?
• Show revenue by region
• Show revenue trend
"""
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🐰 Talking Rabbitt")
st.subheader("Conversational Analytics for Business Data")

st.write("Upload your CSV dataset and ask questions about it.")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.divider()

    # -----------------------------
    # DATA PREVIEW
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # -----------------------------
    # BUSINESS METRICS
    # -----------------------------
    st.subheader("Business Insights")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        col = numeric_cols[0]

        total_value = df[col].sum()
        avg_value = df[col].mean()
        max_value = df[col].max()

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Value", f"{total_value}")
        c2.metric("Average Value", f"{avg_value:.2f}")
        c3.metric("Highest Value", f"{max_value}")

    st.divider()

    # -----------------------------
    # CHAT INPUT
    # -----------------------------
    question = st.chat_input("Ask a question about your data")

    if question:

        st.chat_message("user").write(question)

        q = question.lower()

        response = ""

        if len(numeric_cols) > 0:
            col = numeric_cols[0]

            # -----------------------------
            # HIGHEST VALUE
            # -----------------------------
            if "highest" in q or "max" in q or "best" in q:

                row = df.loc[df[col].idxmax()]
                response = f"The highest {col} is **{row[col]}**."

                st.chat_message("assistant").write(response)

                fig = px.bar(df, x=df.columns[0], y=col, title="Highest Value Comparison")
                st.plotly_chart(fig)

            # -----------------------------
            # LOWEST VALUE
            # -----------------------------
            elif "lowest" in q or "min" in q or "worst" in q:

                row = df.loc[df[col].idxmin()]
                response = f"The lowest {col} is **{row[col]}**."

                st.chat_message("assistant").write(response)

            # -----------------------------
            # AVERAGE
            # -----------------------------
            elif "average" in q or "mean" in q:

                avg = df[col].mean()
                response = f"The average {col} is **{avg:.2f}**."

                st.chat_message("assistant").write(response)

            # -----------------------------
            # TOTAL
            # -----------------------------
            elif "total" in q or "sum" in q:

                total = df[col].sum()
                response = f"The total {col} is **{total}**."

                st.chat_message("assistant").write(response)

            # -----------------------------
            # SHOW BAR CHART
            # -----------------------------
            elif "chart" in q or "plot" in q or "visualize" in q:

                response = "Here is the chart for your dataset."

                st.chat_message("assistant").write(response)

                fig = px.bar(df, x=df.columns[0], y=col, title="Data Visualization")
                st.plotly_chart(fig)

            # -----------------------------
            # TREND CHART
            # -----------------------------
            elif "trend" in q or "growth" in q:

                response = "Here is the trend of your data."

                st.chat_message("assistant").write(response)

                fig = px.line(df, x=df.columns[0], y=col, title="Trend Analysis")
                st.plotly_chart(fig)

            # -----------------------------
            # DEFAULT RESPONSE
            # -----------------------------
            else:

                response = """
I can answer questions like:

• Which has the highest value?
• What is the average value?
• Show the chart
• Show the trend
• What is the total?
"""

                st.chat_message("assistant").write(response)

    st.divider()

    # -----------------------------
    # AUTO INSIGHTS BUTTON
    # -----------------------------
    if st.button("Generate Automatic Insights"):

        st.subheader("Automatic Insights")

        if len(numeric_cols) > 0:

            col = numeric_cols[0]

            best_row = df.loc[df[col].idxmax()]
            worst_row = df.loc[df[col].idxmin()]

            st.write(f"Top performer: **{best_row[df.columns[0]]}**")
            st.write(f"Lowest performer: **{worst_row[df.columns[0]]}")

            fig = px.bar(df, x=df.columns[0], y=col, title="Performance Comparison")
            st.plotly_chart(fig)

else:

    st.info("Please upload a CSV file to begin analysis.")