from typing import Union, Tuple, List

class Parser:

    def __init__(self):
        self.emails = set()
        self.hosts = set()

    async def parse_dictionaries(self, results: dict) -> tuple:
        """
        Parse method to parse json results
        :param results: Dictionary containing a list of dictionaries known as selectors
        :return: tuple of emails and hosts
        """
        if results is None:
            return None, None
        for dictionary in results["selectors"]:
            field = dictionary['selectorvalue']
            if '@' in field:
                self.emails.add(field)
            else:
                field = str(field)
                if 'http' in field or 'https' in field:
                    field = field[8:] if field[:5] == 'https' else field[7:]
                self.hosts.add(field.replace(')', '').replace(',', ''))
        return self.emails, self.hosts


class Parser2:

    def __init__(self, word, text):
        self.word = word
        self.text = text
        self.hostnames = set()
        self.ips = set()

    def parse_text(self) -> Union[List, Tuple]:
        sub_domain_flag = 0
        self.text = str(self.text).splitlines()
        # Split lines to get a list of lines.
        for index in range(len(self.text)):
            line = self.text[index].strip()
            if '"ip":' in line:
                # Extract IP.
                ip = ''
                for ch in line[7:]:
                    if ch == '"':
                        break
                    else:
                        ip += ch
                self.ips.add(ip)
            elif '"subdomains":' in line:
                # subdomains start here so set flag to 1
                sub_domain_flag = 1
                continue
            elif sub_domain_flag > 0:
                if ']' in line:
                    sub_domain_flag = 0
                else:
                    if 'www' in self.word:
                        self.word = str(self.word).replace('www.', '').replace('www', '')
                    # Remove www from word if entered
                    self.hostnames.add(str(line).replace('"', '').replace(',', '') + '.' + self.word)
            else:
                continue
        return list(self.ips), list(self.hostnames)
