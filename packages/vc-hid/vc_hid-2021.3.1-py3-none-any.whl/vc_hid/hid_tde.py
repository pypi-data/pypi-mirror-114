
import vc_hid as hid

pid="89a"
setID="28"
readID="29"
controlID=1
readnumber=16


if(__name__)=="__main__":
    anotherCMD=[0,0,0,0]

    passflag,data=hid.readset(pid,setID,controlID,readnumber,anotherCMD)
    print(passflag,data)

    
    passflag,data=hid.readhid(pid,readID,controlID,readnumber)  
    print(passflag,data)
   








