import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Short_weather import fetch_weather, filter_weather_data

stadiums = [
    {"name": "서울월드컵경기장", "nx": 60, "ny": 127},
    {"name": "부산아시아드주경기장", "nx": 98, "ny": 76},
    {"name": "인천문학경기장", "nx": 55, "ny": 124},
    {"name": "대구스타디움", "nx": 89, "ny": 90},
    {"name": "광주월드컵경기장", "nx": 58, "ny": 74},
    {"name": "대전월드컵경기장", "nx": 67, "ny": 100},
    {"name": "수원월드컵경기장", "nx": 61, "ny": 120},
    {"name": "울산문수축구경기장", "nx": 102, "ny": 84},
    {"name": "포항스틸야드", "nx": 102, "ny": 94},
    {"name": "제주월드컵경기장", "nx": 53, "ny": 38}
]


def send_weather_email(sender, password, recipient, subject, weather_data):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    text = f"날씨 정보:\n강수확률: {weather_data.get('POP', 'N/A')}\n강수형태: {weather_data.get('PTY', 'N/A')}\n습도: {weather_data.get('REH', 'N/A')}\n하늘상태: {weather_data.get('SKY', 'N/A')}"
    html = f"""\
    <html>
      <body>
        <p>날씨 정보:<br>
           강수확률: {weather_data.get('POP', 'N/A')}<br>
           강수형태: {weather_data.get('PTY', 'N/A')}<br>
           습도: {weather_data.get('REH', 'N/A')}<br>
           하늘상태: {weather_data.get('SKY', 'N/A')}
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    sender = input("Enter your Gmail address: ")
    password = input("Enter your Gmail password: ")
    recipient = input("Enter recipient email address: ")
    subject = "Weather Information"

    print("Select a stadium:")
    for i, stadium in enumerate(stadiums):
        print(f"{i + 1}. {stadium['name']}")

    choice = int(input("Enter the number of the stadium: "))
    selected_stadium = stadiums[choice - 1]

    weather_data = fetch_weather(selected_stadium['nx'], selected_stadium['ny'])
    filtered_weather_data = filter_weather_data(weather_data)

    send_weather_email(sender, password, recipient, subject, filtered_weather_data)
