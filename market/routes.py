from market import app
from flask import render_template , redirect , url_for , flash , request 
from market.models import Item , User
from market.forms import RegisterForm , LoginForm ,PurchassForm  , SellForm
from market import db
from flask_login import login_user  , logout_user , login_required , current_user
@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/market' ,methods = ['GET' , 'POST'])
@login_required
def market_page():
    purchass = PurchassForm()
    sell = SellForm()
    if purchass.validate_on_submit() :
        if request.method == 'POST' :
            purchassed_item = request.form.get('purchass') 
            p_item_pur = Item.query.filter_by(name = purchassed_item ).first()
            if p_item_pur : 
                if current_user.budget >= p_item_pur.price  :    
                    p_item_pur.owner = current_user.id
                    current_user.budget -= p_item_pur.price 
                    db.session.commit()
                    flash(f'congratulation you buy {p_item_pur.name}' , category="success")    
                else :         
                    flash(f"you can't buy {p_item_pur.name}" , category="danger")
                return redirect(url_for('market_page'))
    if sell.validate_on_submit()  : 
        if request.method == "POST" : 
            selled_item = request.form.get('sell_item')
            p_item_sell = Item.query.filter_by(name = selled_item  ).first()
            current_user.budget += p_item_sell.price 
            p_item_sell.owner = None
            db.session.commit()
            flash(f'congratulation you sell {p_item_sell.name}' , category="success")
        return redirect(url_for('market_page'))     
    if request.method == 'GET'  : 
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items , PurchassForm =purchass , owned_items = owned_items , sell=sell)

@app.route('/register', methods = ['GET' , 'POST']) 
def register_page() : 
    form = RegisterForm() 
    if form.validate_on_submit() : 
        user_to_create = User(username=form.username.data , email_address = form.email_address.data , password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('user created with success' , category="success")
        return redirect(url_for('market_page'))
    if form.errors != {} : 
        for err_msg in form.errors.values() : 
            flash(f'there was an error when creating a user {err_msg[0]}', category='danger')
    return render_template('register.html' , form=form)

@app.route('/login' , methods = ['GET' , 'POST'])

def login_page() : 
    form = LoginForm()
    if form.validate_on_submit() : 
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) : 
            login_user(user)
            flash(f"Success ! , you login as : {user.username}", category="success")
            return redirect(url_for('market_page'))
        else :
            flash('username and password are not mathc ! Please try again' , category='danger')
    return render_template('login.html' , form = form)

@app.route('/logout')
def logout() : 
    logout_user()
    flash('you have been logged out!' , category='info')
    return redirect(url_for("home_page"))