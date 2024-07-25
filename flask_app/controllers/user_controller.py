from flask_app import app, bcrypt
from flask import render_template, redirect, session, request
from flask_app.models import user_model


# ********* CREATE *********
@app.route('/users/new')
def user_new():
    return render_template('/user_new.html')

@app.route('/users/create', methods=['POST'])
def user_create():
    data = {
        **request.form,
    }
    if not user_model.User.validator(**data):
        return redirect('/')
    
    hash_password = bcrypt.generate_password_hash(data['password'])
    data['password'] = hash_password

    uuid = user_model.User.create_one(**data)
    session['uuid'] = uuid
    
    return redirect('/')

# ********* READ *********
@app.route('/users')
def user_show():
    context = {
    'all_users' :  user_model.User.get_all()
    }
    return render_template('/pages/users/user_edit.html', **context)
    
@app.route('/users/<int:id>/edit')
def user_edit(id):
    context = {
        'user' :  user_model.User.get(id=id)
    }
    return render_template('/pages/users/user_edit.html', **context)


# ********* UPDATE *********
@app.route('/users/<int:id>/update', methods=['POST'])
def user_update(id):
    data = {
        **request.form,
    }

    if not user_model.User.validator(**data):
        return redirect(f'/users/{id}/edit')

    user_model.User.update_one({'id':id}, **data)
    return redirect(f'/users/{id}/edit')

# ********* DELETE *********
@app.route('/users/<int:id>/delete')
def user_delete(id):
    user_model.User.delete_one(id=id)
    return redirect('/user')