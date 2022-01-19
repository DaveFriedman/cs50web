from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from difflib import get_close_matches
from markdown import markdown
from random import choice

from . import forms
from . import util


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create_entry(request, title=None):

    if request.method == "POST":
        form = forms.entry_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            
            if not util.get_entry(title):
                util.save_entry(title, bytes(body, "utf8"))

                messages.success(request, f"Entry '{title}' has been added!")
                return HttpResponseRedirect(
                    reverse("read", kwargs={"title": title}))
            
            else:
                messages.error(request, f"Entry '{title}' could not be added.")
                return render(request, "encyclopedia/create_entry.html", {
                    "form": form
                })

    else:
        return render(request, "encyclopedia/create_entry.html", {
            "form": forms.entry_form(initial={"title": title})
        })


def read_entry(request, title):

    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": markdown(util.get_entry(title))
        })

    else:
        return render(request, "encyclopedia/no_entry.html", {
            "title": title
        })


def update_entry(request, title):

    if request.method == "POST":
        form = forms.entry_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            util.save_entry(title, bytes(body, "utf8"))

            messages.success(request, f"Entry '{title}' has been updated!")
            return HttpResponseRedirect(
                reverse("read", kwargs={"title": title}))
        
        else:
            messages.error(request, f"Entry '{title}' was not updated.")
            return render(request, "encyclopedia/update_entry.html", {
                "form": form
            })
            
    else:
        body = util.get_entry(title)

        return render(request, "encyclopedia/update_entry.html", {
            "title": title,
            "form": forms.entry_form(initial={
                "title": title, 
                "body": body
                })
        })


def delete_entry(request, title):

    if util.get_entry(title):
        util.remove_entry(title)
        messages.success(request, f"Entry '{title}' has been deleted.")

    else:
        messages.error(request, f"Entry '{title}' was not deleted.")
    
    return HttpResponseRedirect(reverse("index"))


def random(request):

    c = choice(util.list_entries())
    return HttpResponseRedirect(
        reverse("read", kwargs={"title": c}))


def search(request):

    query = request.GET.get("q")
    titles = util.list_entries()

    query_c, titles_c = query.casefold(), [t.casefold() for t in titles]

    # Disregarding case, send exact matches directly to entry
    for t in titles_c:
        if query_c == t:
            return HttpResponseRedirect(
                reverse("read", kwargs={"title": t}))

    # Get a list of close matches
    results_c = get_close_matches(query_c, titles_c, cutoff=.4)
    results = [t for t in titles if t.casefold() in results_c]

    # Send queries with no close matches to a no_entry page for that query 
    if not results:
        return HttpResponseRedirect(
            reverse("read", kwargs={"title": query}))

    # Otherwise, display the search results
    return render(request, "encyclopedia/search_results.html", {
        "results": results
    })
