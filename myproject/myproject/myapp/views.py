# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm

def get_table_context(f)

    print f.read()
    return {"schema_list" : [{"col" : 1, "value" : "Country"},
                             {"col" : 2, "value" : "Population"}],
                             
            "row_list" : [{"row" : 1, "cell" : [{"col" : 1, "value" : "China"},
                                                {"col" : 2, "value" : "20"}]},
                          {"row" : 2, "cell" : [{"col" : 1, "value" : "US"},
                                                {"col" : 2, "value" : "30"}]}]}
    
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
            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
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
