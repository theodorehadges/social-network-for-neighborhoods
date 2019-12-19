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


friend_query = "(select tm.thread_id, tm.title \
            from userm u inner join friend f on u.id = f.user_1_id or u.id \
            = f.user_2_id \
            inner join thread_friend tf on f.id = tf.friend_id \
            inner join thread_message tm on tf.thread_id = tm.thread_id \
            where u.id = 4 \
            and (tm.body ilike :search_text \
            or tm.title ilike :search_text))"

neighbor_query = "(select tm.thread_id, tm.title \
        from userm u inner join neighbor n on u.id = n.user_1_id or u.id \
            = n.user_2_id \
            inner join thread_friend tf on n.id = tf.friend_id \
            inner join thread_message tm on tf.thread_id = tm.thread_id \
            where u.id = 4 \
            and (tm.body ilike :search_text  \
            or tm.title ilike :search_text))" 

neighborhood_query = "(select tm.thread_id, tm.title \
            from userm u inner join block b on u.block_id = b.id \
            inner join neighborhood nh on b.neighborhood_id = nh.id \
            inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id \
            inner join thread_message tm on tm.thread_id =tnh.thread_id \
            where u.id = 4 \
            and (tm.body ilike :search_text  \
            or tm.title ilike :search_text))"

block_query = "(select tm.thread_id, tm.title \
            from userm u inner join thread_block tb \
            on u.block_id = tb.block_id \
            inner join thread_message tm on tm.thread_id =tb.thread_id \
            where u.id = 4 \
            and (tm.body ilike :search_text  \
            or tm.title ilike :search_text))"


# TODO: add case when no results found
def search_threads(uid, search_type, search_text):
    search_text = "%" + search_text + "%"
    #search_text = "%bicycle"
    if search_type == "all":
        query = friend_query + 'union' + neighbor_query + 'union' \
                + neighborhood_query + 'union' + block_query
        result = db.session.execute(
            query,
            {'uid': uid, 'search_type': search_type, \
                    'search_text': search_text}
            )
    elif search_type == "friend":
        query = friend_query
        result = db.session.execute(
            query,
            {'uid': uid, 'search_type': search_type, \
                    'search_text': search_text}
            )
    elif search_type == "neighbor":
        query = neighbor_query
        result = db.session.execute(
            query,
            {'uid': uid, 'search_type': search_type, \
                    'search_text': search_text}
            )
    elif search_type == "neighborhood":
        query = neighborhood_query
        result = db.session.execute(
            query,
            {'uid': uid, 'search_type': search_type, \
                    'search_text': search_text}
            )
    elif search_type == "block":
        query = block_query
        result = db.session.execute(
            query,
            {'uid': uid, 'search_type': search_type, \
                    'search_text': search_text}
            )
    else:
        return("no type specified. (shouldn't get here)")
    return (result)


# note: redirect to thread

# note: make sure to add db.session.commit() at end






def get_messages_by_thread_id(thread_id):
    messages = db.session.execute(
        """select distinct tm.id, u.username, tm.title, tm.body
        from thread_message tm inner join userm u on tm.author = u.id
        where tm.thread_id = :ti
        order by tm.id asc""",
        {"ti": thread_id}
    )
    return messages


def insert_message_reply(thread_id, cu_id, title, body):
    message = db.session.execute(
            """with rows as (insert into thread_message(thread_id, author, created_time, title, body, lat, long)
            values(:thread_id, :cu_id, now(), :title, :body, NULL, NULL
            ) RETURNING id)
            select id from rows;
            """,
        {"thread_id": thread_id, "cu_id": cu_id, "title": title, "body": body}).fetchone()
    db.session.commit()
    return message[0]


def insert_message_read(message_id, thread_id, cu_id):
    db.session.execute(
        """
        insert into message_read(message_id, thread_id, user_id)
        (select :message_id, :thread_id, friend_id as uid
from thread_friend tf
where tf.thread_id = :thread_id)
union
--neighbor
(select :message_id, :thread_id,  tn.neighbor_id as uid
from thread_neighbor tn
where tn.thread_id = :thread_id
)
union
--neighborhood
(select :message_id, :thread_id, u.id as uid
from thread_block tb inner join userm u on tb.block_id = u.block_id
where tb.thread_id = :thread_id)
union
--block
(select :message_id, :thread_id, u.id as uid
from thread_neighborhood tnn inner join block b on tnn.neighborhood_id = b.neighborhood_id
inner join userm u on b.id = u.block_id
where tnn.thread_id = :thread_id)
        """,
        {"thread_id": int(thread_id), "message_id": message_id}
    )
    db.session.commit()


def update_message_read(message_id, thread_id, cu_id):
    db.session.execute(
        """
        update message_read
        set read = TRUE 
        where thread_id = :thread_id
        and message_id = :message_id
        and user_id = :cu_id
        """,
        {"thread_id": int(thread_id), "message_id": message_id, "cu_id": cu_id}
    )

def get_user_list(cu_id):
    users = db.session.execute(
        """select id, username, firstname, lastname
        from userm
        where id != :cu_id""",
        {"cu_id": cu_id}
    )
    return users


def make_request_record(cu_id, friend_id):
    db.session.execute(
        """insert into friend_request(user_1_id, user_2_id,approved, created_on)
            values(:cu_id, :friend_id, NULL, now())""",
        {"cu_id": cu_id, "friend_id": friend_id}
    )
    db.session.commit()


def get_pending_friends(cu_id):
    """Only need to check for user_id_2 because everytime we request a friend the requester is user_id_1 and the person
    who needs to respond is user_id_2"""
    users = db.session.execute(
        """select fr.user_1_id, u.username, u.firstname, u.lastname
        from friend_request as fr inner join userm as u on fr.user_1_id = u.id 
        where fr.user_2_id = :cu_id
        and fr.approved is NULL""",
        {"cu_id": cu_id}
    )
    return users


def update_request_friends(cu_id, user_1_id, approved):
    db.session.execute(
        """update friend_request
        set approved = :approved
        where user_1_id = :user_1_id
        and user_2_id = :cu_id
        and approved is NULL""",
        {"approved": approved, "user_1_id": user_1_id, "cu_id": cu_id}
    )
    db.session.commit()