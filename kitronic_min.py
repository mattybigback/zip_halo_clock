_A=False
from microbit import i2c,pin19,pin20
class KitronikRTC:
	CHIP_ADDRESS=111;RTC_SECONDS_REG=0;RTC_MINUTES_REG=1;RTC_HOURS_REG=2;RTC_WEEKDAY_REG=3;RTC_DAY_REG=4;RTC_MONTH_REG=5;RTC_YEAR_REG=6;RTC_CONTROL_REG=7;RTC_OSCILLATOR_REG=8;RTC_PWR_UP_MINUTE_REG=28;START_RTC=128;STOP_RTC=0;ENABLE_BATTERY_BACKUP=8;currentSeconds=0;currentMinutes=0;currentHours=0
	def __init__(A):i2c.init(freq=100000,sda=pin20,scl=pin19);B=bytearray(2);C=bytearray(1);D=0;E=0;B[0]=A.RTC_SECONDS_REG;i2c.write(A.CHIP_ADDRESS,B,_A);C=i2c.read(A.CHIP_ADDRESS,1,_A);D=C[0];B[0]=A.RTC_CONTROL_REG;B[1]=67;i2c.write(A.CHIP_ADDRESS,B,_A);B[0]=A.RTC_WEEKDAY_REG;i2c.write(A.CHIP_ADDRESS,B,_A);C=i2c.read(A.CHIP_ADDRESS,1,_A);E=C[0];B[0]=A.RTC_WEEKDAY_REG;B[1]=A.ENABLE_BATTERY_BACKUP|E;i2c.write(A.CHIP_ADDRESS,B,_A);B[0]=A.RTC_SECONDS_REG;B[1]=A.START_RTC|D;i2c.write(A.CHIP_ADDRESS,B,_A)
	def readValue(A):C=bytearray(1);B=bytearray(7);A.readCurrentSeconds=0;C[0]=A.RTC_SECONDS_REG;i2c.write(A.CHIP_ADDRESS,C,_A);B=i2c.read(A.CHIP_ADDRESS,7,_A);A.currentSeconds=((B[0]&112)>>4)*10+(B[0]&15);A.currentMinutes=((B[1]&112)>>4)*10+(B[1]&15);A.currentHours=((B[2]&48)>>4)*10+(B[2]&15)
	def setTime(B,setHours,setMinutes,setSeconds):E=setSeconds;D=setMinutes;C=setHours;A=bytearray(2);A[0]=B.RTC_SECONDS_REG;A[1]=B.STOP_RTC;i2c.write(B.CHIP_ADDRESS,A,_A);A[0]=B.RTC_HOURS_REG;A[1]=int(C/10)<<4|int(C%10);i2c.write(B.CHIP_ADDRESS,A,_A);A[0]=B.RTC_MINUTES_REG;A[1]=int(D/10)<<4|int(D%10);i2c.write(B.CHIP_ADDRESS,A,_A);A[0]=B.RTC_SECONDS_REG;A[1]=B.START_RTC|int(E/10)<<4|int(E%10);i2c.write(B.CHIP_ADDRESS,A,_A)
	def readSec(A):return A.currentSeconds
	def readMin(A):return A.currentMinutes
	def readHrs(A):return A.currentHours