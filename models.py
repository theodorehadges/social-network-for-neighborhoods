from flask_login import UserMixin
from sqlalchemy import text, bindparam

from app import db
import requests


class User(UserMixin, db.Model):
    __tablename__ = 'userm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.LargeBinary())
    email = db.column(db.String(255))
    block_id = db.Column(db.Integer)


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

def get_profile_info_from_uid(uid):
    record = db.session.execute(
        """select u.firstname, u.lastname, u.description, u.photo, u.lat, u.long 
        from userm u
        where u.id = :uid;""",
        {'uid': uid}
    ).fetchone()
    return record


def make_thread(uid, title, body, type, uids):
    thread = db.session.execute(
            """with rows as (insert into thread(name, created_on) VALUES (:title, now()) RETURNING id)
    select id from rows;
            """,
        {"title": title}).fetchone()
    insert_type_thread_query(thread[0], type, uid, uids)
    insert_message_reply(thread[0], uid, title, body)
    db.session.commit()
    return thread[0]


def insert_type_thread_query(thread_id, type, cu_id, uids):
    if type == "friend":
        query = """insert into thread_friend(thread_id, friend_id) 
                    (select :thread_id, id
                    from friend
                    where user_1_id = :uid
                    and user_2_id = :cu_id)
                    union
                    (select :thread_id, id
                    from friend
                    where user_1_id = :cu_id
                    and user_2_id = :uid)"""
        for uid in uids:
            db.session.execute(query, {"thread_id": thread_id, "cu_id": cu_id, "uid": uid})
        db.session.commit()
    elif type == "neighborhood":
        query = """insert into thread_neighborhood(thread_id, neighborhood_id) 
                    select :thread_id, neighborhood_id 
                    from userm u inner join block b on b.id = u.block_id
                    inner join neighborhood n on n.id = b.neighborhood_id 
                    where u.id = :cu_id"""
        db.session.execute(query, {"thread_id": thread_id, "cu_id": cu_id, "uid": uids})
        db.session.commit()
    elif type == "neighbor":
        query = """insert into thread_neighbor(thread_id, neighbor_id) 
                    (select :thread_id, id
                    from neighbor
                    where user_1_id = :uid
                    and user_2_id = :cu_id)
                    union
                    (select :thread_id, id
                    from neighbor
                    where user_1_id = :cu_id
                    and user_2_id = :uid)"""
        for uid in uids:
            db.session.execute(query, {"thread_id": thread_id, "cu_id": cu_id, "uid": uid})
        db.session.commit()
    elif type == "block":
        query = """insert into thread_block(thread_id, block_id) 
                    select :thread_id, block_id 
                    from userm
                    where id = :cu_id"""
        db.session.execute(query, {"thread_id": thread_id, "cu_id": cu_id, "uid": uids})
        db.session.commit()
    else:
        print("something went wrong couldn't insert into anything")
    # t = text(query)
    # t = t.bindparams(bindparam('uids', expanding=True))


friend_query = "(select tm.thread_id, tm.title \
            from userm u inner join friend f on u.id = f.user_1_id or u.id \
            = f.user_2_id \
            inner join thread_friend tf on f.id = tf.friend_id \
            inner join thread_message tm on tf.thread_id = tm.thread_id \
            where u.id = :uid \
            and (tm.body ilike :search_text \
            or tm.title ilike :search_text))"

neighbor_query = """(select tm.thread_id, tm.title 
        from userm u inner join neighbor n on u.id = n.user_1_id or u.id 
            = n.user_2_id 
            inner join thread_neighbor tn on n.id = tn.neighbor_id 
            inner join thread_message tm on tn.thread_id = tm.thread_id 
            where u.id = :uid 
            and (tm.body ilike :search_text  
            or tm.title ilike :search_text))"""

neighborhood_query = "(select tm.thread_id, tm.title \
            from userm u inner join block b on u.block_id = b.id \
            inner join neighborhood nh on b.neighborhood_id = nh.id \
            inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id \
            inner join thread_message tm on tm.thread_id =tnh.thread_id \
            where u.id = :uid \
            and (tm.body ilike :search_text  \
            or tm.title ilike :search_text))"

block_query = "(select tm.thread_id, tm.title \
            from userm u inner join thread_block tb \
            on u.block_id = tb.block_id \
            inner join thread_message tm on tm.thread_id =tb.thread_id \
            where u.id = :uid \
            and (tm.body ilike :search_text  \
            or tm.title ilike :search_text))"

def get_recent_friend_messages(uid):
    rows = db.session.execute(
        """select distinct tf.thread_id, tm.title, tm.created_time
        from userm u inner join friend f on u.id = f.user_1_id or u.id = f.user_2_id
        inner join thread_friend tf on f.id = tf.friend_id
        inner join thread_message tm on tf.thread_id = tm.thread_id
        where u.id = :uid
        order by tm.created_time desc
        limit 2""",
        {'uid': uid}
    )
    return rows

def get_recent_neighbor_messages(uid):
    rows = db.session.execute(
        """select distinct tm.thread_id, tm.title, tm.created_time\
        from userm u inner join neighbor n on u.id = n.user_1_id or u.id \
        = n.user_2_id \
        inner join thread_neighbor tn on n.id = tn.neighbor_id \
        inner join thread_message tm on tn.thread_id = tm.thread_id \
        where u.id = :uid \
        order by tm.created_time desc
        limit 2""" ,
        {'uid': uid}
    )
    return rows

def get_recent_neighborhood_messages(uid):
    rows = db.session.execute(
        """select tm.thread_id, tm.title, tm.created_time \
        from userm u inner join block b on u.block_id = b.id \
        inner join neighborhood nh on b.neighborhood_id = nh.id \
        inner join thread_neighborhood tnh on nh.id = tnh.neighborhood_id \
        inner join thread_message tm on tm.thread_id =tnh.thread_id \
        where u.id = :uid \
        order by tm.created_time desc
        limit 2""",
        {'uid': uid}
    )
    return rows

def get_recent_block_messages(uid):
    rows = db.session.execute(
        """select tm.thread_id, tm.title, tm.created_time \
        from userm u inner join thread_block tb \
        on u.block_id = tb.block_id \
        inner join thread_message tm on tm.thread_id = tb.thread_id \
        where u.id = :uid \
        order by tm.created_time desc \
        limit 2""",
        {'uid': uid}
    )
    return rows





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
    return result


# note: redirect to thread

# note: make sure to add db.session.commit() at end






def get_messages_by_thread_id(thread_id, cu_id):
    messages = db.session.execute(
        """select distinct tm.id, u.username, tm.title, tm.body, tm.created_time, mr.read
        from thread_message tm inner join userm u on tm.author = u.id
        inner join message_read mr on tm.id = mr.message_id and tm.thread_id = mr.thread_id
        where tm.thread_id = :ti
        and mr.user_id = :cu_id
        order by tm.id asc;""",
        {"ti": thread_id, "cu_id": cu_id}
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
    insert_message_read(message[0], thread_id, cu_id)
    update_message_read(message[0], thread_id, cu_id)
    return message[0]


def insert_message_read(message_id, thread_id, cu_id):
    db.session.execute(
        """
        insert into message_read(message_id, thread_id, user_id, read)
        ((select :message_id, :thread_id, user_1_id as uid, FALSE
from thread_friend tf inner join friend f on tf.friend_id = f.id
where tf.thread_id = :thread_id)
union
(select :message_id, :thread_id, user_2_id as uid, FALSE
from thread_friend tf inner join friend f on tf.friend_id = f.id
where tf.thread_id = :thread_id))
union
--neighbor
((select :message_id, :thread_id, user_1_id as uid, FALSE
from thread_neighbor tn inner join neighbor n on tn.neighbor_id = n.id
where tn.thread_id = :thread_id)
union
(select :message_id, :thread_id, user_2_id as uid, FALSE
from thread_neighbor tn inner join neighbor n on tn.neighbor_id = n.id
where tn.thread_id = :thread_id))
union
--neighborhood
(select :message_id, :thread_id, u.id as uid, FALSE
from thread_block tb inner join userm u on tb.block_id = u.block_id
where tb.thread_id = :thread_id)
union
--block
(select :message_id, :thread_id, u.id as uid, FALSE
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
    db.session.commit()

def get_user_list(cu_id):
    users = db.session.execute(
        """select id, username, firstname, lastname
        from userm
        where id != :cu_id""",
        {"cu_id": cu_id}
    )
    return users


def get_user_list_minus_neighbors(cu_id):
    users = db.session.execute(
        """(select id, username, firstname, lastname
        from userm
        where id != :cu_id)
        except
        (with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from neighbor
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname
        from uf inner join userm u on uf.uf_id = u.id)""",
        {"cu_id": cu_id}
    )
    return users


def get_user_list_minus_friends(cu_id):
    users = db.session.execute(
        """(select id, username, firstname, lastname
        from userm
        where id != :cu_id)
        except
        (with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from friend
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname
        from uf inner join userm u on uf.uf_id = u.id)
        except
        (with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from friend_request
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname
        from uf inner join userm u on uf.uf_id = u.id)""",
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

def get_all_friends(cu_id):
    friends = db.session.execute(
          """with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from friend
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname, u.lat, u.long
        from uf inner join userm u on uf.uf_id = u.id""",
          {"cu_id": cu_id}
    )
    return friends 

def get_all_neighbors(cu_id):
    neighbors = db.session.execute(
        """with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from neighbor
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname, u.lat, u.long
        from uf inner join userm u on uf.uf_id = u.id""",
            {"cu_id": cu_id}
    )
    return neighbors

def get_lat_lon_from_address(street, city, state):
    API_KEY = "AIzaSyDZ9FKI0IjDZJJK5vEyDb_Temr3QyZLfVs" 
    
    response = requests.get( \
            'https://maps.googleapis.com/maps/api/geocode/json?address=' \
            + street + ',' + city + ',' + state + '&key=' + API_KEY)
    resp_json_payload = response.json()
    
    return(resp_json_payload['results'][0]['geometry']['location'])




def insert_user(reg_form, bcrypt_hash, lat, lon):
    username = reg_form.username.data
    firstname = reg_form.firstname.data
    lastname = reg_form.lastname.data
    email = reg_form.email.data
    street = reg_form.street.data
    city = reg_form.city.data
    zipcode = reg_form.zipcode.data
    state = reg_form.state.data
    description = reg_form.description.data
    password = bcrypt_hash
    db.session.execute(
        """
        insert into userm(username, password, firstname, lastname, email,
        description, street, city, state, zipcode, lat, long, created_on) 
        values(:username, :password, :firstname, :lastname, :email,
        :description, :street, :city, :state, :zipcode, :lat, :long, now())
        """,
        {"username": username, "password": password,
         "firstname": firstname, "lastname": lastname, "email": email,
         "description": description, "street": street, "city": city, 
         "state": state, "zipcode": zipcode, "lat": lat, "long": lon}
    )
    db.session.commit()

def get_neighborhoods():
    neighborhoods = db.session.execute(
        """
        select id, name
        from neighborhood
        """,
        {}
    )
    return neighborhoods


def get_blocks(neighborhood_id):
    blocks = db.session.execute(
        """
        select id, name
        from block
        where neighborhood_id = :neighborhood_id
        """,
        {"neighborhood_id": neighborhood_id}
    )
    return blocks


def insert_into_block_apply(cu_id, block_id):
    db.session.execute(
        """
        insert into block_apply(pending_user, need_approval_by, block_id, created_on)
        select :cu_id, id, :block_id, now()
        from userm
        where id != :cu_id
        and block_id = :block_id;
        """,
        {"cu_id": cu_id, "block_id": block_id}
    )
    db.session.commit()


def insert_into_neighbors(cu_id, friend_id):
    db.session.execute(
        """
        insert into neighbor(user_1_id, user_2_id) 
values(:cu_id, :friend_id)
        """,
        {"cu_id": cu_id, "friend_id": friend_id}
    )
    db.session.commit()


def get_all_neighbors(cu_id):
    users = db.session.execute(
          """with uf as (select coalesce(nullif(user_1_id, :cu_id), user_2_id) as uf_id
        from neighbor
        where user_1_id = :cu_id
        or user_2_id = :cu_id)
        select u.id, u.username, u.firstname, u.lastname
        from uf inner join userm u on uf.uf_id = u.id""",
          {"cu_id": cu_id}
    )
    return users


def get_neighbors_from_block(cu_id, block_id):
    users = db.session.execute(
    """
    select id
    from userm
    where block_id = :block_id
    and id != :cu_id;
    """,
    {"block_id": block_id, "cu_id": cu_id}
    )
    return users


def update_block_on_uid(cu_id, block_id):
    db.session.execute(
        """
        update userm
        set block_id = :block_id
        where id = :cu_id
        """,
        {"cu_id": cu_id, "block_id": block_id}
    )
    db.session.commit()


def get_pending_block_approvals(cu_id):
    users = db.session.execute(
        """select ba.pending_user, u.username, u.firstname, u.lastname
        from block_apply as ba inner join userm as u on ba.pending_user = u.id 
        where ba.need_approval_by = :cu_id
        and ba.given_approval is NULL""",
        {"cu_id": cu_id}
    )
    return users


def update_block_approval(block_id, pending_id, cu_id, approval):
    db.session.execute(
        """
        update block_apply
        set given_approval = :approval
        where block_id = :block_id
        and pending_user = :pending_id
        and need_approval_by = :cu_id
        """,
        {"block_id": block_id, "pending_id": pending_id, "cu_id": cu_id, "approval": approval}
    )
    db.session.commit()
