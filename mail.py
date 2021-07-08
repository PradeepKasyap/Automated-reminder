import smtplib
import pandas as pd
import datetime
import os
import random

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():

    # finding absolute path of working folder.
    # This is required to run code on pythonanywhere.com(or other cloud handlers)
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    #reading the schedule
    df = pd.read_csv(os.path.join(THIS_FOLDER, 'schedule.csv'))
    print(df)

    #quite clear
    today = datetime.datetime.today().weekday()
    tomorrow = (today + 1) % 7
    #print(today, tomorrow)

    #getting the list of devs for tomorrow's sevas(this list is arranged to match with sevas)
    list_of_devs = df.iloc[tomorrow, 1:18]


    #making a dictionary of mail ids from mail_list.csv
    dict_of_mailids = {}
    with open(os.path.join(THIS_FOLDER, 'mail_list.csv'), encoding='utf-8-sig') as csvfile:
        for row in csvfile:
            dict_of_mailids[row.split(',')[0].lower()] = row.split(',')[1][:-1]
    #print(dict_of_mailids)


    # ecooking1 devotee also does eoffering
    sevas = [
        'Morning Cooking', 'Morning Cooking', 'Sabji Cutting',
        'Chapati Making', 'Chapati Making', 'Afternoon Cooking and Offering',
        'Evening Cooking, Offering and Deity Garland Removing', 'Evening Cooking','Evening Offering',
        'Prasadam Hall Cleaning in the Afternoon','Prasadam Hall Cleaning in the Evening',
        'Altar Cleaning and probably Morning Offering too',
        'Altar Cleaning and probably Morning Offering too',
        'Temple Hall Cleaning', 'Temple Hall Cleaning', 
        'Vessel Washing', 'Vessel Washing'
    ]

    combined_list = []
    for i in range(len(list_of_devs)):
        combined_list.append((list_of_devs[i], dict_of_mailids[list_of_devs[i].lower().rstrip()], sevas[i]))
    for _ in combined_list:
        print(_)


    # A random chapter of Srila Prabhupada Uvaca to inspire devotees
    link = "www.vedabase.com/en/spu/" + str(random.randint(1,129))



    # Ready for mailing
    MY_ADDRESS = 'laxmanpradeepkasyap@gmail.com'
    PASSWORD = 'zxcft67ujm'
    message_template = read_template(os.path.join(THIS_FOLDER, 'template.txt'))

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email, seva in combined_list:
        if email == '-': continue

        msg = MIMEMultipart()  # create a message

        # add in the actual person name and seva to the message template
        message = message_template.substitute(PERSON_NAME=name.title(), SEVA=seva, LINK=link)

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Seva Reminder"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main() 
