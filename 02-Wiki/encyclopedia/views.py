from django.shortcuts import render
import markdown2
from . import util
from django import forms
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# ---- start entry page ----
# md to html


def md_to_html(title):
    # implement the logic to convert markdown entry to html
    entry_content = util.get_entry(title)

    if entry_content is None:
        return None
    else:
        markdowner = markdown2.Markdown()
        html_content = markdowner.convert(entry_content)
        return html_content


# entry page by title


def get_content(request, title):
    # get the HTML content for the specified entry title
    content_html = md_to_html(title)

    # if content is found, render the entry.html template
    if content_html is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html,
        })
    else:
        # if no content is found, render the error.html template
        return render(request, "encyclopedia/error.html")


# ---- end entry page ----

# ---- start search ----


class SearchForm(forms.Form):
    q = forms.CharField(label='Search')


def find_similar_entries(entry_search):
    all_entries = util.list_entries()
    # find entries that contain the search term (case-insensitive)
    similar_entries = [
        entry for entry in all_entries if entry_search.lower() in entry.lower()]
    return similar_entries


def search(request):
    # create an instance of the searchform
    form = SearchForm(request.POST or None)

    # handle form submission
    if request.method == "POST" and form.is_valid():
        # get the cleaned data from the form
        entry_search = form.cleaned_data['q']
        content_html = md_to_html(entry_search)

        # if a matching entry is found, render the entry.html template
        if content_html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": content_html,
            })
        else:
            # if no exact match is found, find similar entries
            similar_entries = find_similar_entries(entry_search)
            if similar_entries:
                # if similar entries are found, render the search.html template
                return render(request, "encyclopedia/search.html", {
                    "similar": similar_entries,
                    "query": entry_search,
                })
            else:
                # if no similar entries are found, render the search.html template
                return render(request, "encyclopedia/search.html", {
                    "query": entry_search,
                })

    # render the search.html template with the form
    return render(request, "encyclopedia/search.html", {'form': form})

# ---- end search ----


# ---- start new entry ----
class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name': 'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'name': 'content'}))


def new_entry(request):
    form = NewEntryForm(request.POST or None)

    # check if the request method is GET
    if request.method == "GET":
        # render the form for creating a new entry
        return render(request, "encyclopedia/new.html")
    elif request.method == "POST" and form.is_valid():
        # if the request method is POST and the form is valid, retrieve title and content from the form
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        # check if an entry with the same title already exists
        title_exist = util.get_entry(title)
        if title_exist is not None:
            # if entry already exists, render an error page
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            # if entry does not exist, save the new entry and convert content from Markdown to HTML
            util.save_entry(title, content)
            html_content = md_to_html(title)

            # render the entry page with the new content
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content,
            })

# ---- end new entry ----


# ---- start edit entry ----
class EditEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea())


def edit_entry(request, title):
    # retrieve the content of the entry using the title
    content = util.get_entry(title)

    # check if the form has been submitted
    if request.method == "POST":
        # create a form instance and populate it with data from the request
        form = EditEntryForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # retrieve the new content from the form
            new_content = form.cleaned_data['content']

            # save the updated entry content
            util.save_entry(title, new_content)

            # Convert the Markdown content to HTML
            html_content = md_to_html(title)

            # render the entry page with the updated content
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content,
            })

    # render the edit page with the existing content
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

# ---- end edit entry ----

# ---- start random entry ----

def random_entry(request):
    # get a list of all entries using the util module's list_entries function
    allEntries = util.list_entries()

    # choose a random entry from the list
    rand_entry = random.choice(allEntries)

    # convert the Markdown content of the random entry to HTML using md_to_html function
    html_content = md_to_html(rand_entry)

    # render the "entry.html" template with the title and HTML content of the random entry
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })

# ---- end random entry ----

