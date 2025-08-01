from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Expense
from collections import defaultdict
from datetime import datetime
import json

main = Blueprint('main', __name__)

@main.route('/')# login req
@login_required
def index(): 
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # ----- Filtering -----
    desc = request.args.get('desc', '').lower()
    category = request.args.get('category', '').lower()
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    filtered_expenses = []
    for e in expenses:
        if desc and desc not in e.description.lower():
            continue
        if category and category not in e.category.lower():
            continue
        try:
            if from_date and datetime.strptime(e.date, '%Y-%m-%d') < datetime.strptime(from_date, '%Y-%m-%d'):
                continue
            if to_date and datetime.strptime(e.date, '%Y-%m-%d') > datetime.strptime(to_date, '%Y-%m-%d'):
                continue
        except Exception:
            continue
        filtered_expenses.append(e)

    expenses = filtered_expenses
    total = sum(e.amount for e in expenses)

    # ----- Category Breakdown (Pie Chart) -----
    category_data = defaultdict(float)
    for e in expenses:
        category_data[e.category] += e.amount
    category_labels = list(category_data.keys())
    category_totals = list(category_data.values())

    # ----- Monthly Breakdown (Bar Chart) -----
    monthly_data = defaultdict(float)
    for e in expenses:
        try:
            dt = datetime.strptime(e.date, '%Y-%m-%d')
            key = dt.strftime('%Y-%m')  # "2025-07"
            monthly_data[key] += e.amount
        except Exception:
            continue
    month_labels = list(monthly_data.keys())
    month_totals = list(monthly_data.values())

    # ----- Insights -----
    top_category = max(category_data, key=category_data.get) if category_data else "None"
    this_month = datetime.now().strftime('%Y-%m')
    total_this_month = monthly_data.get(this_month, 0.0)

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        category_labels=json.dumps(category_labels),
        category_totals=json.dumps(category_totals),
        month_labels=json.dumps(month_labels),
        month_totals=json.dumps(month_totals),
        top_category=top_category,
        total_this_month=total_this_month
    )

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        try:
            date = request.form['date']
            description = request.form['description']
            category = request.form['category']
            amount = float(request.form['amount'])
            expense = Expense(date=date, description=description, category=category, amount=amount, user_id=current_user.id)
            db.session.add(expense)
            db.session.commit()
        except Exception as e:
            print("Add Expense Error:", e)
        return redirect(url_for('main.index'))
    return render_template('add_expense.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        try:
            expense.date = request.form['date']
            expense.description = request.form['description']
            expense.category = request.form['category']
            expense.amount = float(request.form['amount'])
            db.session.commit()
        except Exception as e:
            print("Edit Expense Error:", e)
        return redirect(url_for('main.index'))

    return render_template('edit_expense.html', expense=expense)

@main.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        return "Unauthorized", 403

    try:
        db.session.delete(expense)
        db.session.commit()
    except Exception as e:
        print("Delete Expense Error:", e)

    return redirect(url_for('main.index'))
