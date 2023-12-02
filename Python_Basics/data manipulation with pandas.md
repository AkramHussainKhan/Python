## Group by

* Calculate the total weekly_sales over the whole dataset.
* Subset for type "A" stores, and calculate their total weekly sales.
* Do the same for type "B" and type "C" stores.
* Combine the A/B/C results into a list, and divide by sales_all to get the proportion of sales by type.

```python
# Calc total weekly sales
sales_all = sales["weekly_sales"].sum()

# Subset for type A stores, calc total weekly sales
sales_A = sales[sales["type"] == "A"]["weekly_sales"].sum()

# Subset for type B stores, calc total weekly sales
sales_B = sales[sales["type"] == "B"]["weekly_sales"].sum()

# Subset for type C stores, calc total weekly sales
sales_C = sales[sales["type"] == "C"]["weekly_sales"].sum()

# Get proportion for each type
sales_propn_by_type = [sales_A, sales_B, sales_C] / sales_all
print(sales_propn_by_type)
```
Now we will do the same using group by:

```python
# Group by type; calc total weekly sales
sales_by_type = sales.groupby("type")["weekly_sales"].sum()
sum(sales_by_type)
# Get proportion for each type
sales_propn_by_type = sales_by_type / sum(sales_by_type)
print(sales_propn_by_type)
```
We can also groupby with more than one variable. such as :

```python
# Group by type and is_holiday; calc total weekly sales
sales_by_type_is_holiday = sales.groupby(["type", "is_holiday"])["weekly_sales"].sum()
print(sales_by_type_is_holiday)
```

Get the min, max, mean, and median of weekly_sales for each store type using .groupby() and .agg(). Store this as sales_stats. Make sure to use numpy functions!

Get the min, max, mean, and median of unemployment and fuel_price_usd_per_l for each store type. Store this as unemp_fuel_stats.

```python
# Import numpy with the alias np
import numpy as np

# For each store type, aggregate weekly_sales: get min, max, mean, and median
sales_stats = sales.groupby("type")["weekly_sales"].agg([np.min,np.max, np.mean, np.median])

# Print sales_stats
print(sales_stats)

# For each store type, aggregate unemployment and fuel_price_usd_per_l: get min, max, mean, and median
unemp_fuel_stats = sales.groupby("type")[["unemployment", "fuel_price_usd_per_l"]].agg([np.min,np.max, np.mean, np.median])

# Print unemp_fuel_stats
print(unemp_fuel_stats)
```
## Pivot table

It is an alternative of groupby.

* Get the mean weekly_sales by type using .pivot_table() and store as mean_sales_by_type.

```python
# Pivot for mean weekly_sales for each store type
mean_sales_by_type = sales.pivot_table(index = "type", values = "weekly_sales")
# Print mean_sales_by_type
print(mean_sales_by_type)
```

* Get the mean and median (using NumPy functions) of weekly_sales by type using .pivot_table() and store as mean_med_sales_by_type.

```python
# Import NumPy as np
import numpy as np

# Pivot for mean and median weekly_sales for each store type
mean_med_sales_by_type = sales.pivot_table(index = "type", values = "weekly_sales", aggfunc = [np.mean, np.median])
# Print mean_med_sales_by_type
print(mean_med_sales_by_type)
``` 

* Get the mean of weekly_sales by type and is_holiday using .pivot_table() and store as mean_sales_by_type_holiday.

```python
# Pivot for mean weekly_sales by store type and holiday 
mean_sales_by_type_holiday = sales.pivot_table(index = "type", values = "weekly_sales", columns= "is_holiday")

# Print mean_sales_by_type_holiday
print(mean_sales_by_type_holiday)
``` 
* Print the mean weekly_sales by department and type, filling in any missing values with 0.
```python
# Print mean weekly_sales by department and type; fill missing values with 0
print(sales.pivot_table(index = "type", columns = "department", values = "weekly_sales", fill_value = 0))
```
* Print the mean weekly_sales by department and type, filling in any missing values with 0 and summing all rows and columns.
```python
# Print the mean weekly_sales by department and type; fill missing values with 0s; sum all rows and cols
print(sales.pivot_table(values="weekly_sales", index="department", columns="type", fill_value = 0, margins = True))
```
## Subsetting with .loc[]
The killer feature for indexes is .loc[]: a subsetting method that accepts index values. When you pass it a single argument, it will take a subset of rows.
The code for subsetting using .loc[] can be easier to read than standard square bracket subsetting, which can make your code less burdensome to maintain.

* Create a list called cities that contains "Moscow" and "Saint Petersburg".
* Use [] subsetting to filter temperatures for rows where the city column takes a value in the cities list.
* Use .loc[] subsetting to filter temperatures_ind for rows where the city is in the cities list.

```python
# Make a list of cities to subset on
cities = ["Moscow", "Saint Petersburg"]
# Subset temperatures using square brackets
print(temperatures[temperatures['city'].isin(cities)])
# Subset temperatures_ind using .loc[]
print(temperatures_ind.loc[cities])
```
### Setting multi-level indexes
Indexes can also be made out of multiple columns, forming a multi-level index (sometimes called a hierarchical index). There is a trade-off to using these.
The benefit is that multi-level indexes make it more natural to reason about nested categorical variables. For example, in a clinical trial, you might have control and treatment groups. Then each test subject belongs to one or another group, and we can say that a test subject is nested inside the treatment group. Similarly, in the temperature dataset, the city is located in the country, so we can say a city is nested inside the country.

* Set the index of temperatures to the "country" and "city" columns, and assign this to temperatures_ind.
* Specify two country/city pairs to keep: "Brazil"/"Rio De Janeiro" and "Pakistan"/"Lahore", assigning to rows_to_keep.
* Print and subset temperatures_ind for rows_to_keep using .loc[].

```python
# Index temperatures by country & city
temperatures_ind = temperatures.set_index(['country','city'])
# List of tuples: Brazil, Rio De Janeiro & Pakistan, Lahore
rows_to_keep = [("Brazil","Rio De Janeiro"),("Pakistan","Lahore")]
# Subset for rows to keep
print(temperatures_ind.loc[rows_to_keep])
```

### Sorting by index values
Previously, you changed the order of the rows in a DataFrame by calling .sort_values(). It's also useful to be able to sort by elements in the index. For this, you need to use .sort_index().
* Sort temperatures_ind by the index values.
* Sort temperatures_ind by the index values at the "city" level.
* Sort temperatures_ind by ascending country then descending city.

```python
# Sort temperatures_ind by index values
print(temperatures_ind.sort_index())
# Sort temperatures_ind by index values at the city level
print(temperatures_ind.sort_index(level='city'))
# Sort temperatures_ind by country then descending city
print(temperatures_ind.sort_index(level=['country','city'],ascending = [True, False]))
```


#############
### Slicing index values
Slicing lets you select consecutive elements of an object using first:last syntax. DataFrames can be sliced by index values or by row/column number; we'll start with the first case. This involves slicing inside the .loc[] method.


* Sort the index of temperatures_ind.
* Use slicing with .loc[] to get these subsets:
  * from Pakistan to Russia.
  * from Lahore to Moscow. (This will return nonsense.)
  * from Pakistan, Lahore to Russia, Moscow.
```python
# Sort the index of temperatures_ind
temperatures_srt = temperatures_ind.sort_index()
# Subset rows from Pakistan to Russia
print(temperatures_srt.loc['Pakistan': 'Russia'])

# Try to subset rows from Lahore to Moscow
print(temperatures_srt.loc['Lahore': 'Moscow'])
#To slice at inner levels, first and last should be tuples.
# Subset rows from Pakistan, Lahore to Russia, Moscow
print(temperatures_srt.loc[('Pakistan','Lahore'):('Russia','Moscow')])
```

### Slicing in both directions
You've seen slicing DataFrames by rows and by columns, but since DataFrames are two-dimensional objects, it is often natural to slice both dimensions at once. That is, by passing two arguments to .loc[], you can subset by rows and columns in one go.

*	Use .loc[] slicing to subset rows from India, Hyderabad to Iraq, Baghdad.
*	Use .loc[] slicing to subset columns from date to avg_temp_c.
*	Slice in both directions at once from Hyderabad to Baghdad, and date to avg_temp_c.
```python
# Subset rows from India, Hyderabad to Iraq, Baghdad
print(temperatures_srt.loc[('India','Hyderabad'):('Iraq','Baghdad')])
# Subset columns from date to avg_temp_c
print(temperatures_srt.loc[: ,"date" : "avg_temp_c"])
# Subset in both directions at once
print(temperatures_srt.loc[('India','Hyderabad'):('Iraq','Baghdad'),"date":"avg_temp_c"])
```
### Slicing time series
Slicing is particularly useful for time series since it's a common thing to want to filter for data within a date range. Add the date column to the index, then use .loc[] to perform the subsetting. The important thing to remember is to keep your dates in ISO 8601 format, that is, "yyyy-mm-dd" for year-month-day, "yyyy-mm" for year-month, and "yyyy" for year.
*	Use Boolean conditions, not .isin() or .loc[], and the full date "yyyy-mm-dd", to subset temperatures for rows in 2010 and 2011 and print the results.
*	Set the index of temperatures to the date column and sort it.
*	Use .loc[] to subset temperatures_ind for rows in 2010 and 2011.
*	Use .loc[] to subset temperatures_ind for rows from Aug 2010 to Feb 2011.

```python
# Use Boolean conditions to subset temperatures for rows in 2010 and 2011
temperatures_bool = temperatures[(temperatures['date']>= "2010-01-01") & (temperatures['date'] <='2011-12-31')]
print(temperatures_bool)
temperatures.head()
# Set date as the index and sort the index
temperatures_ind = temperatures.set_index('date').sort_index()
# Use .loc[] to subset temperatures_ind for rows in 2010 and 2011
print(temperatures_ind.loc['2010':'2011'])
# Use .loc[] to subset temperatures_ind for rows from Aug 2010 to Feb 2011
print(temperatures_ind.loc['2010-08':'2011-02'])
```

### Subsetting by row/column number
The most common ways to subset rows are the ways we've previously discussed: using a Boolean condition or by index labels. However, it is also occasionally useful to pass row numbers.
This is done using .iloc[], and like .loc[], it can take two arguments to let you subset by rows and columns.
Use .iloc[] on temperatures to take subsets.
*	Get the 23rd row, 2nd column (index positions 22 and 1).
*	Get the first 5 rows (index positions 0 to 5).
*	Get all rows, columns 3 and 4 (index positions 2 to 4).
*	Get the first 5 rows, columns 3 and 4.

```python
# Get 23rd row, 2nd column (index 22, 1)
print(temperatures.iloc[22,1])
# Use slicing to get the first 5 rows
print(temperatures.iloc[0:5])
# Use slicing to get columns 3 to 4
print(temperatures.iloc[:,2:4])
# Use slicing in both directions at once
print(temperatures.iloc[0:5,2:4])
```

#### Pivot temperature by city and year
It's interesting to see how temperatures for each city change over time—looking at every month results in a big table, which can be tricky to reason about. Instead, let's look at how temperatures change by year.
*	Add a year column to temperatures, from the year component of the date column.
*	Make a pivot table of the avg_temp_c column, with country and city as rows, and year as columns. Assign to temp_by_country_city_vs_year, and look at the result.

```python
# Add a year column to temperatures
temperatures['year'] = temperatures['date'].dt.year
# Pivot avg_temp_c by country and city vs year
temp_by_country_city_vs_year = temperatures.pivot_table('avg_temp_c',index = ['country', 'city'], columns = 'year')
# See the result
print(temp_by_country_city_vs_year)
```
#### Subsetting pivot tables
A pivot table is just a DataFrame with sorted indexes, so the techniques you have learned already can be used to subset them. In particular, the .loc[] + slicing combination is often helpful.
Use .loc[] on temp_by_country_city_vs_year to take subsets.
*	From Egypt to India.
*	From Egypt, Cairo to India, Delhi.
*	From Egypt, Cairo to India, Delhi, and 2005 to 2010.

```python
# Subset for Egypt to India
temp_by_country_city_vs_year.loc['Egypt':'India']
# Subset for Egypt, Cairo to India, Delhi
temp_by_country_city_vs_year.loc[('Egypt','Cairo'):('India','Delhi')]
# Subset for Egypt, Cairo to India, Delhi, and 2005 to 2010
temp_by_country_city_vs_year.loc[('Egypt','Cairo'):('India','Delhi'),'2005': '2010']
```
### Calculating on a pivot table
Pivot tables are filled with summary statistics, but they are only a first step to finding something insightful. Often you'll need to perform further calculations on them. A common thing to do is to find the rows or columns where the highest or lowest value occurs.
*	Calculate the mean temperature for each year, assigning to mean_temp_by_year.
*	Filter mean_temp_by_year for the year that had the highest mean temperature.
*	Calculate the mean temperature for each city (across columns), assigning to mean_temp_by_city.
*	Filter mean_temp_by_city for the city that had the lowest mean temperature

```python
# Get the worldwide mean temp by year
mean_temp_by_year = temp_by_country_city_vs_year.mean()
temp_by_country_city_vs_year.head()
# Filter for the year that had the highest mean temp
print(mean_temp_by_year[mean_temp_by_year==max(mean_temp_by_year)])
# Get the mean temp by city
mean_temp_by_city = temp_by_country_city_vs_year.mean(axis = 'columns')
mean_temp_by_city 
# Filter for the city that had the lowest mean temp
print(mean_temp_by_city[mean_temp_by_city==min(mean_temp_by_city)])
```

# Creating and visualizing data frame 

* Print the head of the avocados dataset. What columns are available?
* For each avocado size group, calculate the total number sold, storing as nb_sold_by_size.
* Create a bar plot of the number of avocados sold by size.
* Show the plot.

```python
# Import matplotlib.pyplot with alias plt
import matplotlib.pyplot as plt
# Look at the first few rows of data
print(avocados.head())
# Get the total number of avocados sold of each size
nb_sold_by_size = avocados.groupby('size')['nb_sold'].sum()
nb_sold_by_size 
# Create a bar plot of the number of avocados sold by size
nb_sold_by_size.plot(kind = 'bar')
# Show the plot
plt.show()
```
## Changes in sales over time
Line plots are designed to visualize the relationship between two numeric variables, where each data values is connected to the next one. They are especially useful for visualizing the change in a number over time since each time point is naturally connected to the next time point. In this exercise, you'll visualize the change in avocado sales over three years.

* 	Get the total number of avocados sold on each date. The DataFrame has two rows for each date—one for organic, and one for conventional. Save this as nb_sold_by_date.
* 	Create a line plot of the number of avocados sold.
*	Show the plot.

```python
# Import matplotlib.pyplot with alias plt
import matplotlib.pyplot as plt
avocados.head()
# Get the total number of avocados sold on each date
nb_sold_by_date = avocados.groupby('date')['nb_sold'].sum()
nb_sold_by_date
# Create a line plot of the number of avocados sold by date
nb_sold_by_date.plot(kind = 'line')
# Show the plot
plt.show()
```
### Avocado supply and demand
Scatter plots are ideal for visualizing relationships between numerical variables. In this exercise, you'll compare the number of avocados sold to average price and see if they're at all related. If they're related, you may be able to use one number to predict the other.
*	Create a scatter plot with nb_sold on the x-axis and avg_price on the y-axis. Title it "Number of avocados sold vs. average price".
*	Show the plot.
```python
# Scatter plot of avg_price vs. nb_sold with title
avocados.plot(x = 'nb_sold', y = 'avg_price', kind = 'scatter', title ="Number of avocados sold vs. average price" )
# Show the plot
plt.show()
```
###  Price of conventional vs. organic avocados
Creating multiple plots for different subsets of data allows you to compare groups. In this exercise, you'll create multiple histograms to compare the prices of conventional and organic avocados.
*	Subset avocados for the conventional type, and the average price column. Create a histogram.
*	Create a histogram of avg_price for organic type avocados.
*	Add a legend to your plot, with the names "conventional" and "organic".
*	Modify your code to use 20 bins in both histograms.
*	Modify your code to adjust the transparency of both histograms to 0.5 to see how much overlap there is between the two distributions.
*	Show your plot.

```python
# Modify bins to 20
avocados[avocados["type"] == "conventional"]["avg_price"].hist(alpha=0.5, bins = 20)
# Modify bins to 20
avocados[avocados["type"] == "organic"]["avg_price"].hist(alpha=0.5, bins=20)
# Add a legend
plt.legend(["conventional", "organic"])
# Show the plot
plt.show()

```


  
