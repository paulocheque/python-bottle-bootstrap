

# en-US,en;q=0.8,pt;q=0.6

def parse_AcceptLanguage(acceptLanguage):
  languages = acceptLanguage.split(",")
  locale_q_pairs = []

  for language in languages:
    if language.split(";")[0] == language:
      # no q => q = 1
      locale_q_pairs.append((language.strip(), "1"))
    else:
      locale = language.split(";")[0].strip()
      q = language.split(";")[1].split("=")[1]
      locale_q_pairs.append((locale, q))
  return locale_q_pairs


def simple_langs(acceptLanguage):
    'parse the Accept-Language header'
    langs = parse_AcceptLanguage(acceptLanguage)
    langs = [l[0][0:2] for l in langs]
    return list(set(langs))
