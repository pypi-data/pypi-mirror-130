# myprofile.py

class profile:
	'''
	Example 
	=========================================================
	print('start')
	me = profile('Mama')             #จะได้ return init ของ class นั้นมา โดย pass ค่า Mama ไปที่ name
	print(me)
	print(me.name)                   #print ค่า name ใน function
	me.company = 'ABC'
	me.show_email()                  #Call function show_email 
	print('----------------')

	me.hobby = ['Youtuber','Reading','Sleeping']
	me.show_hobby()


	other = profile('Papa')
	print(other)
	print(other.name)
	other.show_email()

	art = other.show_ascii_art()
	print(art)
	print('\n',other.show_ascii_art())     #

	'''
	def __init__(self,name):               #Initialization
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
          _ _
     _(,_/ \ \____________
     |`. \_@_@   `.     ,'
     |\ \ .        `-,-'
     || |  `-.____,-'
     || /  /
     |/ |  |
`..     /   \
  \\   /    |
  ||  |      \
   \\ /-.    |
   ||/  /_   |
hh \(_____)-'_)
		'''
		print('Hello init!!!!')

	def show_email(self):
		print('email!!!@gmail.com')
		if self.company != '':             # not equal
			print('{}@{}.com'.format(self.name.lower(),self.company)) #แทน {} ด้วย name ที่รับมาจาก class และ set ให้เป็น lowercase
		else:
			print('{}@gmail.com'.format(self.name.lower(),self.company)) #แทน {} ด้วย name ที่รับมาจาก class และ set ให้เป็น lowercase

	def show_ascii_art(self):
		print(self.art)
		return self.art                #ถ้าไม่มี return จะไม่่มีต่าอะไรส่งกลับมา

	def show_hobby(self):
		if len(self.hobby) != 0:
			print('------------My Hobbi------------')
			for h in enumerate(self.hobby,start=1):
				print(h)
			print('--------------------------------')
		else:
			print_('Has no')


def print_hi():
	print('Hi!')

# print('Name:',__name__)         #__name__ จะใช้แทนชื่อไฟล์ที่รัน

if __name__ == '__main__':          
	print('start')
	me = profile('Mama')             #จะได้ return init ของ class นั้นมา โดย pass ค่า Mama ไปที่ name
	print(me)
	print(me.name)                   #print ค่า name ใน function
	me.company = 'ABC'
	me.show_email()                  #Call function show_email 
	print('----------------')

	me.hobby = ['Youtuber','Reading','Sleeping']
	me.show_hobby()


	other = profile('Papa')
	print(other)
	print(other.name)
	other.show_email()

	art = other.show_ascii_art()
	print(art)
	print('\n',other.show_ascii_art())     #

	help(other)                   # แสดง Help ที่อยู่ใต้ Class ''' '''






