import streamlit as st

st.title("Training Evaluation")

responses = {}

# 1. Antal touch
responses["touch"] = st.radio(
    "1. Number of touches",
    ["Too few", "Just right"]
)

# 2. Reason
responses["touch_reason"] = st.radio(
    "Reason for answer",
    ["Exercise design", "Myself"]
)

# 3. Intensity
responses["intensity"] = st.radio(
    "Intensity",
    ["Low", "Just right", "High"]
)

# 4. Reason for intensity
responses["intensity_reason"] = st.radio(
    "Reason for intensity",
    ["Training setup", "Myself"]
)

# 5. Match relevance
responses["match_connection"] = st.radio(
    "Connection to match",
    ["Unclear", "Clear"]
)

# Comment
responses["comment"] = st.text_area("Comment (optional)")

if st.button("Submit"):
    st.write(responses)