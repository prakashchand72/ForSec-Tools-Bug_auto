import time,os,subprocess,sys,signal,pyfiglet,random
from pwn import *
from termcolor import colored 

def evil_cmd(cmd):
	#print('\n[\033[1;32m+\033[1;37m]executing process')
	execute = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	result = execute.stdout.read() + execute.stderr.read()
	result = result.decode()

def kill(sig, frame):
    print("\n\033[94m[*] {}\n\033[00m" .format('Thank You For Using ForSec @ASTUTE'))
    sys.exit(1)

def delete_db():
	evil_cmd('rm -rf *.txt && rm -rf screenshots')

def rand():
	r = random.randrange(0,4)
	lst = ['red','blue','green','yellow']
	return lst[r]

def subfinder(domain):
	print(colored("---------->starting subdomains gathering<------------",'yellow')) 
	print('Target domain > ' + colored(domain,'red')) 
	print("\n\033[91m[!] {}\n\033[00m" .format('fetching subdomains , It may take some time , please wait ...'))
	evil_cmd(f'subfinder -d {domain} -o subdomains.txt')
	os.system('cat subdomains.txt')
	print(colored("total subdomains found:","yellow"),end='')
	os.system("wc -l subdomains.txt > tmp.txt && cat tmp.txt | awk '{print $1}' | lolcat")
	print("\033[92m[+] {}\n\033[00m" .format('Done '))	

signal.signal(signal.SIGINT, kill)
print(colored(pyfiglet.figlet_format('ForSec'),rand()))
print(colored(('                              developed by @astute'),rand()))
#os.system("echo '                              developed by @astute' | lolcat ")
#print(colored("\n---------->starting subdomains gathering<------------\n",'yellow')) 
ask = input(colored('1.Automation \n2.Manual \n3.Delete older database\nInput> ','green')).strip()
if ask == '1' or ask =='Automation' or ask == 'automation':
	print('worked')
	domain=input(colored('Enter Target Domain: ','blue')).strip()
	print('Target domain > ' + colored(domain,'red')) 
	print('')
	subfinder(domain)
	os.system("echo 'Starting XSS Hunting' | figlet -f mini | lolcat")
	print(colored("\n---------->Fetching waybackurls<------------\n",'yellow'))
	os.system('cat subdomains.txt | waybackurls | tee -a waybackurls.txt')
	print(colored("--------->total endpoints waybackurls found<---------","yellow"))	
	evil_cmd("wc -l waybackurls.txt > tmp.txt && cat tmp.txt | awk '{print $1}' | lolcat")
	print(colored("--------->starting XSS Payload<---------","yellow"))
	print("\033[91m[!] {}\n\033[00m" .format('Executing Process , Please wait ....'))
	#evil_cmd(xsspayload)
	act = '''cat waybackurls.txt | qsreplace '"><img src=x onerror=alert(1)>' | tee -a xss_fuzz.txt'''
	evil_cmd(act)
	print("\033[92m[+] {}\n\033[00m" .format('Done'))
	print("\n\033[93m[!] {}\n\033[00m" .format('url on red line are vulnerable to XSS \n'))
	print(colored("\nurl on red line are vulnerable to XSS \n",'red'))
	os.system('cat xss_fuzz.txt | grep onerror | freq | tee -a possible_xss.txt')
	
elif ask == '2' or ask == 'Manual' or ask == 'manual':
	
	print('also worked')
	method=input(colored('1.Technology Detection \n2.sub-domain gathering  \n3.screenshort capture + url status. . .  \n4.Vulnerability Scanning \nInput> ','green')).strip()
	if method == '1' or method == 'Technology Detection':
		url = input(colored("Enter the url>",'green')).strip() 
		print(colored("--------->starting Technology Detection with nuclei<---------\n","yellow"))
		os.system(f'nuclei -u {url}')
	elif method == '2' or method == 'sub-domain gathering':
		domainmanual = input(colored("Enter the domain>",'green')).strip()
		subfinder(domainmanual)
		"""
		print(colored("---------->starting subdomains gathering<------------",'yellow'))
		print("\n\033[91m[!] {}\n\033[00m" .format('fetching subdomains , please wait ...'))
		evil_cmd(f'subfinder -d {domainmanual} -o manualsubdomains.txt')
		os.system('cat manualsubdomains.txt')
		print(colored("total subdomains found:","yellow"))
		os.system("wc -l manualsubdomains > tmp.txt && cat tmp.txt | awk '{print $1}' | lolcat")
		print("\033[92m[+] {}\n\033[00m" .format('Done'))	
		"""
	elif method == '3' or method == 'screenshots capture':
		options = input(colored('1.single website target  \n2.multiple website url screenshots \nInput> ','green')).strip()
		if options == '1':
			print(colored("--------->starting Screenshot <---------","yellow"))	
			url = input(colored("Enter the url of taget> ",'green')).strip()
			os.system(f'echo {url} | aquatone')
			print("\033[92m[+] {}\n\033[00m" .format('Done ,Check Screenshot directory for screenshorts'))
		elif options == '2' or options == 'mal target': 
			mul_target = input(colored('Enter the file path>','green')).strip()
			cmd = f'''cat {mul_target} | aquatone tee -a statusaqua.txt'''
			os.system(cmd)
		else:
			print(colored('Invalid Input!! Entered : ','blue') + colored(options,'red')) 
	
	elif method == '4' or method == 'vulnerability scan':
		target = input(colored('Enter domain: \n')).strip()
		subdomain = subfinder(target) 
		os.system('cat subdomains.txt | httpx -o httpx.txt')
		os.system('cat httpx.txt | nuclei | tee -a nuclei_result.txt') 


	else:
		print(colored('Invalid Input!! Entered : ','blue') + colored(method,'red')) 
		
	
elif ask == '3' or ask == 'delete db':
	delete_db()
	
else:
	print(colored('Invalid Input!! Entered : ','blue') + colored(ask,'red')) 
