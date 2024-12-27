import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from datetime import datetime

# Function to fetch RBI news from Google Custom Search
def fetch_rbi_news():
    search_engine_id = "759053462c1944ac0"  # Your Search Engine ID
    query = "Reserve Bank of India"
    google_cse_url = f"https://cse.google.com/cse?cx={search_engine_id}&q={query}"
    
    response = requests.get(google_cse_url)
    if response.status_code != 200:
        return "Failed to fetch news. Please check the Custom Search URL."

    # Parse HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='gs-title')  # Adjust selector as needed
    
    news_content = ""
    for idx, result in enumerate(results[:5], 1):  # Limit to top 5 results
        title = result.text.strip() if result else "No Title"
        url = result.get('href', 'No URL') if result else "No URL"
        news_content += f"{idx}. {title}\n"
        news_content += f"   URL: {url}\n\n"
    
    return news_content or "No news found for today."

# Function to send an email
def send_email(news_content):
    sender_email = os.getenv("SENDER_EMAIL")  # Fetch email from environment variables
    sender_password = os.getenv("SENDER_PASSWORD")  # Fetch password from environment variables
    recipient_email = os.getenv("RECIPIENT_EMAIL")  # Fetch recipient email from environment variables
    
    if not sender_email or not sender_password or not recipient_email:
        raise ValueError("Email credentials or recipient email are not set in environment variables.")
    
    subject = f"Daily RBI News Digest - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Construct the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(news_content, "plain"))
    
    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == "__main__":
    news = fetch_rbi_news()
    send_email(news)
