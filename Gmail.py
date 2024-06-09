import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Short_weather import fetch_weather, filter_weather_data
from tkinter import simpledialog, messagebox, Toplevel, StringVar, Label, OptionMenu, Button

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

def send_weather_email(sender, password, recipient, subject, stadium_name, weather_data):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    text = f"경기장: {stadium_name}\n날씨 정보:\n강수확률: {weather_data.get('POP', 'N/A')}\n강수형태: {weather_data.get('PTY', 'N/A')}\n습도: {weather_data.get('REH', 'N/A')}\n하늘상태: {weather_data.get('SKY', 'N/A')}"
    html = f"""\
    <html>
      <body>
        <p>경기장: {stadium_name}<br>
           날씨 정보:<br>
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

def get_email_details(root):
    sender = simpledialog.askstring("Sender Email", "Enter your Gmail address:", parent=root)
    if not sender:
        return

    password = simpledialog.askstring("Password", "Enter your Gmail password:", show='*', parent=root)
    if not password:
        return

    recipient = simpledialog.askstring("Recipient Email", "Enter recipient email address:", parent=root)
    if not recipient:
        return

    subject = "Weather Information"

    # Select stadium
    stadium_window = Toplevel(root)
    stadium_window.title("Select Stadium")

    Label(stadium_window, text="Select a stadium:").pack(pady=10)
    selected_stadium_var = StringVar(stadium_window)
    selected_stadium_var.set(stadiums[0]['name'])

    stadium_menu = OptionMenu(stadium_window, selected_stadium_var, *[stadium['name'] for stadium in stadiums])
    stadium_menu.pack(pady=10)

    submit_button = Button(stadium_window, text="Submit", command=lambda: send_email_details(sender, password, recipient, subject, selected_stadium_var, stadium_window))
    submit_button.pack(pady=10)

def send_email_details(sender, password, recipient, subject, selected_stadium_var, stadium_window):
    selected_stadium_name = selected_stadium_var.get()
    selected_stadium = next(stadium for stadium in stadiums if stadium['name'] == selected_stadium_name)

    weather_data = fetch_weather(selected_stadium['nx'], selected_stadium['ny'])
    filtered_weather_data = filter_weather_data(weather_data)

    try:
        send_weather_email(sender, password, recipient, subject, selected_stadium_name, filtered_weather_data)
        messagebox.showinfo("Success", "Email sent successfully!", parent=stadium_window)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}", parent=stadium_window)

    stadium_window.destroy()
