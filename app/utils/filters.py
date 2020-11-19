from app import app


@app.template_filter()
def pretty_number(number):
    """
    Add whitespace to string every 3 characters in Jinja2
    """
    list_nr = [i for i in reversed(str(number))]
    list_nr_three = ["".join(list_nr[i:i + 3]) for i in range(0, len(list_nr), 3)]
    str_nr = " ".join(list_nr_three)
    return str_nr[::-1]
