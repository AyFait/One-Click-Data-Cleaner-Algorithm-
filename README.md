# One Click Data Cleaner Algorithm (DCA)[^1]

> This code is meant to do your first job for you, if you're about to work on a data processing or analysis task.

## Domain knowledge of your dataset is highly recommended before using this algorithm 
## Assumes that your .CSV[^2] file as a single row of defined header/title (starting point, first row)

---
### Scope: 
- **Takes raw dataset**
- **Goes through each cell, fixing using outlined instruction**
- **Gives back cleaned dataset**

---
### Structure:
- **Fills empty cells using interpolation**
- **Detects categorical columns**
- **Maps non-numerical elements to numbers**
- **Detects alpha-numerical/object-numerical cells**

---
> Some columns might get deleted or "dropped" from the dataset if it does not meet a threshold (which can be changed as dimmed fit), like number of empty cells, number of full "char" cells. Resulting in smaller features in the output dataset.



















[^1]: More than 85% of this program was hand-written by me in 2024, I'll give about 13% to "why is this part not working as expected?" prompts on ChatGPT, and about 2% of ChatGPT writing whole blocks!
[^2]: Only supports .csv files
