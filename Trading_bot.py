import time
from binance.client import Client
apikey = "API key to be put right here"
secretkey = "secrert key to be put right here"
client = Client(apikey,secretkey)
symbol = ["BTCUSDT","ETHUSDT","BNBUSDT","QTUMUSDT","OMGUSDT"]
intrade = [0,0,0,0,0]
sellprice = [-1,-1,-1,-1,-1]
f = open("current trading data.txt","r")
for x in range(5):
	f.readline()
	intrade[x]=bool(int(f.readline()))
	sellprice[x]=float(f.readline())
f.close()
def look_at_me_baby_i_am_rich():
	for i in range(5):
		try:
			klines = client.get_historical_klines(symbol[i], Client.KLINE_INTERVAL_1MINUTE, "4 hours ago UTC")
		except:
			time.sleep(1)
			look_at_me_baby_i_am_rich()
		curr = float(klines[-1][4])
		if (intrade[i]==0):
			##calculating rsi
			rsi = [0,0]
			for c in range(2):
				sumu = 0.0
				sumd = 0.00000001
				avgu = 0.0
				avgd = 0.0
				for j in range(1,15):
					if (float(klines[-(j+c)][4])>float(klines[-(j+c+1)][4])):
						sumu = sumu + (float(klines[-(j+c)][4])-float(klines[-(j+c+1)][4]))
					else:
						sumd = sumd + (float(klines[-(j+c+1)][4])-float(klines[-(j+c)][4]))
				avgu = sumu/14
				avgd = sumd/14
				rs = avgu/avgd
				rsi[c] = 100 - 100/(1+rs)
			##calculating 200sma
			s = 0
			for k in range(1,201):
				s = s + (float(klines[-k][2])+float(klines[-k][3]))/2
			sma = s/200

			##buy condition
			if(rsi[1]<30 and rsi[0]>=30 and curr<sma):
				try:
					client.order_market_buy(symbol= symbol[i], quantity= 50/curr)
				except:
					look_at_me_baby_i_am_rich()
				print("bought "+symbol[i]+ " for : "+ str(curr) +"\n"+time.strftime("%D  %I:%M:%S %p",time.localtime())+"\n*****\n")
				f = open("trading history.txt","a+")
				f.write("bought "+symbol[i]+ " for : "+ str(curr) +"\n"+time.strftime("%D  %I:%M:%S %p",time.localtime())+"\n*****\n")
				f.close()
				sellprice[i] = curr*1.006
				intrade[i]=1
				f = open("current trading data.txt","w+")
				for y in range(5):
					f.write(symbol[y]+'\n')
					f.write(str(int(intrade[y]))+'\n')
					f.write(str(sellprice[y])+'\n')
				f.close()

		elif(intrade[i]==1):
			##sell condition 
			if (curr >= sellprice[i]):
				try:
					client.order_market_buy(symbol= symbol[i], quantity= 50/curr)
				except:
					look_at_me_baby_i_am_rich()
				print("sold "+symbol[i]+ " for : "+ str(curr) +"\n"+time.strftime("%D  %I:%M:%S %p",time.localtime())+"\n*****\n")
				f = open("trading history.txt","a+")
				f.write("sold "+symbol[i]+ " for : "+ str(curr) +"\n"+time.strftime("%D  %I:%M:%S %p",time.localtime())+"\n*****\n")
				f.close()
				intrade[i]=0
				sellprice[i]=-1
				f = open("current trading data.txt","w+")
				for z in range(5):
					f.write(symbol[z]+'\n')
					f.write(str(int(intrade[z]))+'\n')
					f.write(str(sellprice[z])+'\n')
				f.close()
	time.sleep(10)
	look_at_me_baby_i_am_rich()
look_at_me_baby_i_am_rich()
