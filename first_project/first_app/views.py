from django.shortcuts import render
from first_app import forms
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.models import User
import pandas as pd
from nsepy import get_history
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'first_app/index.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

@login_required
def optionchain(request):
    if request.method == 'POST':
        script = request.POST.get('url')
        #Base_url = request.POST.get('url')
        #page = requests.get(Base_url)
        #page.status_code
        #page.content
        df = get_history(symbol=script, start=date(2018,5,1), end=date(2018,10,31))




        '''Webscrapping option chain
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())

        table_it = soup.find_all(class_="opttbldata")
        table_cls_1 = soup.find_all(id="octable")


        col_list = []

        # The code given below will pull the headers of the Option Chain table
        for mytable in table_cls_1:
            table_head = mytable.find('thead')

            try:
                rows = table_head.find_all('tr')
                for tr in rows:
                    cols = tr.find_all('th')
                    for th in cols:
                        er = th.text
                        ee = er.encode('utf8')
                        ee = str(ee, 'utf-8')
                        col_list.append(ee)

            except:
                print ("no thead")


        col_list_fnl = [e for e in col_list if e not in ('CALLS','PUTS','Chart','\xc2\xa0','\xa0')]

        table_cls_2 = soup.find(id="octable")
        all_trs = table_cls_2.find_all('tr')
        req_row = table_cls_2.find_all('tr')

        new_table = pd.DataFrame(index=range(0,len(req_row)-3) , columns=col_list_fnl)

        row_marker = 0

        for row_number, tr_nos in enumerate(req_row):

             # This ensures that we use only the rows with values
            if row_number <=1 or row_number == len(req_row)-1:
                continue
            td_columns = tr_nos.find_all('td')

             # This removes the graphs columns
            select_cols = td_columns[1:22]
            cols_horizontal = range(0,len(select_cols))

            for nu, column in enumerate(select_cols):
                utf_string = column.get_text()
                utf_string = utf_string.strip('\n\r\t": ')

                tr = utf_string.encode('utf-8')
                tr = str(tr, 'utf-8')
                tr = tr.replace(',' , '')
                new_table.ix[row_marker,[nu]]= tr

            row_marker += 1
        html = new_table.to_html(classes=["table-bordered", "table-striped", "table-hover"])
        '''
        html = df.to_html(classes=["table-bordered", "table-striped", "table-hover"])
        data={'optionchain':html}
        return render(request,'first_app/optionchain.html',context=data)
    return render(request,'first_app/optionchain.html')

def userLogin(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'first_app/user_login.html', {})

def newUser(request):
    loginform = forms.createNewUser()

    if request.method == 'POST':
        loginform = forms.createNewUser(request.POST)

        if loginform.is_valid():
            loginform.save(commit=True)
            return index(request)

    return render(request,"first_app/register.html",context={'loginform': loginform})
