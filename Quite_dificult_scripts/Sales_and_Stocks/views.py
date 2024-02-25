# Python
# Django
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.db.models import Sum
from .models import Sale, Product

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return FileResponse(result, content_type='application/pdf')
    return None

def sales_report(request):
    # Aggregate total sales for each product
    product_sales = Product.objects.annotate(total_sales=Sum('sale__quantity'))
    pdf = render_to_pdf('sales_report.html', {'product_sales': product_sales})
    return pdf