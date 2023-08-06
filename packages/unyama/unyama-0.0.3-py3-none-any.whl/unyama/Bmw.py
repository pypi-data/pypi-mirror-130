# Python code to illustrate the Modules
class Bmw:
	# First we create a constructor for this class
	# and add members to it, here models
	def __init__(self, masubi):
		self.models = ['i8', 'x1', 'x5', 'x6']
		self.masubi = masubi
	# A normal print function
	def outModels(self):
		print(f'{self.masubi} These are the available models for BMW')
		for model in self.models:
			print('\t%s ' % model)
