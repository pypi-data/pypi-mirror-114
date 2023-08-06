#!/usr/bin/env python

from io import BytesIO
from pkgutil import get_data
from typing import Optional

from pystrich.datamatrix import DataMatrixEncoder
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code128, qr
from reportlab.graphics.barcode.eanbc import UPCA
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

with BytesIO(get_data('darbiadev_labels', 'data/fonts/arial/arial.ttf')) as file:
    registerFont(TTFont('arial', file), )

with BytesIO(get_data('darbiadev_labels', 'data/fonts/arial/arialbd.ttf')) as file:
    registerFont(TTFont('arial-bold', file), )

with BytesIO(get_data('darbiadev_labels', 'data/fonts/arial/ariali.ttf')) as file:
    registerFont(TTFont('arial-italic', file), )

with BytesIO(get_data('darbiadev_labels', 'data/fonts/arial/arialbi.ttf')) as file:
    registerFont(TTFont('arial-bolditalic', file), )

registerFontFamily(
    'arial',
    normal='arial',
    bold='arial-bold',
    italic='arial-italic',
    boldItalic='arial-bolditalic',
)


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


def nathan_one_line(
        barcode_values: list[str],
        line_one_values: list[str]
) -> BytesIO:
    bytes_ = BytesIO()
    canvas: Canvas = Canvas(bytes_, pagesize=(2 * inch, 1.5 * inch))
    for barcode_value, line_one_value in zip(barcode_values, line_one_values):
        barcode128 = code128.Code128(barcode_value, humanReadable=True, barHeight=30)
        barcode128._calculate()
        x = (2 * inch - barcode128._width) / 2
        y = 5 * mm
        barcode128.drawOn(canvas, x, y)
        canvas.drawCentredString(1 * inch, 1 * inch, line_one_value)
        canvas.showPage()
    canvas.save()
    bytes_.seek(0)
    return bytes_


def label215(
        label_type: str = 'UPC-A',
        barcode_value: Optional[str] = None,
        item_number: Optional[str] = None,
        item_description: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        price: Optional[str] = None,
        personalize: Optional[str] = None,
) -> BytesIO:
    bytes_ = BytesIO()

    canvas_width = 2 * inch
    canvas_height = 1.5 * inch
    qr_size = .85 * inch
    canvas = Canvas(bytes_, pagesize=(canvas_width, canvas_height))

    # BARCODES BELOW
    if label_type == '128':
        barcode128 = code128.Code128(barcode_value, barHeight=45, barWidth=0.6, checksum=0)
        barcode128._calculate()
        x = (2 * inch - barcode128._width) / 2
        y = 8.5 * mm
        x1 = 6.4 * mm
        barcode128.drawOn(canvas, x, y)
    if label_type == 'QR':
        qr_code = qr.QrCodeWidget(barcode_value)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(.85 * inch, .85 * inch, transform=[.85 * inch / width, 0, 0, .85 * inch / height, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, canvas, (canvas_width - qr_size) / 2, 16)
    if label_type == 'UPC-A':
        barcode_eanbc13 = UPCA(barcode_value)
        bounds = barcode_eanbc13.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(canvas_width - .2 * inch, .5, transform=[1, 0, 0, .85, 0, 0])
        d.add(barcode_eanbc13)
        renderPDF.draw(d, canvas, (canvas_width - width) / 2, .25 * inch)

    # TEXT INFORMATION BELOW
    if item_number is not None:
        canvas.setFont('arial', 10)
        canvas.drawCentredString(canvas_width / 2, 1.35 * inch, item_number)
    if item_description is not None:
        canvas.setFont('arial', 6)
        canvas.drawCentredString(canvas_width / 2, 1.25 * inch, item_description)
    if color is not None:
        canvas.setFont('arial', 6)
        canvas.drawCentredString(canvas_width / 2, 1.15 * inch, color)
    if personalize is None:
        if label_type != 'No Barcode':
            if price is not None:
                if size is not None:
                    canvas.setFont('arial', 10)
                    canvas.drawString(.2 * inch, .1 * inch, size)
            if price is None:
                if size is not None:
                    canvas.setFont('arial', 10)
                    canvas.drawCentredString(canvas_width / 2, .1 * inch, size)
            if price is not None:
                if size is None:
                    canvas.setFont('arial', 10)
                    canvas.drawCentredString(canvas_width / 2, .1 * inch, price)
                if size is not None:
                    canvas.setFont('arial', 10)
                    canvas.drawRightString(canvas_width - .2 * inch, .1 * inch, price)
        if label_type == 'No Barcode':
            if size is not None:
                canvas.setFont('arial', 24)
                canvas.drawCentredString(canvas_width / 2, canvas_height / 3, size)
            if price is not None:
                canvas.setFont('arial', 10)
                canvas.drawCentredString(canvas_width / 2, .1 * inch, price)
    if personalize is not None:
        canvas.setFont('arial', 12)
        canvas.drawCentredString(canvas_width / 2, canvas_height / 2.5, personalize)
        if label_type == 'No Barcode':
            if price is not None:
                if size is not None:
                    canvas.setFont('arial', 10)
                    canvas.drawString(.2 * inch, .1 * inch, size)
                    canvas.setFont('arial', 10)
                    canvas.drawRightString(canvas_width - .2 * inch, .1 * inch, price)
                if size is None:
                    canvas.setFont('arial', 10)
                    canvas.drawCentredString(canvas_width / 2, .1 * inch, price)
            if price is None:
                if size is not None:
                    canvas.setFont('arial', 10)
                    canvas.drawCentredString(canvas_width / 2, .1 * inch, size)
    canvas.save()
    bytes_.seek(0)
    return bytes_


def labels_bins(
        aisle: str,
        bay: str,
        level_top: str,
        bin_: str
) -> BytesIO:
    bytes_ = BytesIO()

    canvas_width = 6 * inch
    canvas_height = 2 * inch
    canvas = Canvas(bytes_, pagesize=(canvas_width, canvas_height))

    top = aisle + bay + level_top + bin_

    level_exchanger = {'B': 'A', 'C': 'B', 'D': 'C'}
    level_bottom = level_exchanger.get(level_top, '')

    arrow_up = BytesIO(get_data('darbiadev_labels', 'data/images/arrow-up.png'))
    arrow_down = BytesIO(get_data('darbiadev_labels', 'data/images/arrow-down.png'))

    # Top info
    barcode128 = code128.Code128(top, barHeight=60, barWidth=0.7, checksum=0)
    barcode128._calculate()
    x = 0
    y = .6 * inch
    barcode128.drawOn(canvas, x, y)

    canvas.setFont('arial', 30)
    canvas.drawString(1.9 * inch, 1.1 * inch, aisle + '-' + bay + '-' + level_top + '-' + bin_)
    canvas.drawImage(ImageReader(arrow_up), 1.4 * inch, 1 * inch, .4 * inch, .4 * inch)

    # Bottom info
    if level_top != 'A':
        bottom = aisle + bay + level_bottom + bin_
        barcode128 = code128.Code128(bottom, barHeight=60, barWidth=0.7, checksum=0)
        barcode128._calculate()
        x = 4.5 * inch
        y = .1 * inch
        barcode128.drawOn(canvas, x, y)

        canvas.setFont('arial', 30)
        canvas.drawRightString(4.15 * inch, .1 * inch, aisle + '-' + bay + '-' + level_bottom + '-' + bin_)
        canvas.drawImage(ImageReader(arrow_down), 4.2 * inch, .1 * inch, .4 * inch, .4 * inch)

    canvas.save()
    bytes_.seek(0)
    return bytes_
