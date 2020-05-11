from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth import authenticate, login
from .models import *
from django.forms.utils import ErrorList
from .forms import LoginForm, SignUpForm
from datetime import datetime
import razorpay
import requests

now = datetime.now()

@login_required(login_url="/login/")
def index(request):
    try:
        org = Organization.objects.get(user=request.user.id)
        proj = Project.objects.filter(org_id=org.id)
        proj_id_list = []
        for x in proj:
            proj_id_list.append(x.id)
        context = {
            "org": Organization.objects.get(user=request.user.id),
            "subscriptions": Subscription.objects.filter(project__in=proj_id_list),
        }
        return render(request, "index.html", context)
    except:
        print("Organization does not exist")
        return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

def loginView(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

def addOrgView(request):
    if request.method == "POST":
        user_loggedV = request.user
        org_nameV = request.POST.get("org_name")
        type_idV = request.POST.get("type_id")
        c_add_1V = request.POST.get("c_add_1")
        c_add_2V = request.POST.get("c_add_2")
        c_countryV = request.POST.get("c_country")
        c_stateV = request.POST.get("c_state")
        c_districtV = request.POST.get("c_district")
        c_phoneV = request.POST.get("c_phone")
        c_emailV = request.POST.get("c_email")
        c_statusV = request.POST.get("c_status")
        c_gstV = request.POST.get("c_gst")
        b_add_1V = request.POST.get("b_add_1")
        b_add_2V = request.POST.get("b_add_2")
        b_countryV = request.POST.get("b_country")
        b_stateV = request.POST.get("b_state")
        b_districtV = request.POST.get("b_district")
        b_phoneV = request.POST.get("b_phone")
        b_emailV = request.POST.get("b_email")
        b_statusV = request.POST.get("b_status")
        b_gstV = request.POST.get("b_gst")

        org = Organization(user = user_loggedV, name = org_nameV, type_id = type_idV, comm_address1 = c_add_1V,
            comm_address2 = c_add_2V, comm_country = c_countryV, comm_state = c_stateV, comm_district = c_districtV,
            comm_phone = c_phoneV, comm_email = c_emailV, comm_status = c_statusV, comm_gstin = c_gstV,
            bill_address1 = b_add_1V, bill_address2 = b_add_2V, bill_country = b_countryV,bill_state = b_stateV,
            bill_district = b_districtV, bill_phone = b_phoneV, bill_email = b_emailV, bill_status = b_statusV,
            bill_gstin = b_gstV)
        org.save()

        return redirect('addcard')
    return render(request, "project/add_organization.html")

def addCardView(request):
    if request.method == "POST":
        org_id1 = Organization.objects.filter(user = request.user)
        org_idV = org_id1.last()
        card_numberV = request.POST.get("card_number")
        name_on_cardV = request.POST.get("name_on_card")
        expiry_dateV = request.POST.get("expiry_date")
        cvvV = request.POST.get("cvv")

        card = Card(org_id = org_idV, card_number = card_numberV, name_on_card = name_on_cardV, expiry_date = expiry_dateV, cvv = cvvV)
        card.save()

        return redirect('addproject')
    return render(request, "project/add_card.html")

def addProjectView(request):
    if request.method == "POST":
        org_id1 = Organization.objects.filter(user = request.user)
        org_idV = org_id1.last()
        titleV = request.POST.get("project_title")
        summaryV = request.POST.get("project_summary")
        durationV = request.POST.get("duartion")
        start_dateV = request.POST.get("p_start_date")
        end_dateV = request.POST.get("p_end_date")
        statusV = request.POST.get("status")

        proj = Project(org_id = org_idV, title = titleV, summary = summaryV, duration = durationV,
                        start_date = start_dateV, end_date = end_dateV, status = statusV)
        proj.save()

        return redirect('selectplan')
    return render(request, "project/add_project.html")

def selectPlanView(request):
    org = Organization.objects.get(user=request.user.id)
    proj = Project.objects.filter(org_id=org.id)
    context = {
        "plans": Plan.objects.all(),
        "projects":proj,
    }
    if request.method == "POST":
        plan1 = request.POST.get("plan")
        project1 = request.POST.get("project")
        renew_time = request.POST.get("renewal_date_time")
        plan_qset = Plan.objects.get(id=plan1)
        proj_qset = Project.objects.get(id=project1)

        #to generate razorpay id for each purchase
        client=razorpay.Client(auth=("rzp_test_2tx97L0V09FUM6","QOWTRaArqW2Gj8O6rUxtEVwR"))
        Data = {'amount':str(int(plan_qset.price)*100),"currency":'INR',"receipt":'order_rcptid_11',"payment_capture":1}
        val = client.order.create(data=Data)
        order_id = val['id']
        print("order id ======= ",order_id)
        

        subs = Subscription(plan = plan_qset, project = proj_qset, subscription_date_time = now.strftime("%d/%m/%Y %H:%M:%S"),
        renewal_date_time = renew_time, auto_renewal = True, status = "unpaid", razorpay_order_id = order_id)
        subs.save()

        return redirect('confirmation')
    return render(request, "project/select_plan.html", context)

def confirmationView(request):
    context = {
        "sub": Subscription.objects.last()
    }
    return render(request, "project/confirmation.html",context)

def postMEdetails(request, pk):
    project_obj = Project.objects.get(id=pk)

    API_ENDPOINT = "http://localhost:9000/register_user"

    data = {'username': request.user.username,
            'email':request.user.email,
            'title':project_obj.title,
            'summary': project_obj.summary,
            'start': project_obj.start_date,
            'end': project_obj.end_date,
            'status': project_obj.status            
            }

    r = requests.post(url = API_ENDPOINT, data = data)

    return redirect("home")
