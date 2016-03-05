# -*- coding: utf-8 -*-
import csv
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm

def get_table_context(f):

    schema_list = []
    row_list = []

    csvreader = csv.reader(f)
    for line in csvreader:

        cur_row = []
        for i in range(len(line)):
            cur_row.append({"col" : i, "value" : line[i]})

        if not schema_list:
            schema_list = cur_row
        else:
            row_list.append({"row" : len(row_list), "cell" : cur_row})

    return {"schema_list" : schema_list, "row_list" : row_list}
#    return {"schema_list" : [{"col" : 1, "value" : "Country"},
#                             {"col" : 2, "value" : "Population"}],
                             
#            "row_list" : [{"row" : 1, "cell" : [{"col" : 1, "value" : "China"},
#                                                {"col" : 2, "value" : "20"}]},
#                          {"row" : 2, "cell" : [{"col" : 1, "value" : "US"},
#                                                {"col" : 2, "value" : f.name}]}]}

def list(request):

    context = {}
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            context.update(get_table_context(request.FILES['docfile']))
            context["has_table"] = True
    else:
        form = DocumentForm() # A empty, unbound form
        context["has_table"] = False

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context["documents"] = documents
    context["form"] = form
    
    return render_to_response(
        'myapp/list.html',
        context,
        context_instance=RequestContext(request)
    )
