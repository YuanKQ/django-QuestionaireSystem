#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
import ast
# Create your models here.

# class ListField(models.TextField):
#     # __metaclass__ = models.SubfieldBase
#     description = "Stores a python list"
#
#     def __init__(self, *args, **kwargs):
#         super(ListField, self).__init__(*args, **kwargs)
#
#     #convert to content in db to python object
#     def to_python(self, value):
#         if not value:
#             value = []
#
#         if isinstance(value, list):
#              return value;
#         return ast.literal_eval(value) #equals to eval()
#
#
#     # #convert python objects to db values
#     # def get_db_prep_value(self, value):
#     #     if not value:
#     #         str = "["
#     #         str = str + ",".join(item.encode("utf-8") for item in value) + "]"
#     #         return str
#     #     return "@"
#
#     #convert the python object in the readable form
#     def get_prep_value(self,value):
#         return value
#
#     # def value_to_string(self, obj):
#     #     value = self._get_val_from_obj(obj)
#     #     return self._get_db_prep_value(value)


# class Questionnaire(models.Model):
#     question_page = models.IntegerField(verbose_name = "pageNO")
#     created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
#     updated = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
#
#     def __unicode__(self):
#         print u'试卷类别:%d [添加时间: %s, 修改时间: %s]' % (self.question_page. self.created, self.updated)
#
#     def questions(self):
#         return self.question_set.order_by('qid')
class Questionnaire(models.Model):
    qpage = models.IntegerField(primary_key=True);
    counting = models.IntegerField(default=0);

    def __unicode__(self):
        print u'问卷编号为[%d]' % (self.qpage)
        print u'统共出现的次数为： %d' % self.counting
        print u'---------------------------------'

class Question(models.Model):
    # questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    question_text = models.CharField(max_length = 100)
    # question_page = models.IntegerField(verbose_name = "pageNO")
    question_page = models.ForeignKey(Questionnaire, verbose_name= "pageNO")
    qid = models.IntegerField(verbose_name="questionNO")
    symptoms = models.TextField()
    diseases = models.TextField()

    # def __init__(self):
    #     symChoices = []
    #     disChoices = []

    # def setChoices(self, value):
    #     templist = []
    #     if isinstance(value, list):
    #         for i in value:
    #             if isinstance(i, unicode):
    #                 templist.append(i.encode('utf-8'))
    #             else:
    #                 templist.append(i)
    #     self.choices = json.dumps(templist)
    #
    # def getChoices(self):
    #     return json.loads(self.choices)

    def setAllChoices(self):
        if self.symptoms != "@":
            self.symChoices = self.symptoms.split(";")
        else:
            self.symChoices = []

        if self.diseases != "@":
            self.disChoices = self.diseases.split(";")
        else:
            self.disChoices = []


class Answer(models.Model):
    question_text = models.CharField(max_length = 100)
    symptoms = models.TextField()
    diseases = models.TextField()

    def __unicode__(self):
        print u'[%d]%s 的选项:' % (self.id, self.question_text)
        print u'symptoms: %s' % self.symptoms
        print u'diseases: %s' % self.diseases
        print u'---------------------------------'