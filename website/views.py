from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Transaction
from . import db
import json
import matplotlib.pyplot as plt

views = Blueprint("views", __name__)


def getNetBenefit(user, month):
    netBenefit = 0
    for transaction in user.transactions:
        if transaction.month == month:
            netBenefit += (1 - 2 * transaction.isExpense) * transaction.amount
    return netBenefit


def getFields(transaction):
    return transaction.split(";")


def isFormatValid(transaction):
    fields = getFields(transaction)
    if (
        len(fields) != 4
        or len(transaction) < 1
        or int(fields[2]) < 1
        or int(fields[2]) > 31
        or int(fields[0]) not in (0, 1)
    ):
        return False

    for field in fields:
        for character in field:
            isAlpha = character.isalpha()
            isNum = character.isnumeric()
            if (
                ((not isNum) and (not isAlpha))
                and ord(character) != 46
                and ord(character) != 32
            ):
                return False
    return True


def getDay(transaction):
    fields = getFields(transaction)
    return str(fields[2])


def getAmount(transaction):
    fields = getFields(transaction)
    return round(float(fields[1]), 2)


def getIsExpense(transaction):
    fields = getFields(transaction)
    return bool(int(fields[0]))


def getConcept(transaction):
    return str(getFields(transaction)[3])


def sortTransactions(user, month):
    transactions = [
        transaction for transaction in user.transactions if transaction.month == month
    ]

    return sorted(
        transactions,
        key=lambda transaction: (
            transaction.day,
            (-1) * transaction.amount if transaction.isExpense else transaction.amount,
        ),
        reverse=True,
    )


@views.route("/month/<month>", methods=["GET", "POST"])
@login_required
def month(month):
    if request.method == "POST":
        transaction = request.form.get("transaction")

        if not isFormatValid(transaction):
            flash("Incorrect formatting", category="error")
        else:
            new_transaction = Transaction(
                user_id=current_user.id,
                data=transaction,
                month=month,
                day=getDay(transaction),
                amount=getAmount(transaction),
                isExpense=getIsExpense(transaction),
                concept=getConcept(transaction),
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash("Transaction added successfully!", category="success")

    return render_template(
        "month.html",
        user=current_user,
        month=month,
        netBenefit=getNetBenefit(user=current_user, month=month),
        transactionList=sortTransactions(user=current_user, month=month),
    )


@views.route("/delete-transaction", methods=["POST"])
def delete_transation():
    transaction = json.loads(request.data)
    transactionId = transaction["transactionId"]
    transaction = Transaction.query.get(transactionId)
    if transaction:
        if transaction.user_id == current_user.id:
            db.session.delete(transaction)
            db.session.commit()
            print("Transaction deleted")
    return jsonify({})
