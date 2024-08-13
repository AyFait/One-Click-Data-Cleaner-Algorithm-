 


I created this program after working for 3 weeks at a stretch. Yeah, I just started data analysis a few months back, so as of today's date on this README, I'm still a beginner.

For the critics, I'm not trying to impress anyone because the parameters I used may be absurd to you and thereby annoying you. This is actually mainly for my personal use. I just got into Machine Learning fully hands-on and realized trying to clean up my dataset takes almost half of my time and, moreover, it seems repetitive with the same technique and procedure.

Hence this DCA:
> It takes in a CSV file and processes it in these 2 basic steps:

#Check each column:
   1. If it's numerical (int, float), fill in missing cells by interpolation.
   2.  If it's an object:
     - Check if it's categorical. If yes, map to a specific set of defined numbers and fill missing cells.
     - If it is not categorical, analyze to check for the ratio of numbers to other values, delete unwanted values, and fill them back by interpolation.
     - If none of the above checks, delete the column.

Kindly check the parameters, understand the code, and adjust to your taste before use.

Thank you 😊
