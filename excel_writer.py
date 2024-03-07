import base64
from io import BytesIO
import xlsxwriter


def create_excel_file(data):

    file_name = "ProductDetails.xlsx"
    img_col = data[len(data)-1]["max_image_len"]
    review_col = data[len(data) -1]["max_review_len"]


    workbook = xlsxwriter.Workbook(file_name)
    
    # main header formatting
    format0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True, 'font_color': '#40679E'})
    format0.set_align('center')
    format0.set_border()
    
    # column header formatting
    format1 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True})
    format1.set_align('left')
    format1.set_border()
    
    format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True})
    format2.set_align('center')
    format2.set_border()
    format3 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True})
    format3.set_align('right')
    format3.set_border()

    # body formatting
    format4 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
    format4.set_align('left')
    format4.set_border()
    format5 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
    format5.set_align('center')
    format5.set_border()
    format6 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
    format6.set_align('right')
    format6.set_border()
    
    # Sheet Name
    sheet = workbook.add_worksheet('Product Details')
    
    # write in sheet
    sheet.merge_range(0, 0, 0, img_col+16, "Product Details", format0)

    sheet.merge_range(2, 0, 3, 0, 'SL No', format2)
    sheet.merge_range(2, 1, 3, 1, 'Product URL', format2)
    sheet.merge_range(2, 2, 3, 2, 'Breadcrumb (Category)', format2)
    sheet.merge_range(2, 3, 3, 3, 'Category', format2)
    sheet.merge_range(2, 4, 3, 4, 'Product Name', format2)
    
    sheet.merge_range(2, 5, 2, 5 + img_col-1, 'Image URL', format2)
    for i in range(img_col):
        sheet.write(3, 5+i, f'Image {i+1}', format2)
        i+=1

    sheet.merge_range(2, img_col + 5, 3, img_col+5, 'Price', format2)
    sheet.merge_range(2, img_col + 6, 3, img_col+6, 'Available Size', format2)
    sheet.merge_range(2, img_col + 7, 2, img_col+11, 'Coordinated product', format2)
    sheet.write(3, img_col + 7, 'product name', format2)
    sheet.write(3, img_col + 8, 'Price', format2)
    sheet.write(3, img_col + 9, 'Product number', format2)
    sheet.write(3, img_col + 10, 'Image URL', format2)
    sheet.write(3, img_col + 11, 'Product URL', format2)

    sheet.merge_range(2, img_col + 12, 2, img_col+14, 'Description', format2)
    sheet.write(3, img_col + 12, 'Description Title', format2)
    sheet.write(3, img_col + 13, 'General Description', format2)
    sheet.write(3, img_col + 14, 'Itemize Description', format2)

    sheet.merge_range(2, img_col + 15, 3, img_col + 15, 'Size Chart', format2)
    
    row = 4
    col = 0
    sl_no = 1
    
    for rec in data:
        sheet.write(row, col, sl_no, format5)
        sheet.write(row, col+1, rec['prod_url'], format5)
        sheet.write(row, col+2, rec['breadcrumbs'], format5)
        sheet.write(row, col+3, rec['category'], format5)
        sheet.write(row, col+4, rec['name'], format5)

        for i in range(img_col):
            image_key = f'image_{i + 1}'
            if image_key in rec:
                sheet.write(row, 5 + i, rec[image_key], format2)
            else:
                sheet.write(row, 5 + i, "", format2)

        sheet.write(row, img_col + 5, rec['price'], format5)
        sheet.write(row, img_col + 6, rec['available_sizes'], format5)
        sheet.write(row, img_col + 6, rec['cp_name'] or '', format5)
        sheet.write(row, img_col + 8, rec['cp_price'] or '', format5)
        sheet.write(row, img_col + 9, rec['cp_number'] or '', format5)
        sheet.write(row, img_col + 10, rec['cp_img_url'] or '', format5)
        sheet.write(row, img_col + 11, rec['cp_prod_url'] or '', format5)
        sheet.write(row, img_col + 12, rec['dsr_title'] or '', format5)
        sheet.write(row, img_col + 13, rec['dsr_general'] or '', format5)
        sheet.write(row, img_col + 14, rec['dsr_itemize'] or '', format5)
        sheet.write(row, img_col + 15, rec['size_chart'], format5)
        
                    
        row += 1
        sl_no += 1
                            
    workbook.close()




