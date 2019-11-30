| Data         |Average | Total           | Epsilon                  | Alpha   | Gamma | Obs 
| :-------------:|:----: |:-------------:    | :-------:                  | --------|------ | ----
|  1           | 37.8024|  10.000         |1 - i * (epsilon/total)   |0.1      | 0.9 | Trained during evaluation
|  2           | 28.4874| 50.000         |1 - i * (epsilon/total)   |0.1      | 0.9
|  3 | 20.4303 | 50.000 | 0.1 | 0.1 | 0.9
| 4 | 26.9491 | 50.000 | 1 - i * (epsilon/total) | 0.1 | 0.9
| 5 | 8.7166 | 10.000 | 1 - i*(epsilon/total) | 0.1 | 0.9
| 6 | 50.0794 | 20.000 | 1 - i*(epsilon/total) | 0.1 | 0.9
| 7 | 24.269| 20.000 | 1 - i*(epsilon/total) | 0.1 | 0.9 | Uses timesteps = 1000+1000 (Instead of 200+100)
| 8 | 29.9672 | 20.000 | 1 - i*(epsilon/total) | 0.1 | 0.9 | Updated to ignore the first tail block

----- 
Notes: 
- Average is calculated from 10.000 games using the best possible action for each state.
- Tested on a empty map enclosed by walls.