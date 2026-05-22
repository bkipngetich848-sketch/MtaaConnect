#create a variable to create balance
bal=6000

while True:
    print('=====Welcome to bank=====')
    print('\nplease select an option:')
    print('1.check balance')
    print('2.deposit funds')
    print('3.withdraw funds')
    print('4.exit')

    choice=str(input('enter option:'))

    if choice=='1':
      print(f'your account balnce is Ksh.{bal}.')
      

    elif exitin=='2':
       deposit=int(input('enter amount to deposit: '))
       bal +=deposit
       print(f'amount Ksh {deposit} has been deposit . new account balance is Ksh{bal}\n')

    elif choice=='3':
       withdraw=int(input('enter amount to withdraw:'))
       bal-=withdraw
       print(f'amount Ksh{withdraw} jhas been withdraw succefully. new account is Ksh{bal}\n')

    elif choice =='4':
       print('are you sure you want to exit?(select 1 to continue and 2 to quit):')

       exitin=str(input('input:'))
       if exitin=='1':
          continue
       elif exitin=='2':
          print('thank you for choosing JNJ BANK. GOODBYE')
       else:
          print('invalid input!Please try again')
          for i in range(1, 6):
           print(" " * (5 - i) + "* " * i)
    a=2
b=4
c=3



