from flask_app import app, bcrypt
from flask import render_template, request, redirect, session


from flask_app.models import model_user, model_recipe


@app.route('/recipes/new')
def recipes_new():
    return render_template("recipe_new.html")


@app.route('/recipes/create', methods=['post'])
def recipes_create(): 
    # input new recipe to db and have it redirect to show on dashboard
    user_data = {
        "user_id": session["uuid"],
        "name": request.form["name"],   
        "description": request.form["description"],     
        "instruction": request.form["instruction"],
        "time": request.form["time"]
    }
    model_recipe.Recipe.create(user_data)
    return redirect("/dashboard")

@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    data = {
        "id": id
    }
    edit_one_recipe = model_recipe.Recipe.get_one_recipe(data)
    return render_template("recipe_edit.html", user=edit_one_recipe)

@app.route('/recipes/update/<int:id>')
def recipe_update(id):
    data = {
        "id": id
    }
    model_recipe.Recipe.update_one_recipe(data)
    return redirect("/dashboard")

@app.route('/recipes/delete/<int:id>')
def recipe_delete(id):
    data = {
        "id": id
    }
    model_recipe.Recipe.delete_recipe(data)
    return redirect("/dashboard")

@app.route('/recipes/<int:id>')
def recipe_details(id):
    context = {
        "recipe": model_recipe.Recipe.get_one_recipe({'id': id})
    }
    return render_template("recipe_details.html", **context)



# @app.route('/create', methods=['POST'])
# def add_recipe_to_user():
#     user_data = {
#         "user_id": request.form["user_name_id"],
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email": request.form["email"],
#         "password": request.form["password"]
#     }
#     model_user.User.save(user_data)
#     return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)

# ****************************