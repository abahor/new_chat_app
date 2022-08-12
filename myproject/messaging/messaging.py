import uuid
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, abort, session
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, emit, disconnect
from sqlalchemy import or_, and_

from myproject import db, socketio
from myproject.models import Rooms, UsersModel, Messages

messaging = Blueprint('messaging', __name__, template_folder="temp", )


@messaging.route('/chats')
@login_required
def chating():
    # db.session.query(Rooms)
    # rooms = Rooms.query.filter_by(participant_one=current_user.id).filter_by(participant_two=current_user.id)
    rooms = Rooms.query.filter(or_(Rooms.participant_one == current_user.id, Rooms.participant_two == current_user.id))

    # rooms = select(Rooms).where(or_(users_table.c.name='wendy',users.c.name='jack'))
    # rooms = Rooms.query.filter(or_(participant_1=current_user.id, participant_2=current_user.id))
    # room = Rooms.query.filter_by(participant_1= current_user.id)
    # roo = Rooms.query.filter_by(participant_2=current_user.id)

    print(rooms)
    users_list = []
    for i in rooms:
        users_list.append(get_user_by_id(i))
    return render_template('chats.html', users_list=users_list)


@messaging.route('/start_new_chat/<int:id_of_user>')
@login_required
def start_new_chat(id_of_user):
    a = Rooms.query.filter(or_(and_(Rooms.participant_one == current_user.id, Rooms.participant_two == id_of_user),
                               and_(Rooms.participant_one == id_of_user,
                                    Rooms.participant_two == current_user.id))).all()
    print(a)
    if a:
        return abort(404)
    print('---------------')
    if current_user.id == id_of_user:
        return abort(404)
    ch = Rooms(participant_1=current_user.id, uui=str(uuid.uuid1()), participant_2=id_of_user)
    try:
        db.session.add(ch)
        db.session.commit()
        print('commit happened ')
    except:
        db.session.rollback()
        print('============= A rollback happened ===============')
    return redirect(f'/messaging/{id_of_user}')


@messaging.route('/messaging/<int:user_id>', methods=['post', 'get'])
def messaging_users(user_id):
    a = Rooms.query.filter(or_(and_(Rooms.participant_one == current_user.id, Rooms.participant_two == user_id),
                               and_(Rooms.participant_one == user_id,
                                    Rooms.participant_two == current_user.id))).first()
    print(a)
    if not a:
        return abort(404)
    messages = [Messages.query.filter(or_(and_(Messages.SenderID == current_user.id, Messages.ReceiverID == user_id)
                                          , and_(Messages.ReceiverID == current_user.id,
                                                 Messages.SenderID == user_id))).order_by(
        Messages.timestamp.asc()).all()]
    print(a)
    session['room'] = str(a.uu)
    session['other_id'] = str(user_id)
    print(messages)
    return render_template('messaging.html', messages=messages[0], )


def get_user_by_id(i):
    if i.participant_one == current_user.id:
        return UsersModel.query.get_or_404(i.participant_two)
    else:
        return UsersModel.query.get_or_404(i.participant_one)


# def arrange()
@socketio.on('connect')
@login_required
def connect():
    if not session['room']:
        return
    join_room(session['room'])


@socketio.on('disconnect')
def on_leave():
    try:
        leave_room(session['room'])
        session.pop('room')
        session.pop('other_id')
    except:
        pass


@socketio.on('send_message')
@login_required
def message(msg):
    print(session['other_id'])
    if not session['other_id']:
        disconnect()
    mes = Messages(senderid=current_user.id, text=msg['text'],
                   receiverid=session['other_id'], timestamp=datetime.utcnow())
    try:
        db.session.add(mes)
        db.session.commit()
    except:
        db.session.rollback()
    emit('new_message', {'text': msg, 'sender': current_user.id}, to=session['room'])
