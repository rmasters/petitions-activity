import datetime
import logging
import sqlite3
import os
from babel.dates import format_timedelta
import dateutil.parser
from flask import Flask, render_template, g
import requests

PETITION_ID = 241584

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect(os.environ.get('DB_PATH'))
        g._database.row_factory = dict_factory
        db = g._database

    return db


@app.template_filter('number_format')
def number_format(value):
    return '{:,d}'.format(value)


@app.template_filter('relative_date')
def relative_date(value):
    delta = datetime.datetime.utcnow() - value
    return format_timedelta(delta, locale='en_GB')


@app.cli.command('init_db')
def init_db():
    db = get_db()
    db.cursor().executescript("""
    CREATE TABLE petition_signatures (
        id INTEGER PRIMARY KEY,
        petition_id INTEGER,
        recorded_at DATETIME,
        signature_count BIGINTEGER
    )
    """)
    db.commit()


@app.cli.command('track_petition')
def track_petition():
    resp = requests.get(f"https://petition.parliament.uk/petitions/{PETITION_ID}/count.json")
    data = resp.json()

    if 'signature_count' not in data:
        logging.warn("Couldn't access petition count (HTTP %d: %s)" % (resp.status_code, resp.text))
        return

    conn = get_db()
    signature_count = data['signature_count']
    recorded_at = datetime.datetime.utcnow()
    conn.execute(
            """insert into petition_signatures (petition_id, recorded_at, signature_count) values (?, ?, ?)""",
            (PETITION_ID, recorded_at, signature_count)
            )
    conn.commit()

    logging.info("Recorded %d signatures at %s" % (signature_count, recorded_at.strftime('%Y-%m-%dT%H:%M:%S')))


@app.cli.command('render')
def render():
    rendered = petition()

    with open(os.path.join(os.environ.get('RENDER_PATH'), 'index.html'), 'w') as f:
        f.write(rendered)


@app.route("/petition")
def petition():
    conn = get_db()
    latest_update = conn.execute("select recorded_at, signature_count from petition_signatures order by recorded_at desc limit 1").fetchone()

    return render_template('petition.html',
            total_signatures=latest_update['signature_count'],
            updated_at=dateutil.parser.parse(latest_update['recorded_at']),
            rendered_at=datetime.datetime.utcnow()
            )

