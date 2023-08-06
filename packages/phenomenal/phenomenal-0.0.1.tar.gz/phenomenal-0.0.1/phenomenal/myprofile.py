# myprofile.py
class Profile:
	'''
	Example:

	my = Profile('Hery')
	my.company = 'Anitocorn'
	my.hobby = ['Youtuber','Coding','Reading']
	print(my.name)
	my.Show_myart()
	my.Show_email()
	my.Show_hobby()
	
	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = art = '''

		   |\
		  || \
		  | | |
		  /.,, /
		 (    /
		  \\  (
		   \\ \
		    \\_\\__
		   .'    '--._    ,__,-.,
		  /          _";__( ,__._7
		 /           )  \\,=; \\
		(         _.'     ~/  6,  '-,
		 \\___    ;        (   _,-.  Y)
		 (C(/\\.  )        /I-._\\_'-'
		       \\\\,-,_  /,,/  '-7)
		          \\  |"\\   \\  `
		           \\ _\\ \\  \\__
		            (`  \\ '.<,_)))  Maxky
		          `-\\)))

		'''

	def Show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name.lower(),self.company.lower()))
		else:
			print('{}@gmail.com'.format(self.name.lower()))

	def Show_myart(self):
		print(self.art)

	def Show_hobby(self):
		if len(self.hobby) != 0:
			print('---------my hobby--------')
			for i,h in enumerate(self.hobby,start=1):
				print(i,h)
			print('-------------------------')
		else:
			print('No hobby')

if __name__ == '__main__':
	my = Profile('Hery')
	my.company = 'phenomenal'
	my.hobby = ['Youtuber','Coding','Reading']
	print(my.name)
	my.Show_myart()
	my.Show_email()
	my.Show_hobby()
	# help(my)
	
	
