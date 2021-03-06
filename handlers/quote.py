import sys
sys.path.append("../")

import sqlite
import settings
import utils

def addquote(conn, msg):
    if len(msg.text.split()) > 1:
        quote = ' '.join(msg.text.split()[1:])
        rowid = sqlite.set('INSERT INTO irc_quote (quote) VALUES (?)', (quote,))
        conn.send('PRIVMSG %s :Quote %i added!\r\n' % (msg.channel, rowid))
    else:
        usage = 'Gebruik: !addquote quote'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))

def delquote(conn, msg):
    if msg.user == settings.irc_OWNER or utils.isadmin(conn, msg):
        if len(msg.text.split()) > 1 and msg.text.split()[1].isdigit():
            rowid = sqlite.set('DELETE FROM irc_quote WHERE id=?', (msg.text.split()[1],))
            conn.send('PRIVMSG %s :Quote %i deleted!\r\n' % (msg.channel, int(msg.text.split()[1])))
        else:
            usage = 'Gebruik: !delquote id'
            conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))
    else:
        usage = 'Je moet een operator zijn om dit commando te kunnen gebruiken.'
        conn.send('PRIVMSG %s :%s\r\n' % (msg.user, usage))

def quote(conn, msg):
    parts = msg.text.split()
    if len(parts) == 1: # Random quote
        rows, count = sqlite.get('SELECT * FROM irc_quote ORDER BY RANDOM()', ())

    elif parts[1].isdigit(): # Haal quote nummer zoveel op
        rows, count = sqlite.get('SELECT * FROM irc_quote WHERE id=?', (parts[1],))

    else:
        rows, count = sqlite.get('SELECT * FROM irc_quote WHERE quote LIKE ? ORDER BY RANDOM()', ("%"+parts[1]+"%",))
    if count != 0:
        conn.send('PRIVMSG %s :Quote %i: %s\r\n' % (msg.channel, rows[0][0], rows[0][1]))
