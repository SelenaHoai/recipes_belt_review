from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_recipe


# ******************** DISPLAY ROUTE **********************

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard_for_recipe():
    if 'uuid' in session:
        all_recipes_from_db = model_recipe.Recipe.get_all_recipes({'id':session['uuid']})
        user_from_db = model_user.User.get_one_user({'id':session['uuid']})
        return render_template('dashboard.html', all_recipes=all_recipes_from_db, user=user_from_db)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    return redirect('/')


# ******************** ACTION ROUTE **********************


@app.route('/login', methods=['post'])
def login():
    # validate login
    is_valid = model_user.User.validator_login(request.form)
    if not is_valid:
        return redirect('/')
    return redirect('/dashboard')


@app.route('/register', methods=['post'])
def register():
    # validate user
    is_valid = model_user.User.validator(request.form)
    if not is_valid:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        **request.form,
        'password': pw_hash
    }
    id = model_user.User.register_user(data)
    session['uuid'] = id
    return redirect('/dashboard')



# ************************* Keep This At The Bottom *************************

if __name__ == "__main__":
    app.run(debug=True)

# **************************** END