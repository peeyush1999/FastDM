import requests
import os
import math
import threading
import random
import time

import os.path
from os import path



num_chunk =1
num_threads=1


def handle(num,chunk):
    range_str =""
    print("Chunk "+str(num)+" started\n")
    
    if(num != (num_chunk-1)):
        #print(str(chunk*num)+"-"+str(chunk*(num+1)-1)+"\n")
        range_str = "bytes="+str(chunk*num)+"-"+str(chunk*(num+1)-1)
        
    else:
        #print(str(chunk*num)+"-"+str(length)+"\n")
        range_str = "bytes="+str(chunk*num)+"-"+str(length)
    
    range_header = {'Range':range_str}
    
    response = requests.get(url,headers=range_header,stream=True)
    #print("status code : "+str(response.status_code)+"\n")
    

    flag=1
    while(flag):
        if(response.status_code == 416):
            time.sleep(5)
            response = requests.get(url,headers=range_header,stream=True)
            #print("rerquested status code : "+str(response.status_code)+"\n")
            #print("Header : "+str(response.headers)+"\n")
            #input()
        else:
            flag=0
            
            

    
    

    #print(response.content)
    #print("\n"*10)
    
    #open(,'wb').write(response.content)
    

    handle = open("temp/"+filename+"."+"{:03}".format(num), "wb")
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)

    print("Chunk "+str(num)+" completed \n")
    
    file = open("temp/res_"+filename.split(".")[0]+".txt","r+")
    file.seek(num,0)
    file.write("1")
    file.close()



#url = "https://knowindia.gov.in/assets/images/vande.mp3"
#url="https://www.python.org/ftp/python/3.9.2/python-3.9.2-embed-win32.zip"
url = input("Enter URL Of File To Be Downloaded : ")















    

#get details of the file to calculate the size of chunk 
response = requests.head(url)
#print(response.headers)


#Various parameters
filename= url.split("/")[-1]
length = response.headers['Content-Length']
Status_Code = response.status_code



#Resume Support File
f_path = "temp/res_"+filename.split(".")[0]+".txt"
if(path.exists(f_path)):
    print("File Alredy present Resuming......")
    file = open("temp/res_"+filename.split(".")[0]+".txt","r+")
    file.seek(50)
    num_threads = int(file.read(2))
    print("Number Chunk in File Were",num_threads)
else:
    num_threads = int(input("No of Parallel Threads (1-25)"))
    
chunk = math.ceil(int(length)/num_threads)
num_chunk = num_threads








print("Status Code:",Status_Code)
print("Total File Size:",length)
print("FileName: " +filename)
print("Chunk Size:",chunk, "\nNumber of Parallel Connection:",num_chunk)


if(int(response.status_code) == 200):
    print("Request Successful")
elif(int(response.status_code) == 404):
    print("File Not Found")

    



try:
    os.mkdir("temp")
except:
    print("Temp Directory Already There....\n")
    pass


if __name__=="__main__":

    threads = list()
    chunk_lst = list() #will store the chunks need to be downloaded

    f_path = "temp/res_"+filename.split(".")[0]+".txt"
    
    if(path.exists(f_path)):
        file = open("temp/res_"+filename.split(".")[0]+".txt","r+")
        file.seek(50)
        num_chunk = int(file.read(2))
        print("Number Chunk in File Were",num_chunk)
        for index in range(num_chunk):
            file.seek(index,0)
            tmp = file.read(1)
            if(tmp=="0"):    
                chunk_lst.append(index)
        file.close()
        
    else:    
        file = open("temp/res_"+filename.split(".")[0]+".txt","w+")
        temp="0"*num_chunk
        file.write(temp)
        file.seek(50)
        file.write(str(num_chunk))
        file.close()
        for index in range(num_chunk):
            chunk_lst.append(index)
        
        

    chunk = math.ceil(int(length)/num_threads)
    
    print(chunk_lst)
    for index in chunk_lst:
        
        x = threading.Thread(target=handle, args=(index,chunk))
        threads.append(x);
        x.start();

    for index,thread in enumerate(threads):
        thread.join()
        print("Thread " + str(index) + "Completed.....\n")

        


    f_path = "temp/"+filename
    new_filename = filename
    
    if(path.exists(f_path)):
        new_filename = str(random.randint(1,10))+filename

    for i in range(num_chunk):
        file = open("temp/"+filename+"."+"{:03}".format(i),'rb')

        open("temp/"+new_filename,'ab').write(file.read())
        file.close()

    print("completed")
    


