import configparser
import poplib
from email import parser
from os.path import expanduser
from subprocess import check_output


# prepare config for reading
config = configparser.ConfigParser()
config.read(expanduser("~") + '/.config/mail_command.conf')

# connect to mail server
if config.getboolean('mail', 'ssl'):
    pop_conn = poplib.POP3_SSL(config.get('mail', 'server'))
else:
    pop_conn = poplib.POP3(config.get('mail', 'server'))

pop_conn.user(config.get('mail', 'user'))
pop_conn.pass_(config.get('mail', 'password'))

# get messages from server
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# concat message pieces
messages = [b"\n".join(mssg[1]) for mssg in messages]
# parse message intom an email object
messages = [parser.BytesParser().parsebytes(mssg) for mssg in messages]
for i, message in enumerate(messages):
    body = message.get_payload().split("\n")
    for row in body:
        e = row.split(' ')
        
        # check is host is same as in config
        if e[0] != config.get('commands', 'host'):
            continue

        try:
            command = config.get('commands', e[1]).split(' ')
            out = check_output(command)
            print(out)

            # delete executed message
            pop_conn.dele(i + 1)
        except:
            continue

# close mail
pop_conn.quit()
