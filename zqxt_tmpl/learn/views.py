# coding=utf-8
from django.shortcuts import render

# Create your views here.
def home(request):
	string=u"我在自强学堂学习Django，用它来建网站"
	TutorialList=["HTML","CSS","jQuery","Python","Django"]
	info_dict={'site':u'自强学堂','content':u'各种IT技术教程'}
	List=map(str,range(1000))
	return render(request,'home.html',{'List':List})