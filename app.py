# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask , render_template, request, redirect, jsonify, send_file


from werkzeug.utils import secure_filename
import pandas as pd
import os
import io


# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)


# definition of data_list and details

def data_list_details():
	# ----------------------------------------------- convert csv data into list
	global data_list, details
	data_list = [list(df.columns)] + df.values.tolist()

	# ----------------------------------------------- get info of csv

	info_buffer = io.StringIO()
	df.info(buf = info_buffer)
	details = info_buffer.getvalue()
	# -----------------------------------------------

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def home():
	return render_template("index.html", mimetype="image/jpeg")

@app.route('/Dataset_Details' , methods = ['GET', 'POST'])
def Dataset_Details():

	# ---------------------------------------------- Get dataset from user
	if (request.method == 'POST'):
		# set file location 
		file_location = 'C:\\Users\\DELL\\Desktop\\BE_Project\\final year project\\prj_web\\Dataset'  #here dataset is stored

		# set the upload folder
		app.config['UPLOAD_FOLDER'] = file_location

		# request file
		file = request.files['FileInput']

		# Save File
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

	# path of dataset

	global csv_path, fileName
	fileName = file.filename
	csv_path = "Dataset/" + secure_filename(file.filename)
	
	# ----------------------------------------------- read csv

	global df

	try:

		df = pd.read_csv(csv_path, encoding='unicode_escape', low_memory=False)


	except Exception as e:

		# df = pd.read_json(csv_path, encoding='unicode_escape', low_memory=False)
		df = pd.read_json(csv_path)


	# ----------------------------------------------- drop null and duplicated values

	df = df.dropna()

	df.drop_duplicates(inplace = True)

	# ------------------------------------------- call fun data_list_details
	data_list_details()

# -----------------------------------------------
	table_json = df.where(pd.notna(df), "").to_dict(orient='records')

	return render_template("Dataset_Details.html", data_list = data_list, details = details, table = table_json , fileName = fileName)

@app.route('/Dataset_Cleaning')
def Dataset_Cleaning():

	select_col_op = request.args.get('select_col_op')

	split_data_op = request.args.get('split_data')
	split_from_value = request.args.get('split_from_value')
	split_join_value = request.args.get('split_join_value')
	split_start_value = request.args.get('split_start_value')
	split_end_value = request.args.get('split_end_value')

	change_data_type_int = request.args.get('change_data_type_int')

	change_data_type_string = request.args.get('change_data_type_string')

	# --------------------------
	common_replace_op = request.args.get('common_replace')
	common_replace_value = request.args.get('common_replace_value')
	common_replace_to_value = request.args.get('common_replace_to_value')

	unique_replace_op = request.args.get('unique_replace')
	unique_replace_value = request.args.get('unique_replace_value')
	unique_replace_to_value = request.args.get('unique_replace_to_value')
	# ------------------

	drop_row_op = request.args.get('drop_row')
	drop_value = request.args.get('drop_row_value')


	drop_col_op = request.args.get('drop_col')
	drop_col_start = request.args.get('drop_col_start')
	drop_col_end = request.args.get('drop_col_end')


	dropMultipleRows_op = request.args.get('dropMultipleRows')
	dropMultipleRows_start = request.args.get('dropMultipleRows_start')
	dropMultipleRows_end = request.args.get('dropMultipleRows_end')


	global status, see_list1, see_col1, see_col, df

	df.to_csv(csv_path, index=False)
	df = pd.read_csv(csv_path)

	status = ""
	see_list = list(df.columns)
	see_col = request.args.get('see_col')
	

	# ------------------------------------------------- split data
	

	if split_data_op == "split_data":
		if split_from_value == "space" or split_from_value == "Space" or split_from_value == "SPACE":
			split_from_value = " "
			

		if split_join_value == "space" or split_join_value == "Space" or split_join_value == "SPACE":
			split_join_value = " "

		status = ""
		try:
			split_start_value = int(split_start_value) - 1
			split_end_value = int(split_end_value) 
			
			df[select_col_op] = df[select_col_op].str.split(split_from_value).str.slice(start=split_start_value, stop=split_end_value).str.join(split_join_value)
			
			status = "*Changes made successfully"
			see_list1 = df[select_col_op].unique()
			see_col1 = select_col_op
		except Exception as e:
			status = "* Please check values are present in column."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()
		

	# ---------------------------------------------------unique replace----------
	if unique_replace_op == "unique_replace":
		if unique_replace_value == "space" or unique_replace_value == "Space" or unique_replace_value == "SPACE":
			unique_replace_value = " "
		if unique_replace_to_value == "space" or unique_replace_to_value == "Space" or unique_replace_to_value == "SPACE":
			unique_replace_to_value = " "
		see_list1 = df[select_col_op].unique()

		if True:
		
			status = ""
			try:
				if unique_replace_value == "nan" or "Nan" or "NAN":
					df[select_col_op] = df[select_col_op].fillna(unique_replace_to_value)

				mask = df[select_col_op] == unique_replace_value

				df.loc[mask, select_col_op] = unique_replace_to_value

				status = "*Changes made successfully"
				see_list1 = df[select_col_op].unique()
				see_col1 = select_col_op
			except Exception as e:
				status = "* Please check values are present in column."
				see_col1 = select_col_op
				see_list1 = df[select_col_op].unique()
		else:
			status = "* Please check values are present in column."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()

	# -------------------------------------------------common replace data

	if common_replace_op == "common_replace":
		if common_replace_value == "space" or common_replace_value == "Space" or common_replace_value == "SPACE":
			common_replace_value = " "
		if common_replace_to_value == "space" or common_replace_to_value == "Space" or common_replace_to_value == "SPACE":
			common_replace_to_value = " "
		see_list1 = df[select_col_op].unique()

		if True:
		
			status = ""
			try:
				if common_replace_value == "nan" or "Nan" or "NAN":
					df[select_col_op] = df[select_col_op].fillna(common_replace_to_value)

				df[select_col_op] = df[select_col_op].str.replace(common_replace_value, common_replace_to_value)

				status = "*Changes made successfully"
				see_list1 = df[select_col_op].unique()
				see_col1 = select_col_op
			except Exception as e:
				status = "* Please check values are present in column."
				see_col1 = select_col_op
				see_list1 = df[select_col_op].unique()
		else:
			status = "* Please check values are present in column."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()

	
	# ------------------------------------------------- drop row

	if drop_row_op == "drop_row":
		see_list1 = df[select_col_op].unique()
		if drop_value in see_list1 or drop_value in see_list1[0]:
		
			status = ""
			try:
				df = df[df[select_col_op] != drop_value] 

				status = "*Changes made successfully"
				see_list1 = df[select_col_op].unique()
				df.to_csv(csv_path, index=False)
				df = pd.read_csv(csv_path)
				see_col1 = select_col_op
			except Exception as e:
				status = "* Please check values are present in column."
				see_col1 = select_col_op
				see_list1 = df[select_col_op].unique()
	
		else:
			status = "* Please check values are present in column."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()


	# ------------------------------------------------- drop col

	if drop_col_op == "drop_col" and drop_col_start == "" and drop_col_end == "":
		try:
			df = df.drop([select_col_op], axis=1)
			df.to_csv(csv_path, index=False)
			df = pd.read_csv(csv_path)
			status = "*Changes made successfully"
		except Exception as e:
			status = "*Check columns is present or not"

	if drop_col_op == "drop_col" and (drop_col_start != "" or drop_col_end != ""):
		
		status = ""
		try:
			drop_col_start = int(drop_col_start)
			drop_col_end = int(drop_col_end)
			df.drop(df.iloc[:, (drop_col_start):(drop_col_end + 1)], inplace=True, axis=1)

			status = "*Changes made successfully"
			see_col1 = select_col_op
		except Exception as e:
			status = "* Give proper index, you can see in details."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()

	# ---------------------------------------------- dropMultipleRows ----------------------------------------------
	if dropMultipleRows_op == "dropMultipleRows" and dropMultipleRows_start == "" and dropMultipleRows_end != "":
		status = f"* You cannot give only ending index..."

	if dropMultipleRows_op == "dropMultipleRows" and dropMultipleRows_start != "" and dropMultipleRows_end == "":
		try:
			dropMultipleRows_start = int(dropMultipleRows_start) - 1

			df = df.drop([dropMultipleRows_start])
			df.to_csv(csv_path, index=False)
			df = pd.read_csv(csv_path)
			status = "*Changes made successfully"
		except Exception as e:
			status = f"* Give proper index, staring from 1 to {len(df)}..."

	if dropMultipleRows_op == "dropMultipleRows" and dropMultipleRows_start != "" and dropMultipleRows_end != "":
		
		status = ""
		try:
			dropMultipleRows_start = int(dropMultipleRows_start) - 1
			dropMultipleRows_end = int(dropMultipleRows_end) + 1
			df.drop(df.index[dropMultipleRows_start : dropMultipleRows_end], inplace=True)

			status = "*Changes made successfully"
			see_col1 = select_col_op
		except Exception as e:
			status = f"* Give proper index, staring from 1 to {len(df)}..."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()

	
	# ----------------------------------------------- convert data type to int32

	if change_data_type_int == "change_data_type_int":
		see_list1 = df[select_col_op].unique()
		status = ""
		try:
			df[select_col_op] = df[select_col_op].astype(int)#int32
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()

			status = "*Changes made successfully"
		except Exception as e:
			status = "* Please select column with all integer values."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()


	# ----------------------------------------------- convert data type to string

	if change_data_type_string == "change_data_type_string":
		see_list1 = df[select_col_op].unique()
		status = ""
		try:
		
			df[select_col_op] = df[select_col_op].astype(str)
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()


			status = "*Changes made successfully"
		except Exception as e:
			status = "* Please select column with all integer values."
			see_col1 = select_col_op
			see_list1 = df[select_col_op].unique()


	# ------------------------------------------------- see unique values

	if see_col in see_list:
		see_col1 = see_col
		see_list1 = df[see_col].unique()

	# ------------------------------------------- call fun data_list_details
	data_list_details()

	table_json = df.where(pd.notna(df), "").to_dict(orient='records')

	return render_template("dataCleaning.html", data_list = data_list, details = details, select_col_op = select_col_op, status = status, see_list = see_list1, see_col = see_col1, table=table_json, csv_path = csv_path, fileName = fileName)


# # ----------------------------------------------
@app.route('/update_data', methods=['POST'])
def update_data():
    updated_data = request.get_json()
	
    for update in updated_data:
        row = update['row']
        col = update['col']
        value = update['value']
        df.at[row, col] = value
	
    return jsonify(success=True)
# # ---------------------------------------------

from flask import send_file
from io import StringIO

@app.route('/download_and_delete')
def download_and_delete():
    # Create a buffer to hold the CSV data
    csv_buffer = StringIO()

    # Save the updated DataFrame to the buffer (instead of a file)
    df.to_csv(csv_buffer, index=False)

    # Get the CSV data as a string
    csv_data = csv_buffer.getvalue()

    # Delete the uploaded CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)

    return csv_data

# ------------------------------------------------
# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.
	app.run(debug=True, port=8000)
