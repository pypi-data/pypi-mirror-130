#myprofile.py

class Profile:
	'''
	Example
	my = Profile('Premchai')
	my.company = 'hana'
	my.hobby = ['FX Trader','Reading','Youtube']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''		 ___________
		||         ||            _______
		||  MY PC  ||           | _____ |
		||         ||           ||_____||
		||_________||           |  ___  |
		|  + + + +  |           | |___| |
		    _|_|_   \\           |       |
		   (_____)   \\          |       |
		              \\    ___  |       |
		       ______  \\__/   \\_|       |
		      |   _  |      _/  |       |
		      |  ( ) |     /    |_______|
		      |___|__|    / CORE I3 RAM16 SSD256
		           \\_____/
		'''
	def show_email(self):
		if self.company !='':
			print('{}@{}.com'.format(self.name.lower(),self.company))
		else:
			print('{}@gmail.com'.format(self.name.lower()))

	def show_myart(self):
		print(self.art)		

	def show_hobby(self):
		if len(self.hobby) !=0:
			print('--------my hobby--------')
			for h in enumerate (self.hobby,start=1):
				print(h)
			print('------------------------')
		else:
			print('No hobby')
if __name__ == '__main__':
	my = Profile('Premchai')
	my.company = 'hana'
	my.hobby = ['FX Trader','Reading','Youtube']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()