import streamlit as st
import pandas as pd
import emoji
from collections import Counter
import plotly.express as px
from textblob import TextBlob
from langdetect import detect

# ----------------------------------------
# CATEGORY MAP
# ----------------------------------------

CATEGORY_MAP = {
    "face": "Smileys & Emotion", "grin": "Smileys & Emotion", "smile": "Smileys & Emotion",
    "laugh": "Smileys & Emotion", "cry": "Smileys & Emotion", "kiss": "Smileys & Emotion",
    "angry": "Smileys & Emotion", "heart": "Smileys & Emotion", "emotion": "Smileys & Emotion",
    "sweat": "Smileys & Emotion", "wink": "Smileys & Emotion", "blush": "Smileys & Emotion",
    "cat": "Animals & Nature", "dog": "Animals & Nature", "monkey": "Animals & Nature",
    "lion": "Animals & Nature", "tiger": "Animals & Nature", "bear": "Animals & Nature",
    "frog": "Animals & Nature", "flower": "Animals & Nature", "tree": "Animals & Nature",
    "leaf": "Animals & Nature", "fish": "Animals & Nature", "elephant": "Animals & Nature",
    "pizza": "Food & Drink", "burger": "Food & Drink", "cake": "Food & Drink",
    "chocolate": "Food & Drink", "coffee": "Food & Drink", "tea": "Food & Drink",
    "ice": "Food & Drink", "apple": "Food & Drink", "banana": "Food & Drink",
    "cookie": "Food & Drink", "popcorn": "Food & Drink", "sushi": "Food & Drink",
    "ball": "Activities", "game": "Activities", "guitar": "Activities",
    "microphone": "Activities", "trophy": "Activities", "medal": "Activities",
    "sport": "Activities", "dance": "Activities", "bowling": "Activities",
    "car": "Travel & Places", "bus": "Travel & Places", "bike": "Travel & Places",
    "plane": "Travel & Places", "ship": "Travel & Places", "train": "Travel & Places",
    "house": "Travel & Places", "mountain": "Travel & Places", "hotel": "Travel & Places",
    "beach": "Travel & Places", "tent": "Travel & Places", "park": "Travel & Places",
    "phone": "Objects", "computer": "Objects", "tv": "Objects",
    "camera": "Objects", "book": "Objects", "clock": "Objects",
    "money": "Objects", "key": "Objects", "light": "Objects", "tool": "Objects",
    "email": "Objects", "envelope": "Objects", "battery": "Objects",
    "arrow": "Symbols", "check": "Symbols", "cross": "Symbols",
    "question": "Symbols", "exclamation": "Symbols", "star": "Symbols",
    "rainbow": "Symbols", "fire": "Symbols",
    "flag": "Flags",
}

# ----------------------------------------
# Helper Functions
# ----------------------------------------

def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]

def get_emoji_description(e):
    return emoji.EMOJI_DATA.get(e, {}).get("en", "Unknown")

def get_emoji_category(e):
    name = emoji.demojize(e).strip(":").replace("_", " ")
    for keyword, category in CATEGORY_MAP.items():
        if keyword in name:
            return category
    return "Miscellaneous"

def analyze_emojis(text):
    emojis = extract_emojis(text)
    counter = Counter(emojis)
    data = [{
        "Emoji": e,
        "Count": count,
        "Description": get_emoji_description(e),
        "Category": get_emoji_category(e)
    } for e, count in counter.items()]
    return pd.DataFrame(data)

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def localize_emojis(language):
    if language == "it":
        return ["🇮🇹", "🍝", "🍷"]
    elif language == "fr":
        return ["🇫🇷", "🥖", "🧀"]
    elif language == "es":
        return ["🇪🇸", "🌶️", "💃"]
    else:
        return []

def correlate_emojis_with_keywords(text):
    KEYWORD_TO_EMOJIS = {
        "celebration": ["🎉", "🎈", "🥳"],
        "love": ["❤️", "💘", "💌"],
        "party": ["🎉", "🍾", "🥂"],
        "sad": ["😢", "😭", "😞"],
        "happy": ["😊", "😁", "😄"]
    }
    matched = []
    for keyword, related in KEYWORD_TO_EMOJIS.items():
        if keyword in text.lower():
            matched.append((keyword, related))
    return matched

def download_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ----------------------------------------
# Streamlit App UI
# ----------------------------------------

st.set_page_config(page_title="EmojiSense: A Smart Emoji Analyzer", layout="centered")
st.title("🧠 EmojiSense: A Smart Emoji Analyzer")

# ----------------------------------------
# Input Areas
# ----------------------------------------

st.header("1️⃣ Emoji Analysis")
emoji_input = st.text_area("Paste text or emojis here for analysis:", height=150, key="input_analysis")

if st.button("🔍 Analyze Emojis"):
    if emoji_input.strip():
        df = analyze_emojis(emoji_input)
        if not df.empty:
            st.subheader("📋 Emoji Summary")
            st.dataframe(df)

            st.subheader("📊 Emoji Frequency")
            fig_bar = px.bar(df, x='Emoji', y='Count', color='Category', title="Emoji Frequency", text='Count')
            st.plotly_chart(fig_bar)

            st.subheader("📈 Emoji Category Distribution")
            cat_df = df.groupby("Category")["Count"].sum().reset_index()
            fig_pie = px.pie(cat_df, names="Category", values="Count", title="Emoji Categories")
            st.plotly_chart(fig_pie)

            st.subheader("📁 Export CSV")
            st.download_button("Download CSV", data=download_csv(df), file_name="emoji_report.csv", mime="text/csv")
        else:
            st.info("No emojis found in the input.")
    else:
        st.warning("Please enter some text to analyze.")

# ----------------------------------------
# Suggestion Area
# ----------------------------------------

st.markdown("---")
st.header("2️⃣ Emoji Suggestion")
suggestion_input = st.text_area("Type your message here for emoji suggestions:", height=150, key="input_suggestion")

if st.button("💡 Suggest Emojis"):
    if suggestion_input.strip():
        sentiment = analyze_sentiment(suggestion_input)
        language = detect_language(suggestion_input)
        local_emojis = localize_emojis(language)
        keyword_emojis = correlate_emojis_with_keywords(suggestion_input)

        st.markdown(f"**🧠 Sentiment Detected**: `{sentiment}`")
        st.markdown(f"**🌍 Language Detected**: `{language.upper()}`" if language != "unknown" else "**🌍 Language Detection Failed**")

        if local_emojis:
            st.markdown(f"**🇺🇳 Localized Emojis**: {' '.join(local_emojis)}")

        if keyword_emojis:
            for keyword, ems in keyword_emojis:
                st.markdown(f"🔑 **Related to '{keyword}'**: {' '.join(ems)}")

        sentiment_emojis = {
            "Positive": ["😊", "😁", "🥳"],
            "Negative": ["😢", "😞", "😭"],
            "Neutral": ["😐", "🤔", "😶"]
        }

        st.markdown(f"🎭 **Emotion-Based Suggestions**: {' '.join(sentiment_emojis.get(sentiment, []))}")
    else:
        st.warning("Please enter text to get emoji suggestions.")
