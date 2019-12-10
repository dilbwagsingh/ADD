import random
import os

def fuzzer(elf):
	idx = random.randint(0,len(elf));
	c = chr(random.randint(0,0xff));
	return elf[:idx]+c.encode()+elf[idx+1:];

def copy_elf(str,new_name):
	with open(str,'rb') as original_file, open(new_name,'wb') as new_file:
		new_file.write(fuzzer(original_file.read()));

def compare(str1,str2):
	return str1==str2;

def check_output(elf_name,new_name):
	cmd1 = "./{0} > original_output".format(elf_name);
	cmd2 = "./{0} > new_output".format(new_name);
	os.system(cmd1);
	os.system(cmd2);
	with open("original_output",'r') as oo ,open("new_output",'r') as no:
		return compare(oo.read(),no.read());

def check_gdb(elf_name,new_name):
	cmd1 = "echo disass main | gdb {0} > original_gdb_output".format(elf_name);
	cmd2 = "echo disass main | gdb {0} > new_gdb_output".format(new_name);
	os.system(cmd1);
	os.system(cmd2);
	with open("original_gdb_output",'r') as ogdb, open("new_gdb_output",'r') as ngdb:
		ogdb = ogdb.read().split("(gdb)")[1];
		ngdb = ngdb.read().split("(gdb)")[1];
		return compare(ogdb,ngdb);

def check_radare2(elf_name,new_name):
	cmd1 = 'echo -e "aaa\n sym.main\n pdf\n" | r2 {0} > original_r2_output'.format(elf_name);
	cmd2 = 'echo -e "aaa\n sym.main\n pdf\n" | r2 {0} > new_r2_output'.format(new_name);
	os.system(cmd1);
	os.system(cmd2);
	with open("original_r2_output",'r') as or2, open("new_r2_output",'r') as nr2:
			return compare(or2.read(),nr2.read());


elf_name = input("Enter the name of the executable:");
new_name = elf_name+"_new";

while True:
	copy_elf(elf_name,new_name);


	cmd = "chmod +x {0}".format(new_name);
	os.system(cmd);


	p = check_output(elf_name,new_name) and not check_gdb(elf_name,new_name) and not check_radare2(elf_name,new_name);
	if(p == 1):
		print("Operation Successful!!!");
		break;

cmd = "rm -f original_output new_output original_gdb_output new_gdb_output new_r2_output original_r2_output"
os.system(cmd);
