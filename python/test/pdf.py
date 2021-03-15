from fpdf import FPDF,HTMLMixin
import glob
pdf = FPDF()
pdf.add_page()
pdf.add_font('微軟正黑體','','微軟正黑體-1.ttf',True)
pdf.set_font('微軟正黑體', size=16)
pdf.write(10,'title')
pdf.image('images/封面.jpg', 1, 1, w=100)
pdf.output('label_big_barcode.pdf')
