# Change Log 

* Version 0.0.5 (2021-07-20)
	* Intialize
	* Start from 0.0.5 as previous versions are all failed
	* Remove __os__, __re__, __string__ from 'install_requires', as they are built-in packages. Issue raise up if list those packages. 

* Version 0.0.6 (2021-07-20)
	* Merge scripts into __init__.py. Script can not load function from another. 

* Version 0.0.7 (2021-07-21)
	* Adjust the column width of reference table.

* Version 0.0.8 (2021-07-23)
	* Add `merge_duplicated_ref()`
		* merge keywords together
		* sort keywords by alphabet 
	* When export to Excel
		* Assign referneces with no keyword to "No Category" sheet
		* Assign references with keyword of __" * "__ to "Important" sheet