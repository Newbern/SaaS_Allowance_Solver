from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import *
from main.forms import *
from decimal import Decimal


# Homepage
def home(request):
    allowance = Allowance.objects.filter(user=request.user).first()
    expense = Expense.objects.filter(allowance=allowance).first()

    #expense.add_spending("Extra", "Walmart", 21.86)

    for item in expense.spending:
        print(expense.spending[item]['item'])


    return render(request, 'main/Home.html', {'user':request.user})


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

            # Going Through Each Expanse
            for exp in expense.spending:
                expense.spending[exp]['set'] = expense.spending[exp]['limit'] - sum([Decimal(amount) for amount in expense.spending[exp]['amount']])

                # Setting Allowance
                item.set_allowance -= sum([Decimal(amount) for amount in expense.spending[exp]['amount']])

            # Saving Allowance & Expense
            item.save()
            expense.save()


# Getting Chat Data
def chart_data(request):

    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()

        names_lst = []
        values_lst = []
        limits_lst = []
        for i in Expense.objects.filter(allowance=allowance).order_by('expense'):
            names_lst.append(i.expense)
            values_lst.append(i.set)
            limits_lst.append((i.limit - i.set))
        data = {
            'labels': names_lst,
            'saved': values_lst,
            'spent': limits_lst,
            'color': 'rgb(0 150 255)',
            'allowance': int(allowance.default_allowance),
            'schedule': allowance.schedules
        }

        return JsonResponse(data)

# Getting Transactions Data


# Showing all Allowances
def show(request):
    update(request)
    if request.method == "GET":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Getting Expense
        expense = Expense.objects.filter(allowance=allowance).first()

        expense_lst = []
        for exp in expense.spending:
            expense_lst.append([expense.spending[exp], expense.spending[exp]['description']])


        # Loading Page
        return render(request, 'main/Show_Allowance.html', {"allowance": allowance, "expense": expense})

    elif request.method == "POST":
        # Getting Allowance
        allowance = Allowance.objects.filter(user=request.user).last()

        # Getting Expense
        expense_name = request.POST.get('expense_name')
        expense = Expense.objects.get(allowance=allowance, expense=expense_name)

        # Getting Values
        expense_description = request.POST.get('expense_description')
        expense_amount = request.POST.get('expense_amount')
        # Adding Spending Cost
        #expense.add_entry(expense_description, expense_amount)

        return redirect(show)


# Create New Allowance
def create(request):
    if request.method == "GET":
        allowance = Allowance.objects.filter(user=request.user).last()
        # Collecting Forms
        # Getting Previous Allowance Expenses
        if allowance:
            form = AllowanceForm(instance=allowance)
            form2 = [AllowanceExpenseForm()]

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


# Settings
def settings(request):
    return render(request, 'main/Settings.html', {})







