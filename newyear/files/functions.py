from random import randint

goalList = ["More Productive", "Initiate Projects", "Work on Happiness","Quit Smoking", "Sleep More", "Save More Money", "Better Temperment", "Lose Weight", "Eat Healthier", "Get Good Grades", "Show Gratitude", "Get Organized", "Cook More Often", "Be More Patient", "Love Myself", "Exercise"]

modivation = ["Strive for progress!", "There are no limits to what you can accomplish!", "Fear is a reaction but courage is a decision!", "Push yourself because no one else will do it for you!", "You are stronger than you know!"]

def checkGoalList(goalType):
  print(goalType)
  if goalType in goalList or goalType == "None":
    return True
  else: 
    return False

def checkExists(checkList):
  for x in checkList:
    if not x:
      return False
  return True

def getModivation():
  random = randint(0, len(modivation)-1)
  return modivation[random]
