# -*- coding: utf-8 -*-
from __future__ import print_function
from threading import Thread

from rest_framework import viewsets
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from .pdf import PdfGenerator


class HealthCheckViewSet(viewsets.ViewSet):
    """
    https://weasyprint.readthedocs.io/en/stable/index.html
    """
    def list(self, request):
        paragraphs = [
            'first paragraph',
            'second paragraph',
            'third paragraph'
        ]
        chart = 'https://res.cloudinary.com/nogsantos/image/upload/v1549390282/instruct/1.jpg'  # noqa

        return self._pdf_gen(paragraphs, chart)

        # worker = Generate(paragraphs, chart)
        # worker.daemon = True
        # worker.start()

        # return render(request, 'pdf_template.html', {
        #     'paragraphs': paragraphs,
        #     'chart': chart
        # })

    def _pdf_gen(self, paragraphs, chart):
        html_header = render_to_string('pdf_header.html')
        html_footer = render_to_string('pdf_footer.html')

        html_body = render_to_string(
            'pdf_template.html', {
                'paragraphs': paragraphs,
                'chart': chart
            }
        )

        PdfGenerator(
            main_html=html_body,
            header_html=html_header,
            footer_html=html_footer
        ).render_pdf()

        fs = FileSystemStorage('/tmp')
        with fs.open('document.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="document.pdf"'  # noqa
            return response


class Generate(Thread):
    """
        Thread simulator
    """

    def __init__(self, paragraphs, chart):
        Thread.__init__(self)
        self.paragraphs = paragraphs
        self.chart = chart

    def run(self):
        html_header = render_to_string('pdf_header.html')
        html_footer = render_to_string('pdf_footer.html')

        html_body = render_to_string(
            'pdf_template.html', {
                'paragraphs': self.paragraphs,
                'chart': self.chart
            }
        )

        PdfGenerator(
            main_html=html_body,
            header_html=html_header,
            footer_html=html_footer
        ).render_pdf()

        fs = FileSystemStorage('/tmp')
        with fs.open('document.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="document.pdf"'  # noqa
            return response
