class Profile:
	
	'''
	EXAMPLE

	if __name__ == '__main__':
	my = Profile('Cum')
	my.company = 'pusspuss'
	my.hobby = ['Youtuber','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	'''


	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []

	def show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name.lower(),self.company.lower()))
		else:
			print('{}@gmail.com'.format(self.name.lower()))

	def show_myart(self):
		art = ''' 
			  (
               )
              (
        /\\  .-"""-.  /\\
       //\\/  ,,,  \\//\\
       |/\\| ,;;;;;, |/\\|
       //\\\\;-"""-;///\\
      //  \\/   .   \\/  \\
     (| ,-_| \\ | / |_-, |)
       //`__\\.-.-./__`\\
      // /.-(() ())-.\\ \\
     (\\ |)   '---'   (| /)
      ` (|           |) `
        \\)           (/ 
        	  '''

		print(art)

	def show_hobby(self):
		if len(self.hobby) !=0:
			print('-------my hobby-------')
			for i,h in enumerate(self.hobby,start=1):
				print(i,h)
			print('----------------------')
		else:
			print('No hobby')


if __name__ == '__main__':
	my = Profile('Cum')
	my.company = 'pusspuss'
	my.hobby = ['Youtuber','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

