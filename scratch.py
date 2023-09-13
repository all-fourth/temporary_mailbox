"""Imports."""
from os import getcwd, makedirs, path
from random import choice
from string import ascii_lowercase, digits
from time import sleep

from requests import get, post

API = 'https://www.1secmail.com/api/v1/'
domain_list = [
  '1secmail.com',
  '1secmail.org',
  '1secmail.net',
]
domain = choice(domain_list)


def generate_username():
    """Return username."""
    name = ascii_lowercase + digits
    username = ''.join(choice(name) for _ in range(10))

    return username


def check_mail(mail=''):
    """Check new mails."""
    req_link = '{}?action=getMessages&login={}&domain={}'.format(
        API, mail.split('@')[0], mail.split('@')[1])

    request = get(req_link, timeout=10).json()
    length = len(request)

    if length == 0:
        print("You don't have new mails at this moment.")
    else:
        id_list = []

        for _ in request:
            for key, value in _.items():
                if key == 'id':
                    id_list.append(value)
        print('You have {} new mails'.format(length))

        current_dir = getcwd()
        final_dir = path.join(current_dir, 'all_mails')

        if not path.exists(final_dir):
            makedirs(final_dir)

        for _ in id_list:
            read_msg = '{}?action=readMessage&login={}&domain={}&id={}'.format(
                API, mail.split('@')[0], mail.split('@')[1], _)

            request = get(read_msg, timeout=10).json()
            sender = request.get('from')
            subject = request.get('subject')
            date = request.get('date')
            content = request.get('textBody')
            mail_file_path = path.join(final_dir, '{}.txt'.format(_))

            with open(mail_file_path, 'w') as file:
                file.write('Sender: {}\nTo: {}\nSubject: {}\nDate: {}\n'
                           'Content: {}'
                           .format(sender, mail, subject, date, content))


def delete_mail(mail=''):
    """Delete mails."""
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1],
    }
    post(url, data=data, timeout=10)
    print('Email address {} is deleted\n'.format(mail))


def main(mail=''):
    """Use main function."""
    try:
        username = generate_username()
        mail = '{}@{}'.format(username, domain)
        print('Your new email: {}'.format(mail))

        get('{}?login={}&domain={}'
            .format(API, mail.split('@')[0], mail.split('@')[1]), timeout=10)

        while True:
            check_mail(mail=mail)
            sleep(5)

    except KeyboardInterrupt:
        delete_mail(mail=mail)
        print('Program interrupted by user')


if __name__ == '__main__':
    main()
