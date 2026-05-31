import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import re

st.title("🌐 Company Enrichment System")

# -------- SCRAPER --------
def scrape(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        return " ".join(text.split())[:4000]
    except:
        return ""

# -------- EXTRACTOR --------
def extract(text, url):

    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"\+?\d[\d\s\-]{8,}\d", text)

    return {
        "website_name": url,
        "company_name": "",
        "address": "",
        "mobile_number": phones[0] if phones else "",
        "mail": emails if emails else [],
        "core_service": "",
        "target_customer": "",
        "probable_pain_point": "",
        "outreach_opener": "Hi team, I noticed your website and would love to connect."
    }

# -------- UI --------
url = st.text_input("Enter Company URL")

if st.button("Enrich"):
    if url:
        text = scrape(url)
        result = extract(text, url)
        st.json(result)

if st.button("Show Sample Test"):
    st.write("Try: https://www.apple.com")