import smtplib

def xterm_mail(RECIEVER_EMAIL, ACCESS_KEY, REMARKS):
    SENDER_EMAIL = '-------------'
    SENDER_PASS = '**********'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)

    msg = """
        Hello, Sir/Ma'am.
        This is your access key : {} !!

            Thank you.
            Keep it confidential !!!

        {}
        """.format(ACCESS_KEY, REMARKS)

    server.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, msg)
    server.quit()

    return "Your mail has been sent. Thank you !!"


if __name__ == "__main__":
    main()
