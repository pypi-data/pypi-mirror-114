#!/usr/bin/env python

from io import BytesIO

from pystrich.datamatrix import DataMatrixEncoder
from reportlab.graphics.barcode import code128
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


def code128_one_line(
        barcode_values: list[str],
        line_one_values: list[str]
) -> BytesIO:
    bytes_ = BytesIO()
    canvas: Canvas = Canvas(bytes_, pagesize=(4 * inch, 6 * inch))
    for barcode_value, line_one_value in zip(barcode_values, line_one_values):
        barcode = code128.Code128(barcode_value, barHeight=1 * inch, barWidth=1.5, humanReadable=True)
        canvas.setFont('Times-Bold', 60)
        canvas.drawString(50, 200, line_one_value)
        barcode.drawOn(canvas, 50, 300)
        canvas.showPage()
    canvas.save()
    bytes_.seek(0)
    return bytes_


def datamatrix_one_line(
        barcode_values: list[str],
        line_one_values: list[str]
) -> BytesIO:
    bytes_ = BytesIO()
    canvas: Canvas = Canvas(bytes_, pagesize=(4 * inch, 6 * inch))
    for barcode_value, line_one_value in zip(barcode_values, line_one_values):
        image = ImageReader(BytesIO(DataMatrixEncoder(barcode_value).get_imagedata()))
        canvas.drawString(70, 280, line_one_value)
        canvas.drawImage(image, 70, 300, mask='auto')
        canvas.showPage()
    canvas.save()
    bytes_.seek(0)
    return bytes_
