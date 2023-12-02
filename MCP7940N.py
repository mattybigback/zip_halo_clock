_A=False
from microbit import i2c,pin19,pin20
class MCP7940N:
	CHIP_ADDR=111;SEC_REG=0;MIN_REG=1;HR_REG=2;WKDAY_REG=3;DAY_REG=4;MTH_REG=5;YR_REG=6;CTRL_REG=7;OSC_EEG=8;PWR_UP_MIN_REG=28;START_RTC=128;STOP_RTC=0;BATT_BAK=8;cur_sec=0;cur_min=0;cur_hr=0
	def __init__(A):i2c.init(freq=100000,sda=pin20,scl=pin19);B=bytearray(2);C=bytearray(1);D=0;E=0;B[0]=A.SEC_REG;i2c.write(A.CHIP_ADDR,B,_A);C=i2c.read(A.CHIP_ADDR,1,_A);D=C[0];B[0]=A.CTRL_REG;B[1]=67;i2c.write(A.CHIP_ADDR,B,_A);B[0]=A.WKDAY_REG;i2c.write(A.CHIP_ADDR,B,_A);C=i2c.read(A.CHIP_ADDR,1,_A);E=C[0];B[0]=A.WKDAY_REG;B[1]=A.BATT_BAK|E;i2c.write(A.CHIP_ADDR,B,_A);B[0]=A.SEC_REG;B[1]=A.START_RTC|D;i2c.write(A.CHIP_ADDR,B,_A)
	def readValue(A):C=bytearray(1);B=bytearray(7);A.readCurrentSeconds=0;C[0]=A.SEC_REG;i2c.write(A.CHIP_ADDR,C,_A);B=i2c.read(A.CHIP_ADDR,7,_A);A.cur_sec=((B[0]&112)>>4)*10+(B[0]&15);A.cur_min=((B[1]&112)>>4)*10+(B[1]&15);A.cur_hr=((B[2]&48)>>4)*10+(B[2]&15)
	def setTime(B,setHours,setMinutes,setSeconds):E=setSeconds;D=setMinutes;C=setHours;A=bytearray(2);A[0]=B.SEC_REG;A[1]=B.STOP_RTC;i2c.write(B.CHIP_ADDR,A,_A);A[0]=B.HR_REG;A[1]=int(C/10)<<4|int(C%10);i2c.write(B.CHIP_ADDR,A,_A);A[0]=B.MIN_REG;A[1]=int(D/10)<<4|int(D%10);i2c.write(B.CHIP_ADDR,A,_A);A[0]=B.SEC_REG;A[1]=B.START_RTC|int(E/10)<<4|int(E%10);i2c.write(B.CHIP_ADDR,A,_A)