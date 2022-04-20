from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_recipe



# ******************** DISPLAY ROUTE **********************

@app.route('/recipes/new')
def recipes_new():
    if 'uuid' in session:
        create_one_recipe = model_recipe.Recipe.get_all_recipes({'id':session['uuid']})
        all_users_from_db = model_recipe.Recipe.get_all_recipes({'id':session['uuid']})
    if not 'uuid' in session:
        return render_template("recipe_new.html")
    return render_template("recipe_new.html", user=all_users_from_db, recipe=create_one_recipe)


@app.route('/recipes/<int:id>')
def recipe_instructions(id):
    if not 'uuid' in session:
        return redirect('/')
    data = {
        "id": id
    }
    user_from_db = model_user.User.get_one_user({'id':session['uuid']})
    get_one_recipe=model_recipe.Recipe.get_one_recipe(data)
    return render_template("recipe_instructions.html", recipe=get_one_recipe, user=user_from_db)


@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    if not 'uuid' in session:
        return redirect('recipes/create')
    data = {
        "id": id
    }
    user_from_db = model_user.User.get_one_user({'id':session['uuid']})
    edit_one_recipe = model_recipe.Recipe.get_one_recipe(data)
    return render_template("recipe_edit.html", recipe=edit_one_recipe,  user=user_from_db)


@app.route('/recipes/delete/<int:id>')
def recipe_delete(id):
    data = {
        "id": id
    }
    model_recipe.Recipe.delete_recipe(data)
    return redirect("/dashboard")



# ******************** ACTION ROUTE **********************

@app.route('/recipes/create', methods=['post'])
def recipes_create(): 
    is_valid = model_recipe.Recipe.validator(request.form)
    if not is_valid:
        return redirect('/recipes/new')
    user_data = {
        "user_id": session["uuid"],
        "name": request.form["name"],   
        "description": request.form["description"],     
        "instruction": request.form["instruction"],
        "date_made_on": request.form["date_made_on"],
        "time": request.form["time"]
    }
    model_recipe.Recipe.create_one_recipe(user_data)
    return redirect("/dashboard")


@app.route('/recipes/update/<int:id>', methods=['post'])
def recipe_update(id):
    is_valid = model_recipe.Recipe.validator(request.form)
    if not is_valid:
        return redirect(f'/recipes/edit/{id}')
    data = {
        **request.form,
        "id": id,
        "user_id":session['uuid']
    }
    model_recipe.Recipe.update_one_recipe(data)
    return redirect("/dashboard")


# ************************* Keep This At The Bottom ************************

if __name__ == "__main__":
    app.run(debug=True)

# **************************** END

