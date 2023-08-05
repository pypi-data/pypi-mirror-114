# Package Description

RefTab is used to manage reference of journal papers. It can export reference table into 1) Excel and 2) Bibtex. Excel contains hyperlink, so users can quickly open the PDF of papers. Bibtex can be recognized for LaTex.

## Functions

* `is_year_format_correct()`
* `is_author_format_correct()`
* `auto_correct_author_string()`
* `auto_fill_abbr()`
* `auto_fill_link()`
* `read_ref_workbook()`
* `merge_ref_workbook()`
* `get_pdf_list()`
* `create_df_from_pdf_name()`
* `sort_header()`
* `save_workbook_to_excel()`
* `save_df_to_excel()`
* `save_df_to_latex()`

## RefTab Class

* `__init__()`
	* two inputs required: 
		* dataframe of reference table
		* file path of readcube folder
	* generate a list of pdf file name in readcube folder
	* file path of readcube folder is used to build hyperlink to pdf
* `update()`
	* replace dataframe with new reference table
* `find_incomplete_ref()`
* `find_duplicated_ref()`
* `find_duplicated_ref_by_abbr()`
* `find_nolink_ref()`
* `find_unlisted_pdf()`
* `find_invalid_pdf_name()`
* `get_unique_keywords()`
	* find categories of papers
* `get_unique_ref()`
	* each record has an unqiue link
		* take Link (pdf name) as primary key
	* merge duplicated records
		* Keyword for multiple records were combined in a string seperate by ','
			* for example, "General Hydrology, Classification"
* `subset_ref_by_keyword()`
* `subset_ref_by_abbr()`
* `save_to_excel()`
	* allow to save as either single-sheet or multiple-sheet (separate by keyword) workbook
* `save_to_latex()`

## Data Type

* Reference Table (DataFrame)
	* Required Columnes: 1) Title, 2) Year, 3) Journal, 4) Authors, 5) Vol, 6) Pages
	* Optional Columnes: 1) Link, 2) Abbreviation, 3) Keyword
		* Link and Abberviation can be auto-filled on the basis of other columns

* Workbook (Dictionary)
	* consist of a number of dataframe
		* key = sheet name
		* values = dataframe of reference table

