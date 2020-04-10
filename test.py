import re
string = '[List_of_countries_by_GDP_PPP|GDP (PPP)]1314324134-[3443431sad sd|ad]'

te = re.compile( r'(\[.*?\|.*?\])').findall(string)

print(te)