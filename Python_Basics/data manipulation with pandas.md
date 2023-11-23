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
  
