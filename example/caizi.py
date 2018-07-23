#coding=utf-8
import random

def caishu():
	num=random.randint(1,100)
	print("输入你猜测的数字:")
	a=input("")


	if a.isdigit():
		if a<1 or a>100:
			print ("请输入1到100之间的数字!")
			a=input("")
		elif a>num:
			print("输入的数字太大了,可以小一点!")
			a=input("")
		elif a<num:
			print("输入的数字太小了,可以再大一点!")
			a=input("")
		elif a==num:
			print("恭喜你猜中了!是否继续?输入0停止,其他键继续.")
			a=input("")
			if a==0:
				print("退出游戏!")
				#break
			else:
				caishu()
	else:
		print("请输入整数数字!")
		a=input("")

if __name__=="main":
	print("猜数字游戏!")
	caishu()