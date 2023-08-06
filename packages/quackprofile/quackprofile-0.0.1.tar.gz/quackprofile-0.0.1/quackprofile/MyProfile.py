# MyProfile
class Profile:
	'''
	Example:
	my = Profile('Quacker')
	my.company = 'Quacking Factory'
	my.hobby = ['Youtuber','Play Games']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	'''
	print("---------My-self---------")

	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
		  __    __
		o-''))_____\\
		"--__/ * * * )
		c_c__/-c____/
		'''
		
	def show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name,self.company))
		else:
			print('{}@gmail.com'.format(self.name))

	def show_myart(self):
		print('---------My-Art---------')
		print(self.art)


	def show_hobby(self):
		if len(self.hobby) != 0:
			print('--------My-Hobby--------')
			for i,h in enumerate(self.hobby,start=1):
				print(i, h)
		else:
			print('No Hobby')


if __name__ == '__main__':
	my = Profile('Quacker')
	my.company = 'Quacking Factory'
	my.hobby = ['Youtuber','Play Games']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	print('-------------------------')