import json
import re

# Load raw scraped data
with open("cirrusgo_content.json", "r") as f:
    raw = json.load(f)

cleaned = {
    "about": "",
    "mission": "",
    "services": [],
    "aws_competencies": [],
    "solutions": [],
    "why_cirrusgo": "",
    "blog_highlights": []
}

# Helper function to clean garbage text
def clean_text(text):
    # Remove form fields, cookie banners, submit buttons, etc.
    text = re.sub(r"Get Your Free Consultation.*", "", text, flags=re.DOTALL)
    text = re.sub(r"We use cookies.*", "", text)
    text = re.sub(r"Your Name.*", "", text)
    text = re.sub(r"Submit", "", text)
    text = text.replace("\u200b", " ")
    text = text.replace("\ufeff", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ------------------------------
# Extract ABOUT & MISSION
# ------------------------------
if " https://www.cirrusgo.com/about-us" in raw:
    about_page = clean_text(raw[" https://www.cirrusgo.com/about-us"])

    # Extract ABOUT (before "Our Mission")
    about_match = re.search(
        r"(Cirrusgo is.*?)(Our Mission|Mission)",
        about_page,
        re.DOTALL | re.IGNORECASE
    )
    if about_match:
        cleaned["about"] = about_match.group(1).strip()

    # Extract MISSION (after "Our Mission")
    mission_match = re.search(
        r"(Our Mission.*)",
        about_page,
        re.DOTALL | re.IGNORECASE
    )
    if mission_match:
        cleaned["mission"] = mission_match.group(1).strip()


# ------------------------------
# Extract WHY CIRRUSGO (from homepage)
# ------------------------------
home_text = clean_text(raw.get("https://cirrusgo.com", ""))

why_match = re.search(
    r"Why Cirrusgo(.*?)(Discover|Jump Into Generative AI)",
    home_text,
    re.DOTALL
)
if why_match:
    cleaned["why_cirrusgo"] = clean_text(why_match.group(1)).strip()


# ------------------------------
# Extract SERVICES
# ------------------------------
services_page = clean_text(raw.get("https://www.cirrusgo.com/our-services", ""))

# Split based on capitalized service headings
service_blocks = re.split(
    r"(?=[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)",
    services_page
)

for block in service_blocks:
    block = block.strip()
    if len(block) < 50:
        continue
    
    # Extract title (first 2–3 words)
    title = " ".join(block.split()[:3])
    
    cleaned["services"].append({
        "title": title,
        "description": block
    })


# ------------------------------
# Extract AWS Competencies Page
# ------------------------------
aws_page = clean_text(raw.get("https://www.cirrusgo.com/aws", ""))
if aws_page:
    cleaned["aws_competencies"].append(aws_page)


# ------------------------------
# Extract BLOG TITLES
# ------------------------------
blog_page = clean_text(raw.get("https://www.cirrusgo.com/blog", ""))

blog_titles = re.findall(
    r"[A-Z][a-zA-Z0-9\s\-&,]+(?=\s\d{1,2},\s\d{4})",
    blog_page
)

cleaned["blog_highlights"] = blog_titles[:10]  # top 10 titles only


# ------------------------------
# Save final cleaned structured file
# ------------------------------
with open("cirrusgo_cleaned.json", "w") as f:
    json.dump(cleaned, f, indent=2)

print("cirrusgo_cleaned.json created successfully!")
