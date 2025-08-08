import os, requests, pandas as pd, json, io
import streamlit as st

API_URL = os.getenv("MR_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="MR Auto-Generate (Demo)", layout="centered")

st.title("Materials Request Generator (Demo)")
st.caption("Enter a short project description. The backend will infer details and generate a draft MR.")

with st.form("mr_form"):
    desc = st.text_area(
        "Project Description",
        placeholder="e.g., Greenfield 69 kV substation, ring bus, 1x 25 MVA transformer, 4 feeders, ComEd.",
        height=150
    )
    submitted = st.form_submit_button("Generate MR")

if submitted and desc.strip():
    try:
        resp = requests.post(f"{API_URL}/mr/generate", json={"description": desc, "options": {"return_format": "json"}})
        resp.raise_for_status()
        data = resp.json()

        st.subheader("Project Meta")
        st.json(data["project_meta"])

        st.subheader("Assumptions")
        for a in data["assumptions"]:
            st.write(f"- {a}")

        st.subheader("Line Items")
        df = pd.DataFrame(data["line_items"])
        df_display = df[["item_code","description","category","unit","qty","source_rule","confidence","notes"]]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.subheader("Totals")
        st.json(data["totals"])

        # Downloads
        csv_buf = io.StringIO()
        df_display.to_csv(csv_buf, index=False)
        st.download_button("Download CSV", csv_buf.getvalue(), file_name=f"{data['mr_id'] or 'mr'}.csv", mime="text/csv")

        md_lines = ["| Item Code | Description | Category | Unit | Qty | Notes |",
                    "|---|---|---|---:|---:|---|"]
        for _, r in df_display.iterrows():
            md_lines.append(f"| {r['item_code']} | {r['description']} | {r['category']} | {r['unit']} | {r['qty']} | {r['notes']} |")
        st.download_button("Copy Markdown Table", "\n".join(md_lines), file_name=f"{data['mr_id'] or 'mr'}.md", mime="text/markdown")

        st.caption(f"Generated at: {data['generated_at']}  •  MR ID: {data.get('mr_id','(not stored)')}")

    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
