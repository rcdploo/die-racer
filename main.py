import random
import time
import sys
import json
import urllib.request
import json

game_len = 7

#into--put text up while APIs load
print("Laaaaaadies aaaaand Geeeentlmen..... Welcome to DIE-RACER ARENA\n")
print("Hold on to your hats because do we have some exciting races for you tonight!\n")
print("Prepare to be entertained by all the die-based horsepower YOU. CAN. HANDLE.\n")
print("Your $10 entry will let you bet on up to "+str(game_len)+" races... if you don't lose it all first!\n")
print("Let's see if today is your lucky day!\n")

#get word lists
url = urllib.request.urlopen("http://api.wordnik.com/v4/words.json/randomWords?api_key=iodw5ezxg3dgfuuh33p4idggzs8fjwnkgwwpgrh54vzym3wh0&includePartOfSpeech=adjective&minCorpusCount=10000")
adjectives = json.loads(url.read())

url = urllib.request.urlopen("http://api.wordnik.com/v4/words.json/randomWords?api_key=iodw5ezxg3dgfuuh33p4idggzs8fjwnkgwwpgrh54vzym3wh0&includePartOfSpeech=noun&minCorpusCount=10000")
nouns = json.loads(url.read())

#set up functions used within races
def getdievalues():
  dievals = [random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6),random.randint(1,6)]

  if 15 <= sum(dievals) <= 27:
    return dievals
  else:
    return getdievalues()

def isprime(num):  
  if num == 2: 
    return True
  for i in range(2,num-1):
    if num % i == 0:
      return False
  return True

class die:
  def __init__(self):
    adj = adjectives.pop(0)
    noun = nouns.pop(0)
    shape = dieshapes.pop(0)
    shortname = adj['word'][0]+noun['word'][0]
    self.name = adj['word'].upper()+ " " + noun['word'].upper()
    self.icon = shape.replace("XX",shortname.upper())
    self.values = getdievalues()
    self.values.sort()
    self.power = diepowers.pop(random.randint(0,len(diepowers)-1))

def roll(die):
  dx = die.values[random.randint(0,5)]
  dy = die.values[random.randint(0,5)]

  #show initial roll
  print(die.name, " rolls!")
  time.sleep(0.5)

  

  if die.power['name'] == "Doubles" and dx==dy:
    print([dx],[dy])
    time.sleep(0.5)
    total = 2*(dx+dy)
    print("Doubles Double!")
    time.sleep(0.5)
    print([dx],[dy],",",[dx],[dy],"=",str(total))
  elif die.power['name'] == "Highest" and dx != dy:
    print([dx],[dy])
    time.sleep(0.5)
    disp = dx if dx > dy else dy
    total = dx+dy + abs(dx-dy)
    print("Adjusting...")
    time.sleep(0.5)
    print([disp],[disp],"=",str(total)) 
  elif die.power['name'] == "Low3of4":
    dx2 = die.values[random.randint(0,5)]
    dy2 = die.values[random.randint(0,5)]
    print([dx],[dy],[dx2],[dy2])
    time.sleep(0.5)
    print("Keep the 3 lowest")
    dlist = [dx,dy,dx2,dy2]
    dlist.sort()
    time.sleep(0.5)
    total = dlist[0]+dlist[1]+dlist[2]
    print([dlist[0]],[dlist[1]],[dlist[1]],"=",str(total))

  elif die.power['name'] == "Primes" and isprime(dx+dy):
    print([dx],[dy])
    time.sleep(0.5)
    dx2 = die.values[random.randint(0,5)]
    dy2 = die.values[random.randint(0,5)]
    total = dx+dy+dx2+dy2
    print("Prime! Roll Again")
    time.sleep(0.5)
    print([dx2],[dy2])
    time.sleep(0.5)
    print([dx],[dy],",",[dx2],[dy2],"=",str(total))  
  else:
    total = dx+dy
    print([dx],[dy],"=",str(total))
    time.sleep(0.5)
  print("\n")
  
  return total

def getbet():
  bet = input("")

  if bet == '1' or bet=='2':
    return int(bet)
  else:
    print("Type either '1' or '2'")
    return getbet()

def betsize(minb,maxb):
  size = input("")
  if size.isnumeric():
    if minb <= int(size) <= maxb:
      if int(size) > bankroll:
        print("You don't have enough money. Bet up to $"+str(bankroll)+"\n")
        return betsize(minb,maxb)
      return int(size)
    else:
      print("Type a number between "+str(minb)+" and "+str(maxb)+"\n")
      return betsize(minb,maxb)
  else:
    print("Type a number between "+str(minb)+" and "+str(maxb)+"\n")
    return betsize(minb,maxb)

def showtrail(die,dist,start=0): 
  for i in range (start,dist+1):
    sys.stdout.write("."*i + die.icon + chr(8)*(i+ len(die.icon)))
    sys.stdout.flush()
    time.sleep(0.05)
  print('')
  time.sleep(1)

#run a race
def race():
  global bankroll 
  global race_num
  global max_bet
  
  #generate die racers
  die1 = die()
  die2 = die()
  
  print("Race "+str(race_num+1))
  print(die1.name+" vs. "+die2.name+"\n")

  print(die1.name+"\n", die1.values," ", die1.values,"\nPower: "+die1.power['desc']+"\n")

  print(die2.name+"\n", die2.values," ", die2.values,"\nPower: "+die2.power['desc']+"\n")

  print(die1.icon)
  print(die2.icon+"\n")

  #get bet
  print("Who do you want to bet on?\n1. "+die1.name+"\n2. "+die2.name+"\n")
  pick = getbet()

  print("How much do you want to bet? (Bankroll=$"+str(bankroll)+" Min Bet=$"+str(race_num+1)+" Max Bet=$"+str(max_bet)+")")
  amt = betsize(race_num+1,max_bet)

  dist1 = 0
  dist2 = 0

  #first leg of three
  print("\n<<First leg>>")
  dist1 += roll(die1)
  dist2 += roll(die2)

  showtrail(die1,dist1)
  showtrail(die2,dist2)
  print("\n")

  #offer double down if behind
  if ((pick == 1 and dist1 < dist2) or (pick == 2 and dist2 < dist1)) and bankroll >= amt*2:
    dd = input("Your racer has fallen behind! Do you want to double down on your bet? Y or N\n")
    while dd not in ('Y','y','N','n'):
      dd = input("Type Y or N")
    if dd in ('Y','y'):
      amt *= 2
      print("Double down! Your bet is now $"+str(amt))
    elif dd in ('N','n'):
      print("Your bet it still $"+str(amt))

  #first leg text
  elif dist1 > dist2:
    print(die1.name+" is off to an early lead!\n")
    
  elif dist2 > dist1:
    print(die2.name+" is faster out of the gate!\n")

  elif dist2 == dist1:
    print("The racers are neck and neck!\n")

  time.sleep(2)

  #second leg
  print("\n<<Second leg>>")
  start1 = dist1
  start2 = dist2
  dist1 += roll(die1)
  dist2 += roll(die2)

  showtrail(die1,dist1,start1)
  showtrail(die2,dist2,start2)
  print("\n")

 #second leg text
  if dist1 > dist2 and start1 <= start2:
    print(die1.name+" surges ahead!\n")
  elif dist1 < dist2 and start1 >= start2:
    print(die2.name+" takes the lead!\n")
  elif abs(dist1 - dist2) > 7:
    print("This is looking like it'll be a blowout")
  elif 3 <= dist1 - dist2 <= 7:
    print(die1.name+" is in control for now!\n")
  elif 3 <= dist2 - dist1 <= 7:
    print("It's "+die2.name+"'s race to lose!\n")
  elif abs(dist2 - dist1) <= 2:
    print("This one will come right down to the wire!\n")

  time.sleep(2)
  
  #final leg
  print("\n<<FINAL leg>>")
  start1 = dist1
  start2 = dist2
  dist1 += roll(die1)
  dist2 += roll(die2)

  showtrail(die1,dist1,start1)
  showtrail(die2,dist2,start2)
  print("\n")

  #final leg text

  if dist1 > dist2:
    if start1 <= start2:
      print(die1.name+" with the come-from-behind victory!\n")
    elif dist1 - dist2 > 7:
      print("An absolute rout by "+die1.name+"\n")
    elif 3 <= dist1 - dist2 <= 7:
      print(die1.name+" wins!\n")
    elif 0 < dist1 - dist2 <= 2:
      print(die1.name+" pulls out the victory in close finish!\n")

    if pick == 1:
      bankroll += amt - race_num
      print("Your winnings: $"+str(amt)+" - $"+str(race_num)+" race fee = $"+str(amt-race_num))
      print("Bankroll: $"+str(bankroll))
    elif pick == 2:
      bankroll -= amt
      print("Your winnings: -$"+str(amt))
      print("Bankroll: $"+str(bankroll))

  elif dist2 > dist1:
    if start1 >= start2:
      print(die2.name+" has passed "+die1.name+" for the win!\n")
    elif dist2 - dist1 > 7:
      print("Commanding performance from "+die2.name+"\n")
    elif 3 <= dist2 - dist1 <= 7:
      print(die2.name+" wins!\n")
    elif 0 < dist1 - dist2 <= 2:
      print(die2.name+" wins by a nose!\n")

    if pick == 2:
      bankroll += amt - race_num
      print("Your winnings: $"+str(amt)+" - ($"+str(race_num)+" race fee) = $"+str(amt-race_num))
      print("Bankroll: $"+str(bankroll))
    elif pick == 1:
      bankroll -= amt
      print("Your winnings: -$"+str(amt))
      print("Bankroll: $"+str(bankroll))

    elif dist1 == dist2:
      print("It's a dead-even draw!\n")
      bankroll -= race_num
      print("Your winnings: $0 - ($"+str(race_num)+" race fee) = $"+str(0-race_num))
      print("Bankroll: $"+str(bankroll))

  print("\n")
  time.sleep(5)
  race_num += 1
  max_bet += race_num

 


#game starts here
diepowers = [
  {'name': 'Doubles','desc':'Doubles are doubled!'},
  {'name': 'Primes','desc':'Bonus Roll on Primes'},
  {'name': 'Low3of4','desc':'Roll 4 dice, keep the 3 lowest'},
  {'name': 'Highest','desc':'Rounds lower die up to higher'}
]

dieshapes = ["~\_XX_>","@@[XX]>","=}(XX)>","8>{XX}>"]
random.shuffle(dieshapes)

race_num=0
max_bet=3

bankroll = 10
race_num = 0

for i in range (0,game_len):
  race()

  #reset dice
  diepowers = [
    {'name': 'Doubles','desc':'Doubles are doubled!'},
    {'name': 'Primes','desc':'Bonus Roll on Primes'},
    {'name': 'Low3of4','desc':'Roll 4 dice, keep the 3 lowest'},
    {'name': 'Highest','desc':'Rounds lower die up to higher'}
  ]
  dieshapes = ["~\_XX_>","@@[XX]>","=}(XX)>","8>{XX}>"]
  random.shuffle(dieshapes)

  if bankroll <= race_num:
    print("You don't have enough money to enter the next race.\n")
    break

print("You finished the day with $"+str(bankroll)+"\n")
print("GAME OVER")

#open and update stats file
stats = open("stats.json")
js = json.load(stats)
stats.close()

js['num_plays'] += 1
js['tot_score'] += bankroll

#check for high score
if bankroll > js['highscore3']:
  print('You got a high score!\n')
  time.sleep(1)
  hs_name = ''
  while len(hs_name) != 4 and hs_name.isalnum() != True:
    hs_name = input("Enter your name (4 chars): _ _ _ _\n")
    if len(hs_name) != 4 and hs_name.isalnum() != True:
      print("Enter exactly 4 alphanumeric characters\n")

  if bankroll > js['highscore1']:
    js['highscore3'] =  js['highscore2']
    js['highscore3_name'] =  js['highscore2_name']
    js['highscore2'] =  js['highscore1']
    js['highscore2_name'] =  js['highscore1_name']
    js['highscore1'] =  bankroll
    js['highscore1_name'] =  hs_name.upper()

  elif bankroll > js['highscore2']:
    js['highscore3'] =  js['highscore2']
    js['highscore3_name'] =  js['highscore2_name']
    js['highscore2'] = bankroll
    js['highscore2_name'] =  hs_name.upper()

  elif bankroll > js['highscore3']:
    js['highscore3'] = bankroll
    js['highscore3_name'] =  hs_name.upper()

#show high scores
print("HIGH SCORES\n")
print(js['highscore1'],js['highscore1_name'])
print(js['highscore2'],js['highscore2_name'])
print(js['highscore3'],js['highscore3_name'])

print("\nAVG SCORE: "+str(js['tot_score']/js['num_plays']))

#write back updates and close the file
with open('stats.json', 'w') as outfile:
    json.dump(js, outfile)
