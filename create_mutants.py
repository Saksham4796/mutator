# Change the name of the program in the code with <file-to-mutate.c>
import os
import re
import sys
import random
import re

### Mutation tricks ###

NULL_STRING = " "

mutation_trick = {
	" < " : 
		[ " != ", " > ", " <= ", " >= ", " == " ],
	" > " : 
		[ " != ", " < ", " <= ", " >= ", " == " ],
	" <= " : 
		[ " != ", " < ", " > ", " >= ",  "==" ],
	" >= " : 
		[ " != ", " < ", " <= ", " > ",  "==" ],
	" == " : 
		[ " != ",  " < ",  " > ", " <= ", " >= " ],
	"==" : 
		[ " != " ],
	" != " : 
		[ " == ",  " < ",  " > ", " <= ", " >= " ],
	"!=" : 
		[ " == " ],
	
	" + " : 
		[ " - ", " * ", " / " ],

	" += " : 
		[ " -= ", " *= ", " /= " ],

	" - " : 
		[ " + ", " * ", " / " ],

	" -= " : 
		[ " += ", " *= ", " /= " ],

	" * " : 
		[ " + ", " - ", " / " ],

	" *= " : 
		[ " += ", " -= ", " /= " ],

	" / " : 
		[ " * ", " + ", " - " ],

	" /= " : 
		[ " *= ", " += ", " -= " ],

 	" % " : 
		[ " / ", " + ", " - ", " * " ],

	" %= " : 
		[ " /= ", " += ", " -= ", " *= " ],

	"+1" :
		[ " - 1", "+ 0", "+ 2", "- 2" ],
	"-1" :
		[ " + 1", "+ 0", "+ 2", "- 2" ],

	
	
	" ! " : 
		[  NULL_STRING ],

	" && " : 
		[ " || " ],

	" || " : 
		[ " && " ],

				
	"true"  : [ "false" ],
	"false" : [ "true" ]

		
}
	

def main (input_file) :

	
	source_code = open(input_file).read().split('\n')
	number_of_lines_of_code = len(source_code)

	z = 1
	
	b = -1

	for i in range(number_of_lines_of_code) :	
		
		#print source_code[i]

		cmmt = 0
		ff = 0

		
		if i <= b :
			print "fffffffffffffffffff"
			continue

		
		if source_code[i].find("/*") != -1 and source_code[i].find("*/") != -1 :
			ci = source_code[i].find("/*")
			comment = source_code[i][ci:]
			source_code[i] = source_code[i][:ci]
			cmmt = 1
			#print "i1="+str(i)
		
		
		if source_code[i].find("/*") != -1 and source_code[i].find("*/") == -1 :
			a = i
			#print "i2="+str(i)
			for kappa in range(i+1,number_of_lines_of_code) :
				#print "i2="+str(kappa)
				if source_code[kappa].find("*/") != -1 :
					b = kappa
					ff = 1
					break

		if ff == 1 :
			continue
					

		#print "i3="+str(i)

		mutant_operators = list(mutation_trick.keys())
		
		mutated_line = "" 
		
		if source_code[i]=="" :
			if cmmt == 1 :
				source_code[i] = source_code[i]+comment
			continue
		
		for m in mutant_operators :
		
			if m == " || " :
				idx = []
				for k in range(len(source_code[i])-1):
					if source_code[i][k]=='|' and source_code[i][k+1]=='|' :
						idx.append(k)
				
				
				if len(idx) > 0 :
						
					for mutate_at_index in idx :
						
						for mutate_with in mutation_trick[m] :

							f = open("faulty_line_m"+str(z)+".txt","w")
							f.write(str(i+1))
							f.close()

							print("\n==> @ Line: "+str(i+1)+"\n\n")
							print("Original Line  : "+source_code[i].strip()+"\n")

							if cmmt == 0:
								mutated_line = source_code[i][0:mutate_at_index-1] +mutate_with+ source_code[i][mutate_at_index+3:]
							else :
								mutated_line = source_code[i][0:mutate_at_index-1] +mutate_with+ source_code[i][mutate_at_index+3:] + comment

							print("After Mutation : "+mutated_line.strip()+"\n")
							print("Changed "+m+"with "+mutate_with+"\n")

							output_file = open("print_tokens_m"+str(z)+".c","w")

							for p in range(0,len(source_code)) :
								if p == i : 
									output_file.write("/* XXX: original code was : "+source_code[p]+" */\n")
									output_file.write(mutated_line+"\n")
								else :
									output_file.write(source_code[p]+"\n")

							output_file.close()

							print("\nOutput written to "+"print_tokens_m"+str(z)+".c"+"\n")

							print("\n")
							z = z + 1
					
						
			else :		
				number_of_substrings_found = source_code[i].count(m)
				
				if number_of_substrings_found > 0 :
					
					idx = [k.start() for k in re.finditer(m,source_code[i])]
					#print idx
					#print m+" is present at the above locations in::"+source_code[i]
							
					for mutate_at_index in idx :

						for mutate_with in mutation_trick[m] :

							f = open("faulty_line_m"+str(z)+".txt","w")
							f.write(str(i+1))
							f.close()

							print("\n==> @ Line: "+str(i+1)+"\n\n")
							print("Original Line  : "+source_code[i].strip()+"\n")

							if cmmt == 0 :
								mutated_line = source_code[i][0:mutate_at_index] + source_code[i][mutate_at_index:].replace(m,mutate_with,1)
							else :
								mutated_line = source_code[i][0:mutate_at_index] + source_code[i][mutate_at_index:].replace(m,mutate_with,1) + comment

							print("After Mutation : "+mutated_line.strip()+"\n")
							print("Changed "+m+"with "+mutate_with+"\n")

							output_file = open("print_tokens_m"+str(z)+".c","w")

							for p in range(0,len(source_code)) :
								if p == i : 
									output_file.write("/* XXX: original code was : "+source_code[p]+" */\n")
									output_file.write(mutated_line+"\n")
								else :
									output_file.write(source_code[p]+"\n")

							output_file.close()

							print("\nOutput written to "+"print_tokens_m"+str(z)+".c"+"\n")

							print("\n")
							z = z + 1
					

				else :
					continue
	
		if cmmt == 1 :
			source_code[i] = source_code[i]+comment					
							

if __name__ == "__main__":
#
	if len(sys.argv) == 2: 
		main(sys.argv[1]) 
	
	else:
		print("Usage: python create_mutants.py <file-to-mutate.c> ")
#

