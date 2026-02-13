import pandas as pd

# 1. Prepare data (Categories and their corresponding values)
data = {
    'Category': ['Marketing', 'Development', 'Sales', 'Support', 'Admin'],
    'Budget': [5000, 12000, 8000, 4000, 3000]
}
df = pd.DataFrame(data)

# 2. Setup the Excel writer
file_path = 'Budget_Report.xlsx'
writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Summary', index=False)

# 3. Access workbook/worksheet
workbook  = writer.book
worksheet = writer.sheets['Summary']

# 4. Create the Pie Chart
chart = workbook.add_chart({'type': 'pie'})

# 5. Add the data series
# Categories: 'Category' column (A2 to A6)
# Values: 'Budget' column (B2 to B6)
chart.add_series({
    'name':       'Budget Allocation',
    'categories': ['Summary', 1, 0, 5, 0],
    'values':     ['Summary', 1, 1, 5, 1],
    'data_labels': {'percentage': True, 'leader_lines': True}, # Shows % on slices
})

# 6. Formatting
chart.set_title({'name': 'Departmental Budget Distribution'})
chart.set_style(10) # Applying a pre-set Excel chart style

# 7. Insert and Save
worksheet.insert_chart('D2', chart)
writer.close()

print(f"Pie chart created in '{file_path}'")