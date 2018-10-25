import datetime
from datetime import timedelta

weight = float(input('What is your current weight in kgs? '))
goal_weight = float(input('What is your goal weight in kgs? '))
height = float(input('What is your height in cms? '))
age = int(input('What is your age? '))
sex = input('What is your sex? M/F: ')
sex = (sex.strip()).upper()
# Harris–Benedict metric equation revised by Mifflin and St Jeor in 1990
if sex == 'F':
    BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
elif sex == 'M':
    BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
exercise = input('''What is your activity level?:
(1) sedentary (little to no exercise)
(2) lightly active (light exercise/sports 1-2 days a week)
(3) Moderately active (moderate exercise/sports 3-5 days a week)
(4) Very Active (hard exercise/sports 6-7 days a week)
Enter 1, 2, 3, or 4 ''')
exercise = int(exercise.strip())
if exercise == 1:
  TEE = BMR * 1.1
elif exercise == 2:
  TEE = BMR * 1.275
elif exercise == 3:
  TEE = BMR * 1.35
elif exercise == 4:
  TEE = BMR * 1.525

current_BMI = (weight/(height / 100)) / (height / 100)
goal_BMI = (goal_weight/(height / 100)) / (height / 100)

try:
    while True:
        intake = int(input('How many calories do you eat each day? '))

        weight_diff = weight - goal_weight
        daily_deficit = TEE - intake
        cal_in_1kg = 7709
        kg_loss = daily_deficit/cal_in_1kg
        days = weight_diff/kg_loss
        today = datetime.date.today()
        future = today + timedelta(days=days)

        print('--------------START OUTPUT------------------')
        
        print('Your TEE (total energy expenditure) is %s' % (round(TEE)))
        
        if current_BMI >= 25:
            print('You currently have a BMI of', '%.2f' % current_BMI,
                  '. You want to get that sucker under 25. A healthy BMI is between 18 and 25' )
        elif current_BMI < 18:
            print('You currently have a BMI of', '%.2f' % current_BMI,
                  '. You want to get that sucker above 18. A healthy BMI is between 18 and 25')
        elif current_BMI > 18 and current_BMI < 25:
            print('You currently have a BMI of', '%.2f' % current_BMI,
                  '. This is in the healthy range.')
            
        if goal_BMI > 18 and goal_BMI < 25:
            print('Your goal BMI is %s and is in the healthy range' % '%.2f' % goal_BMI)
        elif goal_BMI < 18:
            print('''Your goal BMI is %s and is in the underweight range''' % '%.2f' % goal_BMI)
        print('You will reach your goal weight by %s or %s days or %s weeks or approximately %s months' % (future, round(days), '%.2f' % (days/7), '%.2f' % (days/31)))
        print('This is a daily caloric deficit of %s calories' % (round(daily_deficit)))
        print('--------------END OUTPUT------------------')
        continue
except:
    print('End program')
