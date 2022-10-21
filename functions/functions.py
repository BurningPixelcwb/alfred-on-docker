from unicodedata import normalize
def clear_fields_from_xpath(spans, string_to_remove):
    # create a list of lines corresponding to element texts
    lines = [span.get_text() for span in spans]

    res = []
    for sub in lines:
        res.append(sub.replace(string_to_remove, ""))

    qnt = []
    for a in res:
        qnt.append(a.replace('\n', ''))

    clear_field = []
    for d in qnt:
        clear_field.append(d.replace(' ', ''))

    return clear_field

def clear_vl_unit(spans, string_to_remove):
    s = clear_fields_from_xpath(spans, string_to_remove)
    clear_field = [string.replace('\xa0', '') for string in s]

    return clear_field