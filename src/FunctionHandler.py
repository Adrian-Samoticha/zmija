class FunctionHandler:
	declare_functions = []
	init_functions = []
	variables = {}
	generate_function_return_value = ""
	
	def add_function(declare, init):
		FunctionHandler.declare_functions.append(declare)
		FunctionHandler.init_functions.append(init)
		
	def execute_functions():
		for declare in FunctionHandler.declare_functions:
			declare(FunctionHandler.variables)
		for init in FunctionHandler.init_functions:
			init(FunctionHandler.variables)