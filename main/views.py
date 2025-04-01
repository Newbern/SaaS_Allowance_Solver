from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import *
from main.forms import *
from decimal import Decimal


# Homepage
def home(request):
    return render(request, 'main/Home.html', {'user': request.user})


# Updating Data
def update(request):
    # Getting Allowance
    allowance = Allowance.objects.all()

    # Resetting Allowance
    for item in allowance:
        item.set_allowance = item.default_allowance
        item.save()

    # Resetting Expenses
    for item in allowance:
        for expense in Expense.objects.filter(allowance=item):
            # Setting Expense
            #expense.set = expense.limit - sum([Decimal(item[1]) for item in expense.spending])
            #expense.save()

            # Going Through Each Expense
            for exp in expense.spending:
                # Every Expense amount
                spending = sum([Decimal(expense.spending[exp]["item"][name]["amount"]) for name in expense.spending[exp]["item"]])

                # Setting Current Expense
                expense.spending[exp]['set'] = str(Decimal(expense.spending[exp]['limit']) - spending)

                # Setting Allowance
                item.set_allowance -= spending

            # Saving Allowance & Expense
            item.save()
            expense.save()


# Getting Chat Data
def chart_data(request):

    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()
        expense = Expense.objects.filter(allowance=allowance).first()

        names_lst = []
        values_lst = []
        spent_lst = []
        for exp in expense.spending:
            spending = expense.spending[exp]
            names_lst.append(exp)
            values_lst.append(Decimal(spending["set"]))
            spent_lst.append(Decimal(spending["limit"]) - Decimal(spending["set"]))


        data = {
            'labels': names_lst,
            'saved': values_lst,
            'spent': spent_lst,
            'color': 'rgb(0 150 255)',
            'allowance': int(allowance.default_allowance),
            'schedule': allowance.schedules
        }

        return JsonResponse(data)


# Showing all Allowances
def show(request):
    # Update Allowance & Expenses
    update(request)

    if request.method == "GET":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Getting Expense
        expense = Expense.objects.filter(allowance=allowance).first()

        expense_lst = []
        for exp in expense.spending:
            items_lst = []
            for name in expense.spending[exp]["item"]:
                spending = expense.spending[exp]["item"][name]
                items_lst.append([expense.spending[exp], spending, spending["amount"]])
            expense_lst.append(items_lst)



        # Loading Page
        return render(request, 'main/Show_Allowance.html', {"allowance": allowance, "expense": expense})

    elif request.method == "POST":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()
        # Getting Expense
        expense = Expense.objects.filter(allowance=allowance).first()

        # Getting Values
        expense_name = request.POST.get('expense_name')
        expense_description = request.POST.get('expense_description')
        expense_amount = request.POST.get('expense_amount')

        # Adding Spending Cost
        expense.add_spending(expense_name, expense_description, expense_amount)

        return redirect(show)


# Create New Allowance
def create(request):
    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()
        expense = Expense.objects.filter(allowance=allowance).first()
        # Collecting Forms
        # Getting Previous Allowance Expenses
        if allowance:
            form = AllowanceForm(instance=allowance)
            form2 = [(AllowanceExpenseForm(data={'name': name, 'limit': data['limit']})) for name, data in expense.spending.items()]

        # Creating New Allowance Forms
        else:
            form = AllowanceForm()
            form2 = [AllowanceExpenseForm()]

        return render(request, 'main/Create_Allowance.html', {"form": form, "form2": form2})

    elif request.method == "POST":
        # Getting Values
        allowance = request.POST.get("default_allowance")
        schedules = request.POST.get('schedules')
        expense = request.POST.getlist('expense')
        expense_limit = request.POST.getlist('limit')

        # Creating Allowance & Saving
        new_allowance = Allowance(user=request.user, schedules=schedules, default_allowance=allowance)
        new_allowance.save()

        # Creating Expenses & Saving
        expense_obj = Expense.objects.create(allowance=new_allowance)
        for expense, limit in zip(expense, expense_limit):
            expense_obj.add_expense(expense, limit)

        expense_obj.save()


        return redirect(home)


def history(request):
    if request.method == "GET":
        # Getting Allowance
        allowance = Allowance.objects.all()
        expense = Expense.objects.all()

        # Setting up Percentages Allowance
        limit = saved = spent = 0
        for item in allowance:
            limit += item.default_allowance
            saved += item.set_allowance
            spent += (item.default_allowance - item.set_allowance)

        # Rounding Percentages
        saved = f"Saved: {round(saved / limit * 100, 2)}% (${saved})"
        spent = f"Spent: {round(spent / limit * 100, 2)}% (${spent})"


        # Getting Every Value in Expense

        for item in allowance:
            spending = Expense.objects.filter(allowance=item).first().spending
            for exp in spending:
                print(spending[exp]["item"])



        return render(request, 'main/History.html', {"saved": saved, "spent": spent})

def chart_history_data(request):
    if request.method == "GET":
        allowance = reversed(Allowance.objects.all())

        names_lst = []
        values_lst = []
        spent_lst = []
        for item in allowance:
            names_lst.append(item.date)
            values_lst.append(item.set_allowance)
            spent_lst.append(item.default_allowance - item.set_allowance)


        data = {
            'labels': names_lst,
            'saved': values_lst,
            'spent': spent_lst,
            'color': 'rgb(0 150 255)'
        }

        return JsonResponse(data)



# Settings
def settings(request):
    return render(request, 'main/Settings.html', {})







