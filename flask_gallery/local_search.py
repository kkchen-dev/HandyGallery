def build_key_phraseset(phrase):
    symbol_set = {"[", "]", "(", ")", ",", 
                  "?", ";", "{", "}", "-", 
                  "!", "@", "*", "$", "&", 
                  ":", "'", "\"", ".", "=", 
                  "<", ">", "/", "\\", "|",
                  "+", "`"," "}
    phraseset, curr_chars = set(), []
    for c in phrase:
        if curr_chars and c in symbol_set:
            phraseset.add("".join(curr_chars))
            curr_chars = []
        elif c not in symbol_set:
            curr_chars.append(c)
    if curr_chars:
        phraseset.add("".join(curr_chars))
    return phraseset


def sliding_window(a, b):
    if len(a) == 0:
        return True
    lena, lenb = len(a), len(b)
    for i in range(lenb):
        for j in range(lena):
            if i + j >= lenb or (i + j < lenb and b[i+j] != a[j]):
                break
        else:
            return True
    return False


def as_all_in_bs(a_s, b_s):
    localas = [a.lower() for a in a_s]
    localbs = [b.lower() for b in b_s]
    match_count = 0
    
    for a in localas:
        match = False
        for b in localbs:
            if sliding_window(a, b):
                match = True
                break
        match_count += match
    return 0 < len(localas) == match_count


def title_found(book_title, search_phrase):
    search_phrases = build_key_phraseset(search_phrase)
    if not search_phrases:
        return False
    title_phrases = build_key_phraseset(book_title)
    return as_all_in_bs(search_phrases, title_phrases)