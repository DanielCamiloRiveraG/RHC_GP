# RECONSTRUCCION HISTORICA DE CAUDALES - GUATIQUIA PROJECT (RHC_GP)
---

## Descripción

**RHC_GP** es una plaforma de modelación hidrólogica basada en el repositorio **thym** para la reconstrucción histórica de caudales del proyecto de extensión solidaria "Sistema de predicción hidrológica para el análisis de la vulnerabilidad y del riesgo por inundación en la cuenca del Río Guatiquía, Meta, Colombia" de la Universidad Nacional de Colombia, Sede Bogotá.
La plataforma incluye tres diferentes modelos:

1. *GR4J*
2. *HBV*
3. *HYMOD*

Para aprender a usar la plataforma dirijase al título **TROPICAL HYDROLOGICAL MODELLING (THYM) PLATFORM** donde encontrará la estructura del código, compilación, ejecución y graficación e información saobre el modelo de optimimización y calibración usado **The Optimization Software Toolkit for Research Involving Computational Heuristics (OSTRICH)** para obetener los parámetros de los modelos de cada subcuenca.

## Estructura del código

El directorio principal `/RHC_GP` está compuesto por los siguientes directorios y archivos:

1. `/bin`: Contiene el archivo `makefile` y los ejecutables de los modelos tras la compilación. 
2. `/inc`: Contiene todos los archivos de cabecera `*.h`. 
3. `/src`: Contiene todos los archivos de código fuente `*.c`. 
4. `/[modelo]_[subcuenca]`, : Aplicación de un modelo (por ejemplo, GR4J, HBV o HYMOD) a una subcuenca específica. Por ejemplo, `gr4j_S1` contiene los archivos de entrada necesarios para aplicar el modelo GR4J en la subcuenca 1. Este directorio incluye los archivos de entrada correspondientes.
5. `/tools`: Contiene scripts en `python` para el posprocesamiento de los resultados de los modelos:
- El script `plot_boxplots.py` genera gráficos boxplots que representan los regimenes anuales por mes de las series temporales simuladas de caudal por subcuenca.
- El script `plot_subcuencas.py` genera las series temporales de caudales simuladas por subcuenca y modelo usado, agregado a nivel diario, mensual y anual.
- El script `plot_distribuciones.py` genera las distribuciones de probabilidad de las series temporales de cada modelo, por subcuenca.
- El script `procesar_et.py` Procesa la evapotranspiración (et_mm) de 'results.out' para todas las subcuencas y consolida los resultados en tres archivos de acuerdo con la agregación temporal (diaria, mensual y anual): `et_diaria.csv`, `et_mensual.csv` y `et_anual.csv`
- El script `procesar_meteo.py` Procesa las siguientes variables: precipitación (precip), temperatura máxima (tmax), mínima (tmin) y media (tave) de 'meteo.in' para todas las subcuencas y consolida los resultados en tres archivos de acuerdo con la agregación temporal (diaria, mensual y anual) y la variable seleccionada:`variable_diaria.csv`, `variable_mensual.csv` y `variable_anual.csv`.
- El script `procesar_q.py` Procesa el caudal (q_m3s) de 'results.out' para todas las subcuencas y modelos, consolidándolos en tres archivos de acuerdo con la agregación temporal (diario, mensual y anual): `q_diario.csv`, `q_mensual.csv` y `q_anual.csv`.
- El script `plot_in_out.py` genera gráficos de las series temporales simuladas y observadas, así como de las variables presentes en el archivo de entrada `meteo.in`.
6. `/graficas_boxplots`: Contiene las imágenes producidas por el script `plot_boxplots.py`.
7. `/graficas_distribuciones`: Contiene las imágenes producidas por el script `plot_distribuciones.py`.
8. `/graficas_series`: Contiene las imágenes producidas por el script `plot_subcuencas.py`.
9. `/Agregacion_variables`: Contiene los resultados del ensamble de modelos producidos por los scripts `procesar_et.py`, `procesar_meteo.py` y `procesar_q.py`.

## Ensamble de modelos
Posterior a la simulación de todos los casos de estudio:
1. Ir a `/tools`.
2. Ejecutar los siguientes scripts:

### procesar_et.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y el modelo GR4J, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__` y si se quieren obetener los resultados de otras carpetas diferentes al modelo GR4J se debe modificar la variable `results_path` dentro de la función `process_et`.
El modo de uso del script es el siguiente: `./procesar_et.py /ruta/a/RHC_GP`, siendo `/ruta/a/RHC_GP` la ruta base del repositorio donde se tienen las carpetas del caso de estudio.

### procesar_meteo.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y el modelo GR4J, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__` y si se quieren obetener los resultados de otras carpetas diferentes al modelo GR4J se debe especificar el modelo en la línea de código de ejecución.
El modo de uso del script es el siguiente: `./procesar_meteo.py /ruta/a/RHC_GP [variable] [modelo]`. Si no se especifica nada en modelo, el código escogerá automáticamente GR4J y si no se colocá la variable se seleccionará la precipitación (precip).

### procesar_q.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y todos los modelos, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__`.
El modo de uso del script es el siguiente: `./procesar_q.py /ruta/a/RHC_GP`.

## Graficación
1. Ir a `/tools`.
2. Ejecutar los siguientes scripts:

### plot_boxplots.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y todos los modelos, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__`.
El modo de uso del script es el siguiente: `./plot_boxplots.py /ruta/a/RHC_GP`.

### plot_subcuencas.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y todos los modelos, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__`.
El modo de uso del script es el siguiente: `./plot_subcuencas.py /ruta/a/RHC_GP`.

### plot_distribuciones.py
Este script está automatizado para procesar las 6 subcuencas identificadas en la cuenca del Río Guatiquía y todos los modelos, por lo cual, si se desea añadir más o menos subcuencas se debe modificar la función `__init__`.
El modo de uso del script es el siguiente: `./plot_distribuciones.py /ruta/a/RHC_GP`.

# TROPICAL HYDROLOGICAL MODELLING (THYM) PLATFORM
---

## Description

**thym** is hydrological modelling platform  designed to analyse hydrological processes in tropical basins using *aggregate rainfall-runoff conceptual models*. So far, the platforms includes three different well known models:

1. *GR4J*
2. *HBV*
3. *HYMOD*

These models run at *daily time steps* and are able to estimate daily runoff at the basin outlet.

**thym** is programmed in `C` language, and the pre- and postprocessing of model information is performed in `python`.

## Code structure

The main directory `/thym` is composed by the following directories and files:

1. `/bin`: Has the `makefile` and the model executables after compilation.
2. `/inc`: Has all the  headers `*.h` files.
3. `/src`: Has all the source code `*.c` files.
4. `/test_[model]`, : Application of a model (e.g. `GR4J`, `HBV` or `HYMOD`) to test case. For instance, `test_gr4j` contain the input files needed to apply the `GR4J` model.  This directory contains the input files:
5. `/tools`: Has `python` scripts for model result postprocessing. The `plot_in_out.py` script plots simulated and observed time series and the variables in `meteo.in` input file. 

### `ctrl.in` file
This is the control or steering file for **thym**. This file has the following structure:

|ROW|MEANING|
|--------|---------------------------------------------------------|
| row 1  | Watershed name and hydrometric station                  |
| row 2  | Outlet latitude [dec]                                   |
| row 3  | Outlet longitude [dec]                                  |
| row 4  | Outlet altitude in [m.a.s.l]                            |
| row 5  | Watershed area in [km^2]                                |
| row 6  | Starting time (yyyy mm dd hr[0 23] min[0 59] sec[0 59]) |
| row 7  | End time (yyyy mm dd hr[0 23] min[0 59] sec[0 59])      |
| row 8  | Time step (s)                                           |
| row 9  |                                                         |
| row 10 | PET method ['obs', 'hamon0', 'hamon1', 'pen-mon']     |
| row 11 | [Albedo] [wind speeed altitute (usually 10 m overgr.)]  |
| row 12 |                                                         |
| row 13 | Model's name ['gr4j' 'hbv' 'hymod']                     |
| row 14 | Model's parameters                                      |


Note that:
- In *row 10*: The user can chose the method to estimated the daily *potential evapotranspiration* among the following options: *obs* [observed precomputed values introduced through the `meteo.in` file], *hamon0* [Hamon method version 0], *hamon1* [Hamon method version 1 (more standard)] and *pen-mon* [Penman-Monteith method].  

- In *row 14*: This row contains the parameters corresponding to the model in *row 15*. According to the model, the parameters are as follow:

#### GR4J

|COL|PARAMETER|MEANING|RANGE|
|--------|--------|--------------------------------------------------------------------|----------|
| col 1  | x1     | Maximum capacity of the production store [mm]                      |100; 1200 |
| col 2  | x2     | Groundwater recharge coefficient                                   |-5; 3     |
| col 3  | x3     | One-day ahead maximun capacity of the routing store [mm]           |20; 300   |
| col 4  | x4     | Time base of unit hydrograph UH1                                   |1.1; 2.9  |
| col 5  | pa     | % of effective precipitation routed by UH1                         |0.9       |
| col 6  | pb     | % of effective precipitation routed by UH2                         |0.1       |
| col 7  | trs    | Air temperature above which the precipitation is all rainfall [oC] |-         |
| col 8  | tmlt   | The base temperature above which snow melt is allowed [oC]         |-         |
| col 9  | sno50  | The depth of snow when the basin is 50% covered by snow [mm]       |-         |
| col 10  | sno100 | The shreshold depth of snow, above which there is 100% cover [mm] |-         |
| col 11  | ls     | Snow temperature lag factor                                       |-         |
| col 12 | bmlt6  | Melt factor on June 21 [mm H2O/day-oC]                             |-         |
| col 13 | bmlt12 | Melt factor on December 21 [mm H2O/day-oC]                         |-         |
 
Note that the parameters *x1*, *x2*, *x3* and *x4* are often subjected to calibration. The parameters *pa* and *pb* take constant values. The others parameters belong to the *snow model* and are not relevant in tropical basins modelling.

#### HBV

|COL|PARAMETER|MEANING|RANGE|
|--------|--------|-------------------------------------------------------|----------|
| col 1  | k2     | Withdrawal rate from deep layer [days]                |10; 20000 |
| col 2  | k1     | Withdrawal rate for shallow layer overflow [days]     |1; 100    |
| col 3  | k0     | Withdrawal rate from shallow layer (interflow) [days] |0.5; 20   |
| col 4  | degd   | Degree day factor (snowmelt rate) [mm/day oC]         |0; 20     |
| col 5  | degw   | Base temperature above which melt occur [oC]          |-3; 3     |
| col 6  | ttlim  | Temperature threshold below which freezing occurs [oC]|-3; 3     |
| col 7  | perc   | Percolation rate into deep layer [mm/day]             |0; 100    | 
| col 8  | beta   | Distribution of soil stores [-]                       |0; 7      |
| col 9  | lp     | Limiting soil moisture at which PET takes place [-]   |0.3; 1    |
| col 10 | fcap   | Maximum soil moisture storage [mm]                    |10; 2000  |
| col 11 | hl1    | Maximum shallow layer storage [mm]                    |0; 100    |
| col 12 | maxbas | Length of hydrograph routing transformation [hour]    |24; 120   |


#### HYMOD

|COL|PARAMETER|MEANING|RANGE|
|--------|-------|------------------------------------------------|----------------------|
| col 1  | ks    | Slowflow routing tank's rate parameter         |0; 1                  |
| col 2  | kq    | Quickflow routing tanks' rate parameter        |0; 1                  |
| col 3  | ddf   | Degree day factor                              |0; 2                  |
| col 4  | tb    | Base temperature to calculate melt             |-5; 5                 |
| col 5  | tth   | Temperature threshold                          |-5; 5                 |
| col 6  | alpha | Quick/slow split parameter                     |0; 1                  |
| col 7  | b     | Scaled distribution function shape parameter   |0; 2                  |
| col 8  | huz   | Maximum height of soil moisture accounting tank|0; Inf                |
| col 9  | nq    | Number of quickflow routing tanks              |1; Inf (typically < 3)|
| col 10 | kv    | Vegetation adjustment to PE                    |0; 2                  |

### `meteo.in` file 
This file contains the *meterological data* recorded within the catchment. This file has the following columns:

| datetime            | tave_oC | tmin_oC | tmax_oC | precip_mm | windv_m/s | evapt_mm | runoff_mm |
|---------------------|---------|---------|---------|-----------|-----------|----------|-----------|
| 1981-01-01 00:00:00 | -3.5    | 0.0     | 0.0     | 7.21      | 0.0       | 0.0      | 1.0502    |
| ...                 | ...     | ...     | ...     | ...       | ...       |...       | ...       |

where:

- *datetime*: Date time following the format: *YYYY-MM-DD HH:MM:SS*
- *tave_oC*: Daily average air temperature [$^oC$].
- *tmin_oC*: Daily minimum air temperature [$^oC$].
- *tmax_oC*: Daily maximum air temperature [$^oC$].
- *precip_mm*: Daily precipitation [$mm$].
- *windv_m/s*: Daily daily wind speed [$mm$]. Used to estimate potential evapotranspiration using, for instance, Penman-Monteith method. Note that the altitude at which *windv* is measured is indicated at row 11 in `ctrl.in` file. Set this column to 0.0 is not needed by the evapotranspiration method. 
- *evapt_mm*: Daily observed potential evapotranspiration [$mm$]. Optionally, this can be calculated within the model (see `ctrl.in` file) using different methods. If the *evapotranspiration* is calculated within the model, this column can be equal to 0. 
- *runoff_mm*: Daily runoff at the outlet of the basin [$mm$].

and the output file:

### `results.out` file 
This file is composed by columns that records the values of *state variables* and *flux variables* for each simulated day. The variables (columns) are different for each model. Note that the most relevant variable, the *total catchment runoff* is called *q_mm* for any model and is given in *mm*. 

### `diagnostic.out`
This file contains some statistics to assess the model performance based on the simulated (*q_mm* in `results.out`) and the observed runoff (*runoff_mm* in `meteo.in`). The file has the following structure: *<STAT>,<VAL>*. Below are the estimated *STAT*s:

- *NSE*: Nash-Sutcliffe efficiency
- *LNSE*: Log Nash-Sutcliffe efficiency
- *RMSE*: Root-mean-squared error
- *PBIAS*: Percentage bias
- *ABSER*: Average absolute error
- *ABSMAXER*: Maximum absolute error
- *PDIFF*: Peak difference
- *ERCOR*: Correlation of error
- *NSC*: Number of sign changes

## Compilation, execution and plotting

### Compilation

1. Go to '/bin'. 
2. Type `make clean` this will remove `*.o` files and the executable (optional).
3. Within `makefile` change the variable `MODEL`. So if:
    - `MODEL=1` compilation is performed for *GR4J* model
    - `MODEL=2` compilation is performed for *HBV* model
    - `MODEL=3` compilation is performed for *HYMOD* model
4. Type `make`. This will execute the `makefile` and create `thym_[model]` (e.g `thym_gr4j`) (*model executable*) and a *symboly link* to the executable within the main dir `/thym`.

### Execution
1. Go to the root dir `/thym`.
2. Type `./thym_[model] testcase`, so for instance `thym_gr4j test_gr4j`. This will run *GR4J* model for the *test_gr4j* study case. If the model execution is succesfull, the model will log results in the file `results.out` saved within *testcase* directory (e.g. `/test_gr4j`).


### Plotting
1. Go to `/tools`
2. Type `./plot_in_out.py ../testcase`, so for instance `./plot_in_out.py ../test_gr4j`. `plot_in_out.py` will plot time series of *simulated* (*q_mm* variable in the `results.out` output file) and *observed* (*runoff_mm* variable in the `meteo.in` input file) runoff in *mm*. The script will plot also all the variables in `meteo.in` file. 

Note that *compilation, execution and plotting* can be performed all at once using the `run.sh` in `/thym` root dir typing `./run.sh testcase valgrind` (e.g. `./run.sh test_gr4j yes`). Every step is performed as long as: `COMP=true EXEC=true  PLOT=true`. Note that `valgrind` can be `yes` or something else. *valgrind=yes* the model is ran and memory leaks are checked. The option `yes` must be chosen when  new developments are added to the model and memory leaks need to be checked.


## Calibration and optimization with OSTRICH

### **Ostrich** features
- Perform calibration and optimization of environmental models. Ideally, models must:
    - use a text-based input/output file format. However, **Ostrich** can work with models that use **MS Acces** or **NetCDF** file formats if the **Ostrich** is configured accordingly (see `Type Conversions`), 
    - run without prompting for user intervention,
    - produce outputs that can be reliably parsed.


- Implement multiple *deterministic*, *heuristic* and *smaplers* algorithms (see table 1 in the user's manual). For instance, while the *Levenberg-Marquardt* algorithm is tailored to non-linear calibration problems, the *Pareto Archive Dynamically Dimensioned Search* and the *Simple Multi-Objective Optimization Test Heuristic* are suitable for multi-objective optimization or multi-criteria calibration. Additionaly, sampling-based algorithm such as *Generalized Likelihood Uncertainty Estimation*, *Rejection Sampling* and *Metropolis-Hastings Markov Chain Monte Carlo* are based for uncertainty-based calibration. 
- Estimate multiple *regression statistics and diagnostics* when used for model calibration via a *weighted sum of squared errors* approach (see table 2 in the user's manual).

### Input files
**Ostrich** requires to set up the `ostIn.txt` input file and to create *template model input files*.   

#### The `ostIn.txt` input file 
The following briefly explain the groups that form the input file. Note that with few exceptions, the format for a line of input in the file is `<variable> <value>`.
1. *basic configuration group*: Some of the configuration variables are mandatory and is the only one group that does not need a `Begin...` and `End...` group tags. This means that this group variables can be placed anywhere within the file. The configuration variables are:
- `ProgramType`: Indicate the algorithm to be used to perform calibration or optimization.
- `ModelExecutable`: Indicate the name and path of model executable. 
- `ModelSubdir`: When running in parallel, a working subdirectory must be especified to prevent parallel runs from clobbering each other's input and output files.
- `ObjectiveFunction`: Objective function to be optimized, either `WSSE` (Weighted Sum of Square Errors) calibration or `GCOP` (General-purpose Constrained Optimization Platform).
- `PreserveBestModel`: A user supply script that is run by **Ostrich** every time a new best parameter set is discovered. 
- `PreserveModelOutput`: If `yes`, **Ostrich** will make copies of files associated with each model run and preserved files will be stored in directories named `runNNN` when `NNN` is a counter that increases after each model run. Alternatively, users can provide the name of a script that will run to preserve certain model run information. **Ostrich** will pass some argument to the user-defined script (see section 2.3 of user's manual). 
- `OstrichWarmStart`: If set to `yes`, **Ostrich** will read the contents of any previously created `OstModel` output files and use the entries therein to restart the optimization or calibration exercise. 
- `NumDigitsOfPrecision`: Specifies the precision of values written by **Ostrich** output files.
- `TelescopingStrategy`: If selected (see listing 3 in user's manual) **Ostrich** will cause parameter bounds to become increasingly smaller as an optimization or calibration proceeds.
- `RandomSeed`: Used to control the random seed when generating random numbers.
- `OnObsError`: Used to control how **Ostrich** behaves when a model fails to generate all of the expected output for a `WSSE` calibration. If equal to `quit`, **Ostrich** will abort if it ever fails to parse an observation from user-specified output files. If set to a value, **Ostrich** will use the value as a placeholder observation value.
- `CheckSensitivities`: If it is set to `yes`, **Ostrich** will perform a pre-calibration step to calculate parameter sensitivies. 
- `SuperMUSE`: If it is set to `yes`, **Ostrich** will interface with **EPA** SuperMUSE tasker-client approach to parallel computing.
- `OstrichCatching`: If it is set to `yes`, **Ostrich** will examine `OstModel` output files prior to running a model configuration to see if the parameter set has already been evaluated.- `BoxCoxTransformation`: If set to a value other than `1`, **Ostrich** will apply a *Box-Cox* power transformation on each calibration residual. The value is used as the exponent for the transformation.
- `ModelOutputRedirectionFile`: This variable allows users to override the default name (i.e. `OstExeOut.txt`) of the file where **Ostrich** will redirect model output that would normally be displayed on a console screen. 

2. *file pairs group*: A file pair consist of a *template file* and a corresponding *input file*. The contents of the *template file* should be identical to the paired model *input file* except that values of optimization (or calibration) parameters are placed placed with unique parameter names defined in the *Parameter section*. During **Ostrich** execution, this will use the *template files* to create syntactically correct model *input files* in preparation of running model at different parameter values. `BeginFilePairs` and `EndFilePairs` are parsing tags to define this group. Pairs are introduced as `<template1><sep><inputfile1>`.

3. *extra files group*: Extra files are model input files not used by **Ostrich**, but required for proper execution of the model. `BeginExtraFiles` and `EndExtraFiles` are parsing tags to define this group. Files are introduced as `<otherinputfile1>`.

4. *extra directories group*: Extra directories are directories containing model input files not used by **Ostric**, but required for proper execution of the mode. `BeginExtraDirs` and `EndExtraDirs` are parsing tags to define this group. Directories are introduced as `<inputdir1>`.

5. *real-value parameters group*: This configuration group describes the parameters to be calibrated or optimized. `BeginParams` and `EndParams` are parsing tags to define this group. Parameters are introduced as `<parameter_name1> <initial_value1> <lower_bound1> <upper_bound1> <input_transf1> <ostrich_transf1> <output_transf1> <format1>`. Transformation can take the following values: `none`, `log10` and `ln`. The format value is used to write into model input file following an specific format required by model. 

6. *integer-value parameters group*: This configuration group describes the parameters to be calibrated or optimized that can take only integer values.  `BeginIntegerParams` and `EndIntegerParams` are parsing tags to define this group. Parameters are introduced as `<parameter_name1> <initial_value1> <lower_bound1> <upper_bound1>`.

7. *combinatorial parameters group*: This configuration group describes the parameters to be calibrated or optimized that can take on a discrete set of real, integer or string values.  `BeginCombinatorialParams` and `EndCombinatorialParams` are parsing tags to define this group. Parameters are introduced as `<parameter_name1> <type1> <initial_value1> <value1> <value2> ... <valuen>`. `type` can be either `real`, `integer` or `string`.

8. *tied parameters group*: This configuration group describes the parameters which are computed as a function of integer, real of combinatorial parameter values. They may also be functions of other tied parameters.  `BeginTiedParams` and `EndTiedParams` are parsing tags to define this group. Parameters are introduced as `<parameter_name1> <number_of_param1> <pname1> <pname2> ... <pnamen> <type1> <type2> ... <type_data>`. `type` is the type of functional relationship and can be either `linear`, `exp`, `log`, `dist`, `wsum`, `ratio` or `constant`. `type_data` depends of the function `type` and on the `number_of_param`.

9. *special parameters (pre-emption) group*: This configuration group describes the special parameters that are cost and constrain thresholds that are tracked by selected algorithms.  `BeginSpecialParams` and `EndSpecialParams` are parsing tags to define this group. Parameters are introduced as `<parameter_name1> <initial_value1> <type1> <con_type1> <con_name1>`. `type` is the type of pre-emption parameter: `BestCost` or `BestConstraint`. `con_type` can be `upper` or `lower` if `type` is `BestConstraint`. `con_name` is the name of the constraint which are defined in the *constraints group*.

10. *initial parameters group*: This configuration group describes initial parameter set that allow to introduce prior information (such as previous optimization results) improving the process.  `BeginInitParams` and `EndInitParams` are parsing tags to define this group. Parameters are introduced as `<p1,1> <p2,1> ... <pn,1<`. In `pi,j` *j* is the j-initial value of the parameter *i*. Note that this set up must follow the order in the *parameters group*. 

11. *parameters correction group*: This configuration group allow users to interface **Ostrich** with an external program or script that makes adjustments to a candidate parameter set that has been calculated by **Ostrich** but not yet evaluated.  `BeginParameterCorrection` and `EndParameterCorrection` are parsing tags to define this group. `BeginCorrections` and `EndCorrections` are tags to define the parameter corrections. 

12. *observations group*: This configuration group allow users to list the observations names, values and weights, along with parsing instructions to reading simulated equivalent observations from model output files.  `BeginObservations` and `EndObservations` are parsing tags to define this group. This file is set up as `<name1> <value1> <wgt1> <file1> <sep1> <key1> <line1> <col1> <tok1> <aug1> <grp1>`. 

13. *response variables group*: This configuration group allow users to define the response variables when performing optimization. **Ostrich** will read the response variable from model output files prior to evaluating costs and constraints.  `BeginResponseVars` and `EndResponseVars` are parsing tags to define this group. 

14. *tied-response variables group*: This configuration group allow users to define tied-response variables which are variables whose values are computed by **Ostrich** as function of one or more response variables and/or parameters. `BeginTiedResVars` and `EndTiedResVars` are parsing tags to define this group.  

15. *type conversion group*: Models that generate input or output files in *MS Access* or *netcdf* format can be interfaced with  **Ostrich** via specification of a corresponding `TypeConversion` group. Outputs specified in the `TypeConversion` group are extracted into text-based files that can then be processed into observations (see Observation group) or Response Variables (see Response Variables group). `BeginTypeConversion` and `EndTypeConversion` are parsing tags to define this group.   

16. *search algorithms group*: Each algorithm (see table 1 in user's manual) has its own configuration group, wherein the users can specify the values for various algorithm control variables. Additional optional configuration variables and groups such as *warm start*, *pre-emption*, *parameter correction*, *list of initial parameters*, *math and stats* and *line search*, may also be available for a given algorithm. 

17. *uncertainty-based search algorithms group*: Several of the search algorithms implemented in **Ostrich** are designed to enumerate parameter probability distributions or behavioral parameter sets. Such algorithms are referred to as being *uncertainty-based* since they are not just concerned with identifying a single globally optimal parameter set. Each algorithm (see table 1 in user's manual) has its own configuration group. 

18. *multi-objective search algorithms group*: These algorithms seek to identify non-dominated solutions representing the trade-off curve (i.e. pareto front) among conflicting objectives. These objectives can reflect a multi-criteria calibration exercise or a multi-objective optimization problem. 

19. *math and stats group*: These group describes the *finite difference method* employed by algorithms (see table 1 in user's manual). If calibration is performed, additional variables in this group are used to request various statistical and diagnostic output. `BeginMathAndStats` and `EndMathAndStats` are parsing tags to define this group.   

20. *line search group*: This group is used for configuration of the one-dimensional search algorithm that underlines unconstrained numerical optimization procedure (see table no. 1 in user's manual). `Begin1dSearch` and `End1dSearch` are parsing tags to define this group.   

21. *general-purpose constrained optimization platform (GCOP) group*: In this group users can specify the *response variable* (or variables if performing multiobjective optimization or multi-criteria calibration) that will serve as the *cost function* (or functions) for general constrained optimization platform. Each *cost function* identifies a single response variable or tied response variable that represents a *system cost* to be minimized by the optimizer. The overall *GCOP* objective is a combination of the *system cost* and a *penalty function*, which accounts for the cost of all constraint violations.`Begin1dSearch` and `End1dSearch` are parsing tags to define this group.    


22. *constraints group*: In this group the user supplies information about various constraints that are to be placed on a general constrained optimization problem. Any number and combination of constraints are supported.  `BeginConstraints` and `EndConstraints` are parsing tags to define this group.   

### Running **Ostrich**
**Ostrich** can run in *serial* or *parallel* mode. The **Ostrich** executable, `Ostrich` in **Linux**, must be in a directory along with `ostIn.txt`, model *template files* and the *extra model input files*. Remember that **Ostrich** uses the model *template files* to create model input files. The fundamental setup of `ostIn.txt` for:

1. Weighted Sum of Squared Errors (WSSE) Calibration: Several groups and variables must be setup in the `ostIn.txt` including `ObjectiveFunction` (set to `WSSE`), `ProgramType`, `ModelExecutable`, `FilePairs`, `Parameters`, `Observations` and `MathAndStats`. 

2. General Constrained Optimization Platform (GCOP): Several groups and variables must be setup in the `ostIn.txt` including `ObjectiveFunction` (set to `GCOP`), `ProgramType`, `ModelExecutable`, `FilePairs`, `Parameters`, `ResponseVariables`,  `GCOP` and `Constraints`. 

To run in *serial* mode in **Linux**:

    `<path>/Ostrich`

To run in multi-core *parallel* model in **Linux**:


    `mpirun -n 12 <path>/Ostrich`

where `mpirun` is a launcher provided by **MPI** libraries and `-n 12` is an `mpirun` argument that indicates the number of processors (12) used to run `Ostrich`. If `Ostrich` want to be run across multiple nodes (like in a *HPC* infrastructure), other arguments like `-hostfile` and `-rankfile` might be needed. 

**Ostrich** execution can be aborted after creating the file `OstQuit.txt`.

Certain search **Ostrich** algorithms allow an *warm start* and can be restarted from previous runs upon the variable `OstrichWarmStart` is set to `yes` in `OstIn.txt`.

### **Ostrich** output files
Upon completion, **Ostrich** will generated several files. If executed in parallel mode, each processor will create its own set of output files, where `N` indicate the processor id. In serial mode, `N=0`, the id of the master core. The files created are:

1. `OstOutputN.txt`: The main output file, it contains an optimization (or regression) record along with statistical output.
2. `OstErrorsN.txt`: Any errors or warning encountered by processors `N`.  
3. `OstModelN.txt`: A sequential record of every model run evaluated by processor `N`.
4. `OstExeOut.txt`: The standard output and errors of the model runs are directed to this file. 
5. `OstStatusN.txt`: This file is periodically updated with the current progress of the selected search algorithm.
6. `OstGcopOut`: This file keeps track of the cost and constraint information for each model evaluation when the `GCOP` is used.  
7. `OstNonDomSolutions`: When a multi-objective search is performed, this file is periodically updated with the current list of non-dominated solutions that have been discovered by the selected search algorithm. 


### General steps to execute **Ostrich**
The following are some simple steps to use **Ostrich** for model calibration.

1. Download and compile [Ostrich](https://www.civil.uwaterloo.ca/envmodelling/Ostrich.html).

2. In `/thym` create a `testcase_ostr` (e.g. `test_gr4j_ostr`) directory. This directory serve to implement **Ostrich**.

3. Copy **Ostrich** executables within `testcase_ostr` o create a *symboly link* of the executable within `testcase_ostr` directory.
- `Ostrich` is the **Linux** executable for *serial* implementation. 
- `OstrichMPI` is the **Linux** executable for *parallel* implementation. You need to have **MPI** libraries installed. 

4. Create a `model` directory. This directory must contains the *model executable* (e.g. `thym_gr4j`) and model *input files* (e.g `test_gr4j/ctrl.in`). Model *output files* are saved within `model` following the model functioning. You can copy the *model executable* or create a *symboly link* to the executable in the `model` directory. 

5. Set up the *template* control model file. In this case, this file is `ctrl.in.tpl`. In this file, one needs to show which are the parameters aim to be calibrated, this is done by replacing parameter values for *parameter names* (e.g `par_x1`). Note that this *parameter names* are listed in the **Ostrich** control file `ostIn.txt` between `BeginParams` and `EndParams`.

6. Set up the script to execute the model (e.g `ost_thym_gr4j.sh`). The script name is included in `ostIn.txt` (see `ModelExecutable`). Note that **Ostrich** will launch it to run the model every time the parameter set changes. 

7. (optional) Set up an script to save the *best* simulation, (e.g. `save_best.sh`).The script name is included in `ostIn.txt` (see `PreserveBestModel`). This script will create a `best` directory within `ModelSubdir` (see `ostIn.txt`). This script will save the best model output files and model diagnostics. 

8. Edit `ostIn_Serial.txt` or `ostIn_Parallel.txt` eithe you want to run in serial or parallel mode. This is **Ostrich** control file, it is `ostIn.txt`, actually. It is important to read **Ostrich** [user's manual](https://www.civil.uwaterloo.ca/envmodelling/Ostrich.html) to understand the structure of the file.  

9. Run **Ostrich** using `run_ost.sh`. This script will:

    1. Clean up the current directory of **Ostrich** output files from previous runs. 
    2. Create the `model` dir if not exist and create the model input dir in it including a link to model executable.
    3. Copy `ostIn_Serial.txt` into `ostIn.txt` or `ostIn_Parallel.txt` into `ostIn.txt`
    4. Run **Ostrich** in serial or parallel mode. Note that in each iteration **Ostrich** will use the template `ctrl.in.tpl` file to change the `ctrl.in` file. 

