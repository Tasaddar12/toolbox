import re

class HTTPParse:
    '''Parse rawdomain'''
    def rawdomain_parse(url):
        '''Prepare domain'''
        url = re.sub(r"^(https://|http://)", "", url); url = re.split(r"\/", url);
        url = url[0];
        url = re.split(r"\.", url)
        domain = url
        '''Return domain'''
        return((domain[domain.__len__()-2]) + "." + domain[domain.__len__()-1])

