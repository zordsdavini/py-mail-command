py-mail-command
===============

Script to read mails and execute commands by instructions. This should be run as cron job.

**Usage**

Script reads mail form mailbox. It would be good to make separate mailbox per host. Mail body should contain host, command, arguments. Ex.:

    HOME dir

**Configuration**

Config should be saved in ~/.config/mail_command.conf
Example:

    [mail]
    server: mail.somewhere.lt
    ssl: 1
    user: username
    password: super_druper_password
    
    [commands]
    host: HOME
    dir: ls -m
    proc: ps ax
