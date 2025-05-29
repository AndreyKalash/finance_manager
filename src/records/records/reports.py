from datetime import datetime
from io import BytesIO, StringIO
import csv
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


async def generate_csv(data: list[dict], record_type_id: int) -> BytesIO:
    """
    Генерация CSV отчета с учетом типа записи (расход/доход)
    
    :param data: Список словарей с данными записей
    :param record_type_id: 1 - расходы, 2 - доходы
    :return: BytesIO буфер с CSV данными
    """
    text_buffer = StringIO()
    
    headers = [
        "date", "name", "amount"
    ]
    if record_type_id == 1:
        headers.extend(["unit", "unit_quantity", "product_quantity"])
    headers.extend(["category", "tags"])
    
    
    flat_data = []
    for record in data:
        flat_record = {
            "date": record["record_date"],
            "name": record["name"],
            "amount": record["amount"],
            "category": record["category"]["name"],
            "tags": ", ".join(tag["name"] for tag in record["tags"])
        }
        if record_type_id == 1:
            flat_record.update({
                "unit": record["unit"]["name"] if record["unit"] else "",
                "unit_quantity": str(record["unit_quantity"]),
                "product_quantity": str(record["product_quantity"])
            })
        flat_data.append(flat_record)
        
    writer = csv.DictWriter(text_buffer, fieldnames=headers, delimiter=';')
    writer.writeheader()
    writer.writerows(flat_data)
    
    text_buffer.seek(0)
    bytes_buffer = BytesIO(text_buffer.getvalue().encode('utf-8-sig'))
    return bytes_buffer

async def generate_excel(data: list[dict], record_type_id: int) -> BytesIO:
    """
    Генерация Excel файла с автоматическим форматированием
    
    :param data: Список словарей с данными записей
    :param record_type_id: 1 - расходы, 2 - доходы 
    :return: BytesIO буфер с XLSX данными
    """
    buffer = BytesIO()
    
    excel_data = []
    for record in data:
        excel_record = {
            "Дата": record["record_date"],
            "Название": record["name"],
            "Сумма": float(record["amount"]),
            "Категория": record["category"]["name"],
            "Теги": ", ".join(tag["name"] for tag in record["tags"])
        }
        if record_type_id == 1:
            excel_record.update({
                "Единица": record["unit"]["name"] if record["unit"] else "",
                "Кол-во единиц": float(record["unit_quantity"]),
                "Кол-во товара": record["product_quantity"]
            })
        
        excel_data.append(excel_record)

    df = pd.DataFrame(excel_data)
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Records')
        worksheet = writer.sheets['Records']
        
        cell_format = writer.book.add_format({'font_name': 'Arial'})
        worksheet.set_column('A:Z', 20, cell_format)
        
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)

    buffer.seek(0)
    return buffer
# Регистрация кастомного шрифта для поддержки кириллицы в PDF
pdfmetrics.registerFont(TTFont("DejaVuSerif", "DejaVuSerif.ttf"))
async def generate_pdf(data: list[dict], record_type_id: int) -> BytesIO:
    """
    Генерация PDF отчета с табличным представлением данных
    
    :param data: Список словарей с данными записей
    :param record_type_id: 1 - расходы, 2 - доходы
    :return: BytesIO буфер с PDF данными
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'DejaVuSerif'
    styles['Title'].fontName = 'DejaVuSerif'
    
    
    headers = ["Дата", "Название", "Сумма"]
    if record_type_id == 1:
        headers.extend(["Кол-во товара", "Единица", "Кол-во единиц"])
    headers.extend(["Категория", "Теги"])
    
    pdf_data = [[Paragraph(header, styles['Normal']) for header in headers]]
    for record in data:
        row = [
            Paragraph(str(record["record_date"]), styles['Normal']),
            Paragraph(record["name"], styles['Normal']),
            Paragraph(f"{float(record['amount']):.2f}"),
        ]
        if record_type_id == 1:
            row.extend([
                record['product_quantity'],
                Paragraph(record["unit"]["name"], styles['Normal']),
                Paragraph(f"{float(record['unit_quantity'])}"),
            ])
        row.extend([
            Paragraph(record["category"]["name"], styles['Normal']),
            Paragraph(", ".join(tag["name"] for tag in record["tags"]), styles['Normal']),
        ])
        pdf_data.append(row)

    table = Table(pdf_data)
    style = TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'DejaVuSerif'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#BB86FC")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FFFFFF")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#444")),
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_filename(extension: str) -> str:
    """
    Генерация уникального имени файла на основе текущего времени
    
    :param extension: Расширение файла (csv, xlsx, pdf)
    :return: Строка с именем файла
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"records_{timestamp}.{extension}"