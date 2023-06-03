from django.shortcuts import render
from . import util
from markdown2 import Markdown
from random import choice

def convert_md(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
        


def index(request):
    entries = util.list_entries()
    css_file = util.get_entry("CSS")
    coffee = util.get_entry("coffee")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message" : "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        searched_data = request.POST["q"]
        html_content = convert_md(searched_data)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": searched_data,
                "content": html_content
            })
        else:
            list_of_entries = util.list_entries()
            recommended = []
            for entry in list_of_entries:
                if searched_data.lower() in entry.lower():
                    recommended.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommended": recommended
            })
        
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        existed_title = util.get_entry(title)
        if existed_title is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "content": html_content
            })
        
def edit_page(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def random(request):
    existed_entries = util.list_entries()
    random_entry = choice(existed_entries)
    html_content = convert_md(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })