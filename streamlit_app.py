import streamlit as st
import openai
import pandas as pd
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


# List of criteria and providers (fixed)
CRITERIA = [
    "Core Infrastructure Offerings", "Security Parameters", "Performance (Latency/Throughput)",
    "Service Category Coverage", "Suitability for Organization", "Reliability / Uptime",
    "Enterprise Integration", "AI / ML / Data Capabilities", "Pricing & Flexibility",
    "Range of Services", "Quality of Services", "Compliance Certifications",
    "Developer Experience", "Modern Architecture Support", "Regional Strength",
    "Hybrid/Multicloud Support", "Brand Trust / Familiarity", "Vendor Lock-in Risk",
    "Ecosystem / Marketplace", "Innovation Velocity", "Marketing/Perception",
    "Free Tier / Trial", "Niche Services"
]

PROVIDERS = [
    "AWS", "Azure", "GCP", "Oracle", "IBM", "Alibaba",
    "DigitalOcean", "Linode", "Vultr", "Hetzner", "T-Systems"
]

def generate_prompt(use_case_text):
    return f"""
You are a cloud expert. Given the following use case text:

\"\"\"{use_case_text}\"\"\"

Score the following cloud providers (AWS, Azure, GCP, Oracle, IBM, Alibaba, DigitalOcean, Linode, Vultr, Hetzner, T-Systems) on each of these criteria on a scale from 1 to 5:

- Core Infrastructure Offerings
- Security Parameters
- Performance (Latency/Throughput)
- Service Category Coverage
- Suitability for Organization
- Reliability / Uptime
- Enterprise Integration
- AI / ML / Data Capabilities
- Pricing & Flexibility
- Range of Services
- Quality of Services
- Compliance Certifications
- Developer Experience
- Modern Architecture Support
- Regional Strength
- Hybrid/Multicloud Support
- Brand Trust / Familiarity
- Vendor Lock-in Risk
- Ecosystem / Marketplace
- Innovation Velocity
- Marketing/Perception
- Free Tier / Trial
- Niche Services

Return ONLY a JSON object with the criteria as keys and for each criteria an object mapping providers to integer scores 1-5.

Example:

{{
  "Core Infrastructure Offerings": {{"AWS":5, "Azure":4, ...}},
  ...
}}
"""

def call_openai_api(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response['choices'][0]['message']['content']

def parse_scores(json_str):
    try:
        scores = json.loads(json_str)
        # Validate and fill missing criteria/providers if needed
        for c in CRITERIA:
            if c not in scores:
                scores[c] = {p: 1 for p in PROVIDERS}  # fallback default
            else:
                for p in PROVIDERS:
                    if p not in scores[c]:
                        scores[c][p] = 1
                    else:
                        # Ensure integer and 1-5 range
                        val = scores[c][p]
                        if not isinstance(val, int):
                            try:
                                val = int(val)
                            except:
                                val = 1
                        scores[c][p] = max(1, min(5, val))
        return scores
    except Exception as e:
        st.error(f"Failed to parse GPT output: {e}")
        return None

def scores_to_df(scores):
    df = pd.DataFrame(scores).T  # criteria as rows, providers as columns
    df = df[PROVIDERS]  # ensure order
    return df

def weighted_scores(df, weights):
    weighted = df.mul(weights, axis=0)
    provider_scores = weighted.sum(axis=0) / weights.sum()
    return provider_scores.sort_values(ascending=False)

# Streamlit app
st.title("Cloud Provider Decision Assistant")

st.markdown("""
Paste your **use case description** below, describing the context and key priorities.
The app will generate cloud provider scores per criteria using GPT, then you can adjust criteria weights to get a recommendation.
""")

use_case_input = st.text_area("Use Case Description", height=250)

if st.button("Generate Scores"):
    if not use_case_input.strip():
        st.warning("Please enter a use case description.")
    else:
        with st.spinner("Calling OpenAI to generate scores..."):
            prompt = generate_prompt(use_case_input)
            gpt_output = call_openai_api(prompt)
            st.subheader("Raw GPT JSON Output")
            st.code(gpt_output, language="json")
            scores = parse_scores(gpt_output)
            if scores:
                df_scores = scores_to_df(scores)
                st.session_state['scores_df'] = df_scores
                st.success("Scores generated and loaded.")

if 'scores_df' in st.session_state:
    df = st.session_state['scores_df']
    st.subheader("Generated Scores Matrix")
    st.dataframe(df)

    st.markdown("### Adjust Criteria Importance Weights")
    weights = {}
    for crit in CRITERIA:
        weights[crit] = st.slider(
            label=f"Importance of '{crit}'",
            min_value=1,
            max_value=5,
            value=3,
            key=f"weight_{crit}"
        )
    weights_series = pd.Series(weights)

    st.markdown("### Final Weighted Scores")
    final_scores = weighted_scores(df, weights_series)
    st.dataframe(final_scores.to_frame("Score"))

    st.markdown("### Recommended Cloud Provider")
    st.write(f"**{final_scores.idxmax()}** with score {final_scores.max():.2f}")

