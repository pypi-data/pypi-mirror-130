#myprofile.py

class Profile:

	'''
	Example:
	my = Profile('Navapol')
	my.company = 'Mastertech'
	my.hobby = ['Youtuber','Reading']

	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
            __,__
   .--.  .-"     "-.  .--. 
  / .. \/  .-. .-.  \/ .. \ 
 | |  '|  /   Y   \  |'  | | 
 | \   \  \ 0 | 0 /  /   / | 
  \ '- ,\.-"`` ``"-./, -' / 
   `'-' /_   ^ ^   _\ '-'` 
       |  \._   _./  | 
       \   \ `~` /   / 
        '._ '-=-' _.' 
           '~---~' 
			'''

		self.art2 = '''

	              _         _
 .-""-.          ( )-"```"-( )          .-""-. 
/ O O  \          /         \          /  O O \  
|O .-.  \        /   0 _ 0   \        /  .-. O| 
\ (   )  '.    _|     (_)     |     .'  (   ) /  
 '.`-'     '-./ |             |`\.-'     '-'.'
   \         |  \   \     /   /  |         /
    \        \   '.  '._.'  .'   /        /
     \        '.   `'-----'`   .'        /
      \   .'    '-._        .-'\   '.   /
       |/`          `'''''')    )    `\|  
       /                  (    (      ,\ 
      ;                    \    '-..-'/ ;
      |                     '.       /  |
      |                       `'---'`   |
      ;                                 ;
       \                               /
        `.                           .'
          '-._                   _.-'
           __/`"  '  - - -  ' "`` \__  
         /`            /^\           `\ 
         \(          .'   '.         )/ 
          '.(__(__.-'       '.__)__).'
	
	'''
		

		# print('hello ',self.name)

	def show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name.lower(),self.company.lower()))
		else:	
			print('{}@gmail.com'.format(self.name.lower()))
	
	def show_myart(self):
		print(self.art)		

	def show_myart2(self):
		print(self.art2)		

	def show_hobby(self):
		if len(self.hobby) != 0:
			print('----my hobby----')
			for i,h in enumerate(self.hobby,start=1):
				print(i,'-',h)
		else:
			print('No hobby')		

# print(__name__)


if __name__ == '__main__':
	# print(__name__,'start')
	my = Profile('Navapol')
	my.company = 'Emj'
	# my.hobby = ['Youtuber','Reading']

	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	print('-------gf--------')
	gfriend = Profile('Tomtam')
	print(gfriend.name)
	gfriend.show_email()
	gfriend.show_myart2()
    # gfriend.show_myart()


	# print(bear)

	# help(my)



