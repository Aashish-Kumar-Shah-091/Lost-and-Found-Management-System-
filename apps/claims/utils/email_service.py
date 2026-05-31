import resend
from django.conf import settings


# initialize API key
resend.api_key = settings.RESEND_API_KEY


def send_lost_found_email(to_email, item_name):
    subject = "Match Found for Your Lost Item"

    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color:#2c3e50;">🎉 Match Found!</h2>

        <p>Good news! We may have found a match for your lost item.</p>

        <h3>Item: {item_name}</h3>

        <p>Please log in to your dashboard to review the details.</p>

        <a href="http://127.0.0.1:8000/dashboard/"
           style="display:inline-block;
                  padding:10px 20px;
                  background:#4CAF50;
                  color:white;
                  text-decoration:none;
                  border-radius:5px;">
           Check Dashboard
        </a>

        <p style="margin-top:20px;">— Lost & Found System</p>
    </div>
    """

    params = {
        "from": "Lost & Found <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": html_content,
    }

    return resend.Emails.send(params)