import paramiko 
import psycopg2 

host = '10.0.2.15'
user = 'kursant'
secret = '12345678'
port = 22
connect=psycopg2.connect(database='inf_disk',user='inf_disk',host='localhost',password='12345678')
cursor=connect.cursor()
cursor.execute("delete from disk")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)
stdin, stdout, stderr = client.exec_command("lshw -short -C disk|grep -v =|grep -v H/W|awk '{print $1}'")
hw = stdout.read()
stdin, stdout, stderr = client.exec_command("lshw -short -C disk|grep -v =|grep -v H/W|awk '{print $2}'")
device = stdout.read()
device=device[1:]
stdin, stdout, stderr = client.exec_command("lshw -short -C disk|grep -v =|grep -v H/W|awk '{print $3}'")
clas = stdout.read()
stdin, stdout, stderr = client.exec_command("lshw -short -C disk|grep -v =|grep -v H/W|awk '{print $4}'")
desc = stdout.read()    
adding_inf="insert into disk(hw,device,class,description) values ('"+hw+"','"+device+"','"+clas+"','"+desc+"');"    
cursor.execute(adding_inf)

connect.commit()
connect.close()
client.close()
