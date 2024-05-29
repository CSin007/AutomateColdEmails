from bs4 import BeautifulSoup
import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import webbrowser

def findEmail(emailURL):
    try: 
        html_text = requests.get(emailURL)
        if html_text.status_code == 200:
            soup = BeautifulSoup(html_text.content, 'lxml')
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, str(soup))
            if emails:
                return emails
            else:
                return []
        else:
            return []
    except Exception as e:
        return []

def send_email(emailSend, sender_password, emailRec, subject, body, attachment_path):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(emailSend, sender_password)

        # Create the email message
        message = MIMEMultipart()
        message['From'] = emailSend
        message['To'] = emailRec
        message['Subject'] = subject

        # Attach the body text
        message.attach(MIMEText(body, 'plain'))

        # Attach the PDF file
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            message.attach(part)

        # Send the email
        server.sendmail(emailSend, emailRec, message.as_string())

        # Close the connection
        server.quit()
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    emailURL = input("Enter the URL you want to search: ")
    emailList = findEmail(emailURL)
    if emailList:
        for string in emailList:
            print(string)
        emailRec = input("Enter receiver email: ")
        emailSend = input("Enter sender email: ")
        sender_password = input("Enter your email password: ")

        subject = "Opportunity to Apply for Internship"
        body = f"Dear Hiring Manager,\n\nI hope this email finds you well. My name is [Your Name] and I am writing to express my interest in the internship opportunity at [Company Name].\n\nI am a [Your Current Year/Major/Field of Study] at [Your University/College], and I am particularly excited about the opportunity to contribute to [Company Name] because of [mention any specific projects, values, or initiatives of the company that resonate with you].\n\nI have experience in [mention relevant experiences, skills, or projects], and I am eager to further develop my skills and contribute to [Company Name]'s success.\n\nPlease find attached my resume for your review. I look forward to the possibility of discussing this exciting opportunity with you further.\n\nThank you for your time and consideration.\n\nSincerely,\n[Your Name]"

        attachment_path = "resume.pdf"  # Replace with the actual file name of your resume

        # Sending the email
        if send_email(emailSend, sender_password, emailRec, subject, body, attachment_path):
            print("Email sent successfully!")
        else:
            print("Failed to send email. Please check your credentials and try again.")

        # Open default email application
        webbrowser.open('mailto:' + emailRec)
    else:
        print("No emails could be scraped from the page")
