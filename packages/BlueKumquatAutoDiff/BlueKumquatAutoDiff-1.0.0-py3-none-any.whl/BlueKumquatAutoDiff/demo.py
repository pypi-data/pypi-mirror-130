from autodiff import *

if __name__ == "__main__":
	dict_val = {"z":8, "b":16, "k":3, "g":5, "n":5}
	list_functs = ['-(z*2)+(0.5*b)','(b**2)+k','sin(4*k)-g','(n**3)+(z*2)','(n*k)','(b+7)*k']
	auto_diff_test = SimpleAutoDiff(dict_val, list_functs)
	print(auto_diff_test)

	dict_val = {'x': 1}
	list_functs = ['x * 8']
	auto_diff_test = SimpleAutoDiff(dict_val, list_functs)
	print(auto_diff_test) 

	# Variable class
	print("Variable Class Demo")
	x = Variable.sin(np.pi)
	y = Variable(2)

	print("value:",np.round(x.var), "derivative:", x.der)

	# Forward Mode Demo
	print("Forward Mode Demo")
	dict_val = {'x': 1}
	list_functs = ['x * 8', 'x + 3', 'log(x)', 'cos(x)', 'sqrt(x)', 'sinh(x)', 'arctan(x)']
	auto_diff_test = SimpleAutoDiff(dict_val, list_functs)
	print(auto_diff_test)

	# Demo Reverse Mode
	dict_val = {'x': 1, 'y': 2}
	list_funct = ['x * y + exp(x * y)', 'x + 3 * y']
	out = Reverse(dict_val, list_funct)
	print(out)
