from .file_processor.parsers_registry import register

def open_excel_sheet(file_instance, sheet=0):
    workbook = xlrd.open_workbook(file_instance, encoding_override="cp1252")
    return workbook.sheet_by_index(sheet)

def search_sheet(value, sheet):
    for rowidx in range(sheet.nrows):
        row = sheet.row(rowidx)
        for colidx, cell in enumerate(row):
            if cell.value == value:
                return rowidx, colidx
    return None, None

@register([2,3])
def dummy_parser(file_instance):
    print(file_instance, type(file_instance))
    return []

@register([1])
def bd_parser(file_instance):
    sheet = open_excel_sheet(file_instance)

    code_row, code_col = search_sheet('Acc No', sheet)
    company_row, company_col = search_sheet('Company'. sheet)
    qty_row, qty_col = search_sheet('Qty Sold', sheet)
    cost_row, cost_col = search_sheet('Cost', sheet)
    sales_row, sales_col = search_sheet('Sales', sheet)

    if code_row == company_row == qty_row == cost_row == sales_row:
        row = code_row
        product = None
        transactions = []

        # Go through each line of the report
        while row < self.sheet.nrows:
            if ',' in str(self.sheet.cell(row, code_col).value):
                # Set product code and title in a list
                product = str(self.sheet.cell(row, code_col).value).split(',', 1)
            elif 'Total' in str(self.sheet.cell(row, company_col).value):
                # Unset product when transactions have been extracted
                product = None
            elif not product:
                # Skip rows if a product has not been set
                pass
            else:
                # Set quantity for the transaction
                quantity = float(self.sheet.cell(row, qty_col).value)
                if quantity > 0:
                    # Extract transaction info
                    customer_code = str(self.sheet.cell(row, code_col).value)
                    customer_title = str(self.sheet.cell(row, company_col).value)
                    cost = float(self.sheet.cell(row, cost_col).value)/quantity
                    price = float(self.sheet.cell(row, sales_col).value)/quantity
                    record = {'product_code':product[0],
                            'product_title':product[1],
                            'customer_code':customer_code,
                            'customer_title':customer_title,
                            'quantity':quantity,
                            'cost':cost,
                            'price':price}
                    # Append info to list of transactions
                    transactions.append(record.copy())
            # Move to the next row
            row = row+1

    if len(transactions) == 0:
        raise xlrd.XLRDError('No data could be read from BD Foods file')
    print(len(transactions))
    return transactions
