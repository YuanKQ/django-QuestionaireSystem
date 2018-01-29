#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#if the filed "qIDs" is null, we define it as the label "@"
# class User(models.Model):
#     alipayID = models.CharField(max_length=50, primary_key=True)
#     usrName = models.TextField()
#     qIDs = models.CharField(max_length=100, default="@")
#
#     def __unicode__(self):
#         print u'***支付宝帐号:' % (self.alipayID)
#         print u'***姓名: %s' % self.usrName
#         print u'***已完成问卷有: %s' % self.qID
#         print u'**************************************'
#
#     def setAllQuestionnaire(self):
#         if self.qIDs != "@":
#             self.qIDList = self.qIDs.split(";")
#         else:
#             self.qIDList = []
#
#     def isDone(self, qID):
#         self.setAllQuestionnaire()
#         if qID in self.qIDList:
#             return True
#         else:
#             return False

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    alipayID = models.CharField(max_length=50, primary_key=True)
    userName = models.TextField()
    qIDs = models.CharField(max_length=500)
    counting = models.IntegerField(default=0)

    def setAllQuestionnaire(self):
        if self.qIDs != "":
            self.qIDList = self.qIDs.split(";")
        else:
            self.qIDList = []

    def isDone(self, qID):
        self.setAllQuestionnaire()
        if hasattr(self, 'qIDList'):
            if qID in self.qIDList:
                return True

        return False


    def __unicode__(self):
        print "*****success*****"
