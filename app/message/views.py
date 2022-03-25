from flask import redirect, render_template, redirect,request,url_for,flash
from ..models import User, Message
from .. import db
from . import message
from flask_login import login_required, current_user
from sqlalchemy import desc

#消息列表
@message.route('/receive', methods=['GET'])
@login_required
def receive_message():    
    messages=Message.query.filter_by(recipient_id=current_user.id).order_by(desc(Message.id)).all()
    return render_template('message/receive_message.html',messages=messages)

#发送消息窗口
@message.route('/send/<recipe_id>', methods=['GET', 'POST'])
@login_required
def send_message(recipe_id):
    user = User.query.filter_by(id=recipe_id).first()
    if request.method=='POST':
        
        message_body=request.form.get("message_body")
        msg= Message(author=current_user, recipient=user, body=message_body)
        flash('发送成功！')
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('message.send_message',recipe_id=recipe_id))    
    return render_template('message/send_message.html',recipe_id=recipe_id,user=user)



