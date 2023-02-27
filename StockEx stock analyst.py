from bs4 import BeautifulSoup
from urllib import request
import time
import csv
from matplotlib import pyplot as plt

def appendcsv(file,details):
    f=open(file,'a',newline='')
    w_obj=csv.writer(f,delimiter=',')
    w_obj.writerow(details)
    f.close()
    
def readcsv(file,spaces):
    f=open(file,'r',newline='')
    r_obj=csv.reader(f,delimiter=',')
    formatting=':<{}'.format(spaces)
    for i in r_obj:
        for j in i:
            print(('{'+formatting+'}').format(j),end='')
        print('\n'+'='*107)
        time.sleep(1)
    f.close()
    
def DAY():
    time.sleep(5)
    print("Enter Todays's Date")
    day=input('Day:')
    month=input('Month:')
    year=input('Year:')
    if day.lower() in ('saturday','sunday'):
        print('Today is a week-end, the stock exchanges around the world are closed. Try again on the next working day')
        return 'holliday'
    else:
        filename=day+' '+month+' '+year+'.csv'
        appendcsv(filename,[day,month,year])
        appendcsv(filename,['Stock','Buy Price','Sell Price','No. of shares','Net Profit or Loss'])
        return filename

def webscrapper(search,tag):       #This function returns the stock price at that instant of time
    
    URL ='https://www.bing.com/search?q='+search+'stock'

    headers = {'User Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    
    content=request.urlopen(URL) 

    htmlbin = content.read()
    htmltxt = htmlbin.decode()     # to decode to binary file to get the contents of the html file
    
    soup = BeautifulSoup(htmltxt,'html.parser')
    
    price_txt = soup.find('div',{'class':tag}).text

    price_num = ''
    count=0
    for i in price_txt[::-1] :     #To remove the ',' (commas) and make it a valid floating point literal
        if not i.isdigit():
            count += 1
            if count == 1:
                i = '.'
            else:
                i=''       
        price_num += i

    price_num = float(price_num[::-1])

    return price_num
      
def Info():
    print('Here you can look at the details of prominent trade centers in the world:')
    print()
    readcsv('info.csv',30)

def Analyst():
    global Analysis_Start  #check variable to confirm that user has entered this function
    global changes
    global avgs
    global stocks
    global k
    
    Analysis_Start=1
    k+=1
    
    stock=input('Enter the stock You wish to invest in:')
    stocks+=[stock]
    details=[]
    avg=0
    print('Analysing',end='')
    
    for i in range(11):
        cur_price=webscrapper(stock,'b_focusTextMedium')
        avg+=cur_price
        details+=[cur_price]
        if i%2==0:
            print('.',end='')
            time.sleep(2)
    print()    
    avg/=11
    avgs+=[avg]
     
    change=details[-1]-details[0]
    changes+=[change]

    plt.figure(k)
    plt.plot([0,10,20,30,40,50,60,70,80,90,100],details)# plots the line graphs for all stocks entered in the time interval of 100 seconds
    plt.title('Market Analysis '+stock+' stock')
    plt.xlabel('Time')
    plt.ylabel('Price')
    
    print(details)
        
    print('Analysis completed.')
    print()     
    print('Plotting graphs',end='')
    for i in range(3):
        print('.',end='')
        time.sleep(1)

    plt.show()

def Invest_Amount():
    global investment
    global Investment
    
    while True:
        choice=int(input('Manage your investment funds with the following functions: \n1. Modify Amount \n2. Add Investment \n3. Show Investment \n4. Back to Main Menu\n'))

        if choice==1:
            investment=int(input('Total amount you wish to invest (USD):'))
            Investment=investment
            print('Amount modified successfully.') 
        elif choice==2:
            add=int(input('Total amount you wish to add (USD):'))
            investment+=add
            print('Amount added successfully.')
        elif choice==3:
            print('Current Invested Funds :',round(investment,3),'USD')
        elif choice==4:
            print('-----------------------------------------------------------------------------------------------------------')
            break
        else:
            print('Invalid choice, please try again.')
    
    
def Trader():

    global Trade_start   #check variable to confirm that user has entered this function
    global invest_split
    global investment
    

    Trade_start=1
    
    invest_split=[]
    
    for i in stocks:
        percent=int(input('Enter the percentage to be invested in "{}"'.format(i)))
        invest_split += [percent/100*investment]
        
    for j in range(len(invest_split)):
        sharescount=0 

        cur_price1=webscrapper(stocks[j],'b_focusTextMedium')

        while invest_split[j] >= cur_price1:
                        sharescount+=1
                        invest_split[j]-=cur_price1
                       
        if (avgs[j]-cur_price1 > (0.4/100*avgs[j])) :
                        print('Trading '+stocks[j]+' shares',end='')
                        for i in range(5):
                            print('.',end='')
                            time.sleep(1)
                        print()
                        print('Price fell steeply,lets buy!')
                        cur_price2=webscrapper(stocks[j],'b_focusTextMedium')
                        NET=round((cur_price2-cur_price1)*sharescount,3)
                        investment+=NET
                       
                        appendcsv(file,[stocks[j],round(cur_price1,3),round(cur_price2,3),sharescount,NET])
                       
        elif changes[j]>0:
                        print('Trading '+stocks[j]+' shares',end='')
                        for i in range(5):
                            print('.',end='')
                            time.sleep(1)
                        print()
                        print('stock is growing,lets buy before it reaches peak!')
                        cur_price2=webscrapper(stocks[j],'b_focusTextMedium')
                        NET=(cur_price2-cur_price1)*sharescount
                        investment+=NET
                       
                        appendcsv(file,[stocks[j],cur_price1,cur_price2,sharescount,NET])
            
        else:
            k=0
            
            while True:
                        k+=1
                        print('Trading '+stocks[j]+' shares',end='')
                        for i in range(5):
                            print('.',end='')
                            time.sleep(2)
                        print()
                        cur_price2=webscrapper(stocks[j],'b_focusTextMedium')
                        if cur_price2>=cur_price1:
                           NET=(cur_price2-cur_price1)*sharescount
                           investment+=NET
                           appendcsv(file,[stocks[j],cur_price1,cur_price2,sharescount,NET])
                           break
                        if k>5:
                           print('Trading with',stocks[j],'shares at this time is not recommended, try again later') 
                           break
                
        print('Trading completed.')

        print('-----------------------------------------------------------------------------------------------------------')
     
def TodaysResult():
    
    readcsv(file,20)    
        
    if investment > Investment:
        print('You made a net profit of:',round(investment - Investment,3),"from today's investment of",round(Investment,3))
    elif investment < Investment:
        print('You made a net loss of',round(Investment - investment,3),"from today's investment of",round(Investment,3))
    else:
        print("you have made no real profit or loss from today's investment of",round(Investment,3))


# main Program

print() 
print('-----------------------------------------------------------------------------------------------------------')
print('Hi there, I am StockEx a stock analyst app ')
print('I have been created to help amatuer traders by simulating how','their investments would work out in a real market',sep='\n')
print('-----------------------------------------------------------------------------------------------------------')
print()

file=DAY()
if file != 'holliday':
    investment=0
    Analysis_Start=0
    Trade_start=0
    stocks=[]
    avgs=[]
    changes=[]
    k=0
    
    while True:
            
            print('Enter the function you wish to perform:','1. Stock Exchange Details','2. Analysis','3. Investment Amount','4. Trading',"5. Today's Net Result",'6. Exit from the application',sep='\n')
            function=int(input())
            
            print('-----------------------------------------------------------------------------------------------------------')
            
            if function==1:
                Info()
            elif function==2:
                print('Welcome to Analysis!')
                Analyst()
            elif function==3:
                Invest_Amount()
            elif function==4:
                if investment==0 or Analysis_Start==0 :
                    print('Trading can be started only once you have entered the investment amount and analysed the stock you want to trade')
                else:
                    print('Trading has Begun...')
                    Trader()
            elif function==5:
                if Trade_start==0:
                    print("Today's net gains or losses can only be viewed once you have completed trading")
                else:
                    print("Today's Net Result")
                    TodaysResult()
            elif function==6:
                exit()
            else:
                print('Invalid choice, please try again.')
                
            print()
    
    
