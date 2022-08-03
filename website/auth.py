from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .views import getNetBenefit, getTaxAmount, getTotalRevenue

auth = Blueprint("auth", __name__)


def getTransactionsMonth(user, month):
    return [
        transaction for transaction in user.transactions if transaction.month == month
    ]


def getActiveMonths(user):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    while not getTransactionsMonth(user=user, month=months[-1]) and len(months) > 1:
        months.pop(-1)
    return months


def getNetBenefits(user):
    netBenefits = []
    for month in getActiveMonths(user):
        netBenefits.append(getNetBenefit(user=user, month=month))
    return netBenefits


def getTaxAmounts(user):
    taxAmounts = []
    for month in getActiveMonths(user):
        taxAmounts.append(getTaxAmount(user=user, month=month))
    return taxAmounts


def getTotalRevenues(user):
    TotalRevenues = []
    for month in getActiveMonths(user):
        TotalRevenues.append(getTotalRevenue(user=user, month=month))
    return TotalRevenues


def getData(ta, nb, tr, months):
    data = []  # [[month, ta, nb , tr], [month2, ta2, nb2, tr2]]
    for i in range(len(months)):
        data.append([months[i], ta[i], nb[i], tr[i]])

    return data


@auth.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        month = request.form.get("month")
        return redirect(url_for("views.month", month=month))
    return render_template(
        "home.html",
        user=current_user,
        data=getData(
            ta=getTaxAmounts(current_user),
            nb=getNetBenefits(current_user),
            tr=getTotalRevenues(current_user),
            months=getActiveMonths(current_user),
        ),
    )


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("You are now logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("auth.home"))
            else:
                flash("Password is not correct, try again.", category="error")
        else:
            flash("Username has not been found, check the spelling.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", category="error")
        elif len(username) < 4:
            flash("Username must have at least 4 characters.", category="error")
        elif len(password) < 7:
            flash("Password must have at least 8 characters.", category="error")
        elif password != password2:
            flash("Passwords do not match.", category="error")
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account successfully created.", category="success")
            return redirect(url_for("auth.home"))

    return render_template("sign_up.html", user=current_user)
