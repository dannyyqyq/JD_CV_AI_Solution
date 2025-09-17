from src.document_ingestion.pdf_processor import PDFProcessor
from src.parsers.cv_parsers import CVParser
from src.parsers.jd_parsers import JDParser
from src.parsers.cv_vs_jd_parsers import CVvsJDParser
from src.logger import logging
import streamlit as st
import tempfile


def main():
    st.title("📄 CV vs JD Comparison Agent")
    st.write("Upload your CV (PDF) once, then paste different JDs to compare.")

    if "cv_json" not in st.session_state:
        st.subheader("Step 1: Upload CV (PDF)")
        cv_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])
        if cv_file and st.button("🚀 Process CV"):
            try:
                with st.spinner("📄 Processing CV... This may take a moment"):
                    # Save temporary CV file
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp_cv:
                        tmp_cv.write(cv_file.read())
                        tmp_cv_path = tmp_cv.name

                    pdf_processor = PDFProcessor()
                    cv_docs = pdf_processor.process_pdf(tmp_cv_path)
                    cv_text = " ".join([doc.page_content for doc in cv_docs])

                    cv_parser = CVParser()
                    st.session_state.cv_json = cv_parser.parse(cv_text)

                st.success("✅ CV processed and saved for session!")
            except Exception as e:
                logging.error(f"Error processing CV: {e}")
    else:
        st.success("✅ CV already loaded in session")

    # Step 2: Paste JD (can change every run)
    if "cv_json" in st.session_state:
        st.subheader("Step 2: Paste Job Description")
        jd_text = st.text_area("Paste Job Description (JD)", height=250)

        # Industry selection
        industry = st.selectbox(
            "Select Industry",
            ["Technology", "Finance", "Healthcare", "Education", "Other"],
            index=0,
        )

        if st.button("🔍 Compare CV vs JD"):
            if not jd_text.strip():
                st.error("Please paste a JD before running comparison.")
                st.stop()

            try:
                # JD Parsing
                with st.spinner("📄 Parsing Job Description..."):
                    jd_parser = JDParser()
                    jd_json = jd_parser.parse(jd_text)

                # CV vs JD Comparison
                with st.spinner("⚖️ Comparing CV against JD..."):
                    cv_vs_jd_parser = CVvsJDParser()
                    comparison_json = cv_vs_jd_parser.compare_cv_vs_jd(
                        st.session_state.cv_json, jd_json, industry=industry
                    )

                # Show Results
                st.subheader("Results")

                # JD JSON inside expander
                with st.expander("📄 View Parsed JD JSON"):
                    st.json(jd_json)

                # CV JSON inside expander
                with st.expander("📄 View Parsed CV JSON"):
                    st.json(st.session_state.cv_json)

                # CV vs JD Comparison JSON inside expander
                with st.expander("⚖️ View Raw CV vs JD Comparison JSON"):
                    st.json(comparison_json)

                # Highlight key comparison insights outside expanders
                st.subheader("🔍 Key Insights")

                ats_score = comparison_json.get("ats_score", 0)
                ats_feedback = comparison_json.get("ats_feedback", "")

                st.metric(label="ATS Score", value=f"{ats_score}/10")
                st.write(f"**Feedback:** {ats_feedback}")

                st.write("### ✅ Matched Skills")
                st.write(", ".join(comparison_json.get("matched_skills", [])))

                st.write("### ❌ Missing Skills")
                st.write(", ".join(comparison_json.get("missing_skills", [])))

                st.write("### 📌 Recommendations")
                for rec in comparison_json.get("recommendations", []):
                    st.write(f"- {rec}")

                st.write("### ⚠️ Gap Analysis")
                for gap in comparison_json.get("gap_analysis", []):
                    st.write(f"- {gap}")

            except Exception as e:
                logging.error(f"Error during comparison: {e}")
                st.error(f"Comparison failed: {e}")


if __name__ == "__main__":
    main()
