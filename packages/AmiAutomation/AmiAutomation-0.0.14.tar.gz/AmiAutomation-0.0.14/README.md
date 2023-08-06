# RPH extraction
Contains a tool to read a .rph file into a RphData structure.

#### Usage
A simple example is given below:
```
from AmiAutomation import RphData

data = RphData.rphToDf(path = "path_to_rph_file")

# Table data inside a dataframe
dataframe = data.dataframe
```

# Binaries extraction
This package contains the tools to easily extract binary data from PX3's:
* Heat Log
* 2 Second Log
* Wave Log
* Composite
* Histogram

Into a pandas dataframe for further processing  

#### Usage
Importing a function is done the same way as any python package:

```
from AmiAutomation import PX3_Bin, LogData
```

From there you can call a method with the module prefix:

```
dataFrame = PX3_Bin.file_to_df(path = "C:\\Binaries")
```
or
```
dataFrame = LogData.binFileToDF(path = "C:\\Binaries")
```

#### LogData Methods
You can get Binary log data in a LogData format that contains useful data about the binary file, including samples inside a pandas dataframe

```
from AmiAutomation import LogData

#This returns the whole data
logData = LogData.binFileToDF("bin_file_path.bin")

#To access samples just access the dataframe inside the LogData object
dataFrame = logData.dataFrame 
```

This method can also be used to retrive the data table from inside a ".cpst" or ".hist" file, detection is automatic based on file extension, if none is given, ".bin" is assumed

#### PX3_Bin Methods
This method returns a single pandas dataframe containing extracted data from the provided
    file, path or path with constrained dates 

* **file_to_df ( path, file, start_time, end_time, verbose = False )**

 *  To process a single file you need to provide the absolute path in the file argument

```
dataFrame = PX3_Bin.file_to_df(file = "C:\\Binaries\\20240403T002821Z$-4038953271967.bin")
```

 * To process several files just provide the directory path where the binaries are (binaries inside sub-directories are also included) 

```
dataFrame = PX3_Bin.file_to_df(path = "C:\\Binaries\\")
```

* You can constrain the binaries inside a directory (and sub-directories) by also providing a start-date or both a start date and end date as a python datetime.datetime object

```
import datetime

time = datetime.datetime(2020,2,15,13,30) # February 15th 2020, 1:30 PM

### This returns ALL the data available in the path from the given date to the actual time
dataFrame = PX3_Bin.file_to_df(path = "C:\\Binaries\\", start_time=time)
```

```
import datetime

time_start = datetime.datetime(2020,2,15,13,30) # February 15th 2020, 1:30 PM
time_end = datetime.datetime(2020,2,15,13,45) # February 15th 2020, 1:45 PM

### This returns all the data available in the path from the given 15 minutes
dataFrame = PX3_Bin.file_to_df(path = "C:\\Binaries\\", start_time=time_start, end_time=time_end )
```

#### Tested with package version
* pythonnet 2.5.1
* pandas 1.1.0