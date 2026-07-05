from cryptography.fernet import Fernet
import datetime
from dotenv import get_key
from sqlalchemy import text,create_engine
from duplicateDetection import  dupllicateDetection
"""
This vault report generates a detailed report of your passwords giving you a suitable score based on your password age and  number of reused passwords
"""

def fetchData(uuid,cipher:Fernet,longest,shortest,d,avg,total,sum_,overall_score,duplicates):
    connection = create_engine(get_key("./.env","USERS_connection_string")).connect()
    query = text("select password,date_created from vault where vault_uuid=:uuid")
    
    cur = connection.execute(query,{
        "uuid":uuid
    }).fetchall()
    for i in cur:
       total+=1
       print(i[0])
       x=  len(cipher.decrypt(bytes(i[0])).decode())
       current = datetime.datetime.now(datetime.timezone.utc)
       days = (current-i[1]).days
       if days<90:
           d["<90 Days"]+=1
       elif days<180:
           d["90-180 Days"]+=1
       elif days<365:
           d["180-365 Days"]+=1
       else:
           d[">365 Days"]+=1
       sum_+=x
       if x>longest:
           longest=x
       elif x<shortest:
           shortest=x
    overall_score -= min(duplicates * 10, 40)

    overall_score -= min(d[">365 Days"] * 12, 40)
    overall_score -= min(d["180-365 Days"] * 6, 30)
    overall_score -= min(d["90-180 Days"] * 3, 20)
    
    avg_len = sum_ / total if total else 0
    
    if avg_len >= 12:
        overall_score += 10
    elif avg_len >= 8:
        overall_score += 5
    else:
        overall_score -= 10
    
    overall_score = max(0, min(overall_score, 100))
    return total, sum_, longest, shortest, d, overall_score
def vaultReport(UUID:str,cipher:Fernet):
    longest  = 0
    shortest=500
    avg=0
    total=0
    sum_ = 0
    overall_score =  100
    duplicates = len(dupllicateDetection(UUID,cipher))
    d={"<90 Days":0,"90-180 Days":0,"180-365 Days":0, ">365 Days":0}
    total,sum_,longest,shortest,d,overall_score= fetchData(UUID,cipher,longest,shortest,d,avg,total,sum_,overall_score,duplicates)
    print('\n=====================================\n')
    print("           VAULT REPORT              ")
    print('\n=====================================\n')
    print("VAULT_UUID: \t\t\t\t",UUID)
    print("Total Passwords: \t\t\t\t",total)
    print("              Password Stats               ")
    print("-------------------------------------------")
    print("Unqiue Passwords: \t\t\t\t",total-duplicates)
    print("Reused Passwords: \t\t\t\t",duplicates)
    print("Average Length: \t\t\t\t",sum_ / total if total else 0)
    print("Shortest Password: \t\t\t\t",shortest)
    print("Longest Password: \t\t\t\t",longest)
    print("              Password Age               ")
    print("-------------------------------------------")
    print("<90 Days: \t\t\t\t", d["<90 Days"])
    print("90-180 Days: \t\t\t\t", d["90-180 Days"])
    print("180-365 Days: \t\t\t\t", d["180-365 Days"])
    print(">365 Days: \t\t\t\t", d[">365 Days"])
    print("             Security Assessment           ")
    print("-------------------------------------------")
    if overall_score>100:
        overall_score=100
    elif overall_score<0:
        overall_score=0
    print("Overall Score: ",overall_score)
    print("Press Enter To Move Back To Menu:")
    input("")
    