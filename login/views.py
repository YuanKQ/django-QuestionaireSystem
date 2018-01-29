#coding:utf-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from login.models import UserProfile
from survey1.models import Questionnaire

# Create your views here.

# def myLogin(request):
#     questionnaires = Questionnaire.objects.filter(counting__lt=3)
#
#     if request.method == 'POST':
#         tmpAlipay = request.POST.get("alipayID")
#         tmpName = request.POST.get("name")
#         qID = request.POST.get("questionnaireID")
#
#         try:
#             usr = User.objects.get(alipayID=tmpAlipay)
#             usr.qIDs = "%s%s%s" % (usr.qIDs, ";", qID)
#         except:
#             usr = User.objects.create(alipayID=tmpAlipay, usrName=tmpName, qIDs=qID)
#         usr.save()
#
#         return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))
#
#     return render(request, 'survey1/login.html', {'qList': questionnaires})

pwd = "password"

# def myLogin(request):
#     questionnaires = Questionnaire.objects.filter(counting__lt=3)
#     if request.method == 'POST':
#         tmpAlipay = request.POST.get("alipayID")
#         tmpName = request.POST.get("name")
#         qID = request.POST.get("questionnaireID", default="")
#
#         #register or login
#         try:
#             profile = UserProfile.objects.get(alipayID=tmpAlipay)
#             if not profile.isDone(qID):
#                 if profile.qIDs != "":
#                     profile.qIDs = "%s%s" % (profile.qIDs, ";")
#                 profile.qIDs = "%s%s" % (profile.qIDs, qID)
#                 profile.save()
#                 user = auth.authenticate(username=tmpAlipay, password=pwd)
#                 if user:
#                     auth.login(request, user)
#             else:
#                 warning = u"您已经完成过第%s问卷，请选择其他问卷继续答题。" % qID
#                 return render(request, 'survey1/login.html', {'qList': questionnaires, 'warning': warning})
#
#         except UserProfile.DoesNotExist:
#             newuser = User.objects.create_user(username=tmpAlipay, password=pwd)
#             #extend the info of users
#             profile = UserProfile()
#             profile.alipayID = newuser.username
#             profile.user_id = newuser.id
#             profile.userName = tmpName
#             if profile.qIDs != "":
#                 profile.qIDs = "%s%s" % (profile.qIDs, ";")
#             profile.qIDs = "%s%s" % (profile.qIDs, qID)
#             profile.save()
#
#             newuser1 = auth.authenticate(username=tmpAlipay, password=pwd)
#             if newuser1 is not None:
#                 auth.login(request, newuser1)
#
#         return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))
#
#     return render(request, 'survey1/login.html', {'qList': questionnaires})

def myLogin(request):
    warnings = []
    questionnaires = Questionnaire.objects.filter(counting__lt=3)
    if request.method == 'POST':
        tmpAlipay = request.POST.get("alipayID")
        tmpName = request.POST.get("name")
        qID = request.POST.get("questionnaireID", default="")
        if not tmpAlipay:
            warnings.append("Please input your alipayID.\n")
        if not tmpName:
            warnings.append("Please input your name.\n")
        if not qID:
            warnings.append("Please select a questionnaire ID.\n")

        try:
            profile = UserProfile.objects.get(alipayID=tmpAlipay)
            tmpUser = auth.authenticate(username=tmpAlipay, password=pwd)
            if tmpUser:
                auth.login(request, tmpUser)
            else:
                localUser = User.objects.create(username=tmpAlipay, password=pwd)
                auth.login(request, localUser)
             #if the current user never done this questionnaire before
            # if not profile.isDone(qID):
            #     if profile.qIDs != "":
            #         profile.qIDs = "%s%s" % (profile.qIDs, ";")
            #     profile.qIDs = "%s%s" % (profile.qIDs, qID)
            #     profile.save()
            #
            #     tmpUser = auth.authenticate(username=tmpAlipay, password=pwd)
            #     if tmpUser:
            #         auth.login(request, tmpUser)
            #     else:
            #         localUser = User.objects.create(username=tmpAlipay, password=pwd)
            #         auth.login(request, localUser)
            # else:
            #     warnings.append("You have done the questionnaire NO.%s before. Please choose another questionnaire." % qID)

        except UserProfile.DoesNotExist:
            newUser = User.objects.create(username=tmpAlipay, password=pwd)
            profile = UserProfile.objects.create(user_id=newUser.id, alipayID=tmpAlipay, userName=tmpName, qIDs=qID)
            localUser = auth.authenticate(username=tmpAlipay, password=pwd)
            if localUser:
                auth.login(request, newUser)

        if not warnings:
            return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))

    return render(request, 'survey1/login.html', {'qList': questionnaires, 'warnings': warnings})
