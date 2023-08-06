from turtle import *
# coding utf-8
'''此函数使用说明：此函数使用方法为  等边三角形(right或left，初始角
度，边长，颜色，粗细)'''
def 等边三角形(fx='right',cxjd=0,bc=10,color='black',size=1,dbxzfx='right'):
	pencolor(color)
	pensize(size)
	setheading(cxjd)
	for i in range(3):
		forward(bc)
		right(120)
	if dbxzfx=='right':
		right(120)
	elif dbxzfx=='left':
		left(120)
	pencolor('black')

#此函数结束

'''此函数使用说明：此函数使用方法为  正方形(right或left，初始角
度，边长，颜色，粗细，单边旋转方向)'''
def 正方形(fx='right',cxjd=0,bc=10,color='black',size=1,dbxzfx='right'):
	pencolor(color)
	pensize(size)
	setheading(cxjd)
	for i in range(4):
		forward(bc)
		if dbxzfx=='right':
			right(90)
		elif dbxzfx=='left':
			left(90)

#此函数结束

def 八边形(cxjd=0,bc=10,color='black',size=1,dbxzfx='right'):
	pencolor(color)
	pensize(size)
	setheading(cxjd)
	for i in range(8):
		forward(bc)
		if dbxzfx=='right':
			right(45)
		elif dbxzfx=='left':
			left(45)