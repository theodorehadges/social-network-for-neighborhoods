from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'userm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.LargeBinary())
    email = db.column(db.String(255))


def get_thread_friend_unread(uid):
    rows = db.session.execute(
        """select distinct tf.thread_id, tm.title, tm.author, tm.body
        from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
        inner join thread_friend tf on f.id = tf.friend_id
        inner join thread_message tm on tf.thread_id = tm.thread_id
        inner join message_read mr on u.id = mr.user_id and tm.id = mr.message_id
        where u.id = :uid
        and mr.read = False;""",
        {'uid': uid}
    )
    return rows


def make_thread(uid, title, body):
    thread = db.session.execute(
        """with rows as (
    insert into thread (created_on) VALUES (now()) RETURNING id
), em as (
    insert into thread_message(thread_id, author, created_time, title, body, lat, long)
    SELECT id, :uid, now(), :title , :body,
    28.439743, 34.48948
    from rows)
    select id from rows;""",
        {'uid': uid, 'title': title, 'body': body}
    ).fetchone()
    return thread[0]


def get_messages_by_thread_id(thread_id):
    messages = db.session.execute(
        """select distinct tm.thread_id, tm.id, tm.title, tm.author, tm.body
        from thread_message tm
        where tm.thread_id = :ti""",
        {"ti": thread_id}
    )
    return messages


def get_user_list():
    users = db.session.execute(
        """select id, firstname, lastname
        from userm""")
    return(users)
