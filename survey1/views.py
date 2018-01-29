#coding:utf-8
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Questionnaire, Answer
from login.models import UserProfile
from django.core.urlresolvers import reverse
from django.db import connection, IntegrityError
import MySQLdb

# Create your views here.

def index(request):
    return HttpResponse(u"调查问卷第一版")

pwd = "password"
# def myLogin(request):
#     warnings = []
#     questionnaires = Questionnaire.objects.filter(counting__lt=3)
#     if request.method == 'POST':
#         tmpAlipay = request.POST.get("alipayID")
#         tmpName = request.POST.get("name")
#         qID = request.POST.get("questionnaireID", default="")
#         if not tmpAlipay:
#             warnings.append("Please input your alipayID.\n")
#         if not tmpName:
#             warnings.append("Please input your name.\n")
#         if not qID:
#             warnings.append("Please select a questionnaire ID.\n")
#
#
#             # profile = UserProfile.objects.get(alipayID=tmpAlipay)
#         tmpUser = auth.authenticate(username=tmpAlipay, password=pwd)
#         if tmpUser:
#             auth.login(request, tmpUser)
#         else:
#             localUser = User.objects.create(username=tmpAlipay, password=pwd)
#             auth.login(request, localUser)
#
#         if not warnings:
#             return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))
#
#     return render(request, 'survey1/login.html', {'qList': questionnaires, 'warnings': warnings})

def myLogin(request):
    warnings = []
    questionnaires = Questionnaire.objects.filter(counting__lt=3).order_by('counting')
    # questionnaires = getQuestionnaires(request)
    if request.method == 'POST':
        tmpAlipay = request.POST.get("alipayID")
        tmpName = request.POST.get("name")
        qID = request.POST.get("questionnaireID", default="")

        """
        Handle the incomplete informations first!
        Pay attention its execution sequence
        """
        if not tmpAlipay:
            warnings.append("Please input your alipayID.\n")
        if not tmpName:
            warnings.append("Please input your name.\n")
        if not qID:
            warnings.append("Please select a questionnaire ID.\n")
        if warnings:
            return render(request, 'survey1/login.html',
                          {'qList': questionnaires, 'warnings': warnings,
                           'alipay': tmpAlipay, 'name': tmpName})


        # #can work but can't perfectly solve the problem
        # tmpUser = auth.authenticate(username=tmpAlipay, password=pwd)
        # if tmpUser:
        #     auth.login(request, tmpUser)
        # else:
        #     localUser = User.objects.get(username=tmpAlipay)
        #     auth.login(request, localUser)
        #     try:
        #         profile = UserProfile.objects.get(user_id=localUser.id)
        #         if profile.userName != tmpName:
        #             warnings.append("姓名与支付宝帐号不相符。");
        #     except UserProfile.DoesNotExist:
        #         profile = UserProfile.objects.create(user_id=localUser.id, alipayID=tmpAlipay, userName=tmpName)
        #         profile.save()
        #     warnings.append("The user can't be authenticated.")

        # try:
        #     profile = UserProfile.objects.get(alipayID=tmpAlipay)
        #     if profile.userName != tmpName:
        #         warnings.append("姓名与支付宝帐号不相符。");
        #     else:
        #         tmpUser = auth.authenticate(username=tmpAlipay, password=pwd)
        #         if tmpUser:
        #             auth.login(request, tmpUser)
        # except UserProfile.DoesNotExist:
        #     localUser = User.objects.create(username=tmpAlipay, password=pwd)
        #     auth.login(request, localUser)

        try:
            localUser = User.objects.get(username=tmpAlipay)
            localProfile = UserProfile.objects.get(user_id=localUser.id)
            if localProfile.userName == tmpName:
                authUser = auth.authenticate(username=tmpAlipay, password=pwd)
                if authUser:
                    auth.login(request, authUser)
                else:
                    warnings.append("Invalid login.")
            else:
                warnings.append("The name doesn't match the alipayAccount.")

        except User.DoesNotExist:
            newUser = User.objects.create_user(username=tmpAlipay, password=pwd)
            localProfile = UserProfile.objects.create(user_id=newUser.id, alipayID=tmpAlipay, userName=tmpName)
            authUser = auth.authenticate(username=tmpAlipay, password=pwd)
            if authUser:
                auth.login(request, authUser)
            else:
                warnings.append("Successfully register an account but it is an invalid login.")

        if not warnings:
            return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))

    return render(request, 'survey1/login.html', {'qList': questionnaires, 'warnings': warnings})



@login_required
def questionaire(request, page):
    tmpProfile = UserProfile.objects.get(user_id=request.user.id)
    if tmpProfile.isDone(page):
        return HttpResponseRedirect(reverse('survey1:thanks', args=(page, 0)))

    questionaire1 = Questionnaire.objects.get(qpage=int(page))
    if questionaire1.counting < 3:
        questions = Question.objects.filter(question_page=int(page))
        qlen = len(questions)
        for i in xrange(0, qlen):
            questions[i].setAllChoices()

        if request.method == 'POST':
            for question in questions:
                symList = request.POST.getlist('symptom_%d' % question.id)
                disList = request.POST.getlist('disease_%d' % question.id)
                neither = request.POST.get('neither_%d' % question.id, False)
                try:
                    a = Answer.objects.get(id=question.id)
                    if neither:
                        symStr = ""
                        disStr = ""
                    else:
                        symStr = ";".join(item1 for item1 in symList)
                        disStr = ";".join(item2 for item2 in disList)
                    if a.symptoms and symStr:
                        a.symptoms = "%s%s%s" % (a.symptoms, ";", symStr)
                    elif not a.symptoms:
                        a.symptoms = symStr
                    if a.diseases and disStr:
                        a.diseases = "%s%s%s" % (a.diseases, ";", disStr)
                    elif not a.diseases:
                        a.diseases = disStr
                except Answer.DoesNotExist:
                    a = Answer.objects.create(id = question.id, question_text = question.question_text)
                    if neither:
                        a.symptoms = ""
                        a.diseases = ""
                    else:
                        a.symptoms = ";".join(item1 for item1 in symList)
                        a.diseases = ";".join(item2 for item2 in disList)

                a.save()

            questionaire1.counting += 1
            questionaire1.save()

            if not tmpProfile.isDone(page):
                if tmpProfile.qIDs != "":
                    tmpProfile.qIDs = "%s%s" % (tmpProfile.qIDs, ";")
                tmpProfile.counting += 1
                tmpProfile.qIDs = "%s%s" % (tmpProfile.qIDs, page)
            tmpProfile.save()

            # for i in xrange(0, qlen):
            #     questions[i].question_page_id = questionaire1
            #     questions[i].save()

            return HttpResponseRedirect(reverse('survey1:thanks', args=(page, '1')))
    else:
        questions = []
        return HttpResponseRedirect(reverse('survey1:thanks', args=(page, '2')))

    return render(request, 'survey1/tryvote.html', {"questions": questions, "qlen": json.dumps(len(questions))})
    # return render(request, 'survey1/toBeFinish.html', {"questions": questions})

@login_required
def thanks(request, page, type):
    # questionnaires = Questionnaire.objects.filter(counting__lt=3).order_by('counting')
    # The user has finished the questionnaire
    questionnaires = getQuestionnaires(request)
    if type == "0":
        msg = "You have finished the questionnaire NO.%s before,\n" \
              "please choose another questionnaire." % page
    elif type == "1":
        msg = "Thanks for your support and cooperation."
    else:
        msg = "The questionnaire has been finished. Thanks for your support."

    if request.method == 'POST':
        if request.POST.has_key('continue'):
            qID = request.POST.get("questionnaireID", default="")
            return HttpResponseRedirect(reverse('survey1:questionaire', args=(qID,)))

        if request.POST.has_key('logout'):
            auth.logout(request)
            return HttpResponseRedirect(reverse(myLogin))
    return render(request, 'survey1/thankyou.html', {"msg": msg, 'qList': questionnaires})



# def tryvote(request, question_id):
#     questions = Question.objects.filter(id = int(question_id))
#     qlen = len(questions)
#     for i in xrange(0, qlen):
#         questions[i].setAllChoices()
#
#     return render(request, 'survey1/tryvote.html', {"questions": questions})

def getQuestionnaires(request):
    questionnaires = Questionnaire.objects.filter(counting__lt=3)
    tmpProfile = UserProfile.objects.get(user_id=request.user.id)
    qList = []
    qLen = len(questionnaires)
    print qLen
    for i in xrange(qLen):
        if str(questionnaires[i].qpage) in tmpProfile.qIDs:
            # questionnaires[i].delete()
            print "delete %d \n" % questionnaires[i].qpage
            continue
        qList.append(questionnaires[i])

    print len(qList)
    return qList
