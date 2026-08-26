from django.shortcuts import render, redirect
import markdown2
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html")

    html = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })

def search(request):
    query = request.GET.get("q")

    if util.get_entry(query) is not None:
        return redirect(f"/wiki/{query}")
    else:
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
        })
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    else:
        updated_content = request.POST.get("content")
        util.save_entry(title, updated_content)
    
    return redirect("entry", title=title)

def random_page(request):
    title = random.choice(util.list_entries())
    return redirect("entry", title=title)
