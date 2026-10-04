# Polars in FS

1. [Basics of DataFrames](#bodf)
1. [Finding the data you want](#0)
1. [Matplotlib](#plt)
1. [Numpy](#np)

<h2 id="bodf"> Basics of Data Frames </h2>

A concept shared across multiple different data parsing libraries is the ```DataFrame```. It is described in terms of rows and columns. Every column (known in Polars as ```Series```) has a name/id and a datatype (int 32, float 64, string, etc.) and the entire ```DataFrame``` has a number of rows (Each column must have the same # of rows). This looks something like:

<img width="402" height="219" alt="1212" src="https://github.com/user-attachments/assets/f2aca741-bd65-4259-afd8-b1b0dca9a3b5" />


Our data tends to look more like:

<img width="1552" height="330" alt="123" src="https://github.com/user-attachments/assets/2f42ef67-ae7e-45bf-bfb4-9a11191eabe5" />

<h2 id="0"> Finding the data you want </h2>

I will generally refer to dataframes as ```df```.

### Reading files

```python
path = "FS-3/08102025/08102025Endurance1_FirstHalf.parquet" 

# A little tip for windows vscode users: When you select "copy path" on a file it uses  backslashes which you then have to fix. If you instead just copy as if you were going to copy the entire file, and paste it into the editor, it pastes the path with forward slashes!

# Read files with .read_parquet or .read_csv
dfa = pl.read_parquet(path)

# Stack two dataframes vertically (eg. two parts of the same run) with .vstack
df = dfa.vstack(dfb)

# Rename your columns
df.columns = ["altColA", "altColB", . . .]

# Printing your paruqet
print(dfa)

```

### Slicing

```python
df["colA"] # This gets you a specific column or "Series"
df["colA", "colB"] # This gets you a DataFrame with just these two columns
df.select(["colA", "colB"]) # This does the same thing as the line before but is more generalizeable.

df[0] # This gets you the first row as a df
df[:10] # This gets you the first 10 rows as a df

# Unfortunately, polars does not support indexing in reverse so df[-1] returns an error. In it's place you can do:
df[df.height - 1] # Get the last row
```

### Filtering

```python
df.filter(pl.col("colA") == 1) # Returns a df with all the rows where the value of colA is 1.

# To stack these, just call .filter() again!
df.filter(pl.col("Time") > 100).filter(pl.col("Time") < 200) # Get df where the time is between 100 and 200!

# You can also use some other operators like "&" and "|" for "and"/"or"
df.filter((pl.col("Time") > 100) & (pl.col("Time") < 200))
df.filter((pl.col("colA") < 10) | (pl.col("colB") != "hi"))

# There is also some logic for "if" and "else", but it is a bit awkward and uses words like "then" and "otherwise". Look it up if you want to use it and add to this doc because I currently don't have internet to check what it is!
```

### Multi Column or Relative Column Operations

A lovely thing about Polars is how you can perform simple operations between columns quickly!

```python
I = "SME_TEMP_BusCurrent"
V = "SME_TEMP_DC_Bus_V"

# Get the series that is the power value at every moment.
Power = df[I] * df[V]

# Or insert it into the dataframe itself!
df.insert_column(0, df[I] * df[V]) # In place. 0 is the index of where you want the column to end up.
or
df = df.with_columns( # Not in place so you have to set df equal to the result
    (df[I] * df[V]).alias("Power")
)

# You can also perform basic operations on columns or alter them.

df[I] * 40 # returns a Series with all the current values * 40

df = df.with_columns( # Replaces the I column with one that is multiplied by 40.
    df[I] * 40
)
```

### Useful Series Stuff

```python
s = df["colA"]
s.mean() # Mean
s.std() # Standard Deviation
s.min() # Minimum
s.max() # Maximum
s.abs() # Absolute Value (Returns a Series)
s.sqrt() # Square Root (Returns a Series)
s.sample(n = 2, with_replacement = False) # Samples 2 values (Returns a Series)
```

<h2 id="plt"> Matplotlib </h2>
To display parquet data in a more readable way, we use something called matplotlib. It is another helpful python library that we use in FS. You can either set up data manually, or pull from a given file. Here is an example of what a graph with given data would look like: 

```python
import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y, color = 'blue', linestyle = '--')
plt.title("My Matplotlib Plot")
plt.xlabel("X Axis Label")
plt.ylabel("Y Axis Label")
plt.show()
```
Here is what that looks like:

<img width="640" height="480" alt="hi-1" src="https://github.com/user-attachments/assets/f38dcc46-3bd4-49ae-a5d5-b43364008ed2" />


There are multiple different types of plots you can use:
```python
plt.plot() #line chart
plt.scatter() #scatter plot
plt.bar() #bar graph
plt.hist() #histogram
plt.pie() #pie chart
```

Here is an example with a parquet file: 
```python
import polars as pl
import matplotlib.pyplot as plt

df = pl.read_parquet('software-data.parquet') #this uses polars to read the file
plt.plot(df['Time'], df ['VDM_GPS_SPEED'])
plt.show()
```
You can choose which parquet columns to use as your X and Y axis.

<h2 id="np"> Numpy </h2>

Numpy is the python library used for data analysis and heavier math. It lets you complete common math functions on data sets or arrays. Here is a quick look at how NumPy simplifies math compared to a standard Python list:
```python
import numpy as np

python_list = [1, 2, 3]
print(python_list * 2)
# output is [1, 2, 3, 1, 2, 3]

numpy_array = np.array([1, 2, 3])
print(numpy_array * 2)
# output is [2, 4, 6]
```
Some examples of numpys functions:
```python
np.add() 
np.subtract()
np.multiply()
np.divide()
np.sqrt() #takes the sqaure root
np.sin() #there is also cos and tan
np.sum () #calculates the sum of all the elements
np.pi #this is a mathematical constant for PI
np.zeros() #creates a numpy array filled with 0's
np.concatenate() #joins arrays together along an existing axis - the arrays must have the same dimensions
```
There are a lot more numpy functions, but these are the main ones you'll need. This is the [official numpy website](https://numpy.org/doc/stable/reference/), which lists all of their functions.
