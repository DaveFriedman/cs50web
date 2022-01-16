from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from difflib import get_close_matches
from markdown import markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if entry not in util.list_entries():
        return render(request, "encyclopedia/noentry.html", {
        "title" : entry
        })

    return render(request, "encyclopedia/entry.html", {
        "entry" : markdown(util.get_entry(entry)),
        "title" : entry
    })


def random(request):
    e = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": e}))



def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        entries = util.list_entries()

        """
        Send exact matches directly to entry (regardless of case)
        """
        for e in entries:
            if query.casefold() == e.casefold():
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": e}))
                
        """
        Get a list of close matches
        """
        results = get_close_matches(query, entries, cutoff=.4)

        if not results:
            return HttpResponseRedirect(reverse("entry", kwargs={"entry": query}))

        return render(request, "encyclopedia/searchresults.html", {
            "results": results
        })
