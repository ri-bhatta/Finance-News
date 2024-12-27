import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Function to fetch RBI news from Google Custom Search
def fetch_rbi_news():
    search_engine_id = "759053462c1944ac0"  # Your Search Engine ID
    query = "Reserve Bank of India"
    google_cse_url = f"https://cse.google.com/cse?cx={search_engine_id}&q={query}"
    
    response = requests.get(google_cse_url)
    if response.status_code != 200:
        return "Failed to fetch news. Please check the Custom Search URL."

    # Extract relevant information from the HTML response
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='gsc-webResult gsc-result')  # Adjust selector as needed
    
    news_content = ""
    for idx, result in enumerate(results[:5], 1):  # Limit to top 5 results
        title_tag = result.find('a', class_='gs-title')
        url = result.find('a')['href'] if title_tag else "No URL"
        title = title_tag.text if title_tag else "No Title"
        news_content += f"{idx}. {title}\n"
        news_content += f"   URL: {url}\n\n"
    
    return news_content or "No news found for today."

# Function to send an email
def send_email(news_content):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_email_password"  # Replace with your email password
    recipient_email = "recipient_email@example.com"  # Replace with recipient's email
    
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
