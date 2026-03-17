from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db, bcrypt
from models import User, Profile
from forms import RegistrationForm, LoginForm, ProfileSetupForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not user.is_profile_setup:
                return redirect(url_for('auth.profile_setup'))
            return redirect(next_page) if next_page else redirect(url_for('routes.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile_setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    if current_user.is_profile_setup:
        return redirect(url_for('routes.dashboard'))
    
    form = ProfileSetupForm()
    if form.validate_on_submit():
        profile = Profile(
            full_name=form.full_name.data,
            college=form.college.data,
            branch=form.branch.data,
            year_of_study=form.year_of_study.data,
            target_role=form.target_role.data,
            github_link=form.github_link.data,
            linkedin_link=form.linkedin_link.data,
            user=current_user
        )
        current_user.is_profile_setup = True
        db.session.add(profile)
        db.session.commit()
        flash('Profile setup successful! Welcome to your dashboard.', 'success')
        return redirect(url_for('routes.dashboard'))
    
    return render_template('profile_setup.html', title='Profile Setup', form=form)
