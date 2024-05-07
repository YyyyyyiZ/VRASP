# VRASP
**Vehicle Routing and Appointment Scheduling Problem(VRASP)** with stochastic traveling and service time. 
Use **Sample Average Approxiamation(SAA)** to transform the stochastic problem into a deterministic one.
Contain both **CPLEX 12.9** and **Variable Neighorhood Search(VNS)** impementation.
# Dependencies
```
Anaconda Python 3.7
cplex 12.10
docplex 2.11
numpy 1.21.6
pandas 1.3.5
scipy 1.7.3
```
# Files
* .\experiemnt: data for computational experiments
  * problem size--[5, 10, 20, 30, 40]
  * number of instances--20
  * nunber of samples in SAA implementation--[30, 50, 80, 100]
* .\utils\data_model: Class
* .\utils\gen_data: generate experiment data, save them into .txt file
* .\utils\readwrite: load the experiment data
* .\vns_de: VNS algorithm for deterministic VRASP
* .\vns_saa: VNS algorithm for stochastic VRASP using SAA
* .\cplex_solver: CPLEX implementation for both deterministic and stochastic VRASP
* .\vns_main: VNS runner
