from __future__ import annotations

from io import BufferedReader
from re import compile, match, VERBOSE
from operator import itemgetter


class Sitzungsdienst:
    """
    This class represents the weekly assignments of a single
    PDF file as published by the Staatsanwaltschaft Freiburg
    """

    # Source as extracted from PDFs
    source = {}


    # Data as processed from source
    data = []


    # Data about express mode assignees
    express = []


    def __init__(self, input_file = None) -> None:
        """
        Parses & processes the given file object,
        storing the result as the `data` property
        """

        # If provided ..
        if input_file:
            # .. process PDF file object
            self.process_pages(input_file)

            # .. extract data from source
            self.extract_data()


    def process_pages(self, pdf_file) -> Sitzungsdienst:
        """
        Processes PDF content per-page,
        returning its contents per-date
        """

        # Import library
        import PyPDF2

        # Create page data list
        pages = []

        # Fetch content from PDF file
        for page in PyPDF2.PdfFileReader(pdf_file).pages:
            pages.append([text.strip() for text in page.extractText().splitlines() if text])

        # Reset global source
        self.source = {}

        # Initialize weekday buffer
        date = None

        # Reset global express mode data
        self.express = []

        # Extract data
        for page_count, page in enumerate(pages):
            if page_count == 0:
                # Express mode
                # (1) Activation
                is_express = False

                for index, text in enumerate(page):
                    # Skip if no express service
                    if text == 'Keine Einteilung':
                        break

                    # Determine express service ..
                    if text == 'Eildienst':
                        is_express = True

                        # .. and proceed with next entry
                        continue

                    # Skip
                    if text == 'Tag':
                        break

                    if is_express:
                        self.express.append(text)

            # Reset mode
            is_live = False

            for index, text in enumerate(page):
                # Determine starting point ..
                if text == 'Anfahrt':
                    is_live = True

                    # .. and proceed with next entry
                    continue

                # Determine terminal point ..
                if text == 'Seite':
                    is_live = False

                    # .. and proceed with next entry
                    continue

                # Enforce entries between starting & terminal point
                if not is_live or 'Ende der Auflistung' in text:
                    continue

                # Determine current date / weekday
                if text in ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']:
                    date = page[index + 1]

                    if date not in self.source:
                        self.source[date] = []

                    # Proceed with next entry
                    continue

                # Proceed with next entry if it indicates ..
                # (1) .. current date
                if text == date:
                    continue

                # (2) .. follow-up appointment for main trial
                if text in ['F', '+']:
                    continue

                self.source[date].append(text)

        return self


    def is_court(self, string: str) -> bool:
        """
        Checks whether string denotes a court
        """

        if match(r'(?:AG|LG)\s', string):
            return True

        return False


    def format_date(self, string: str, separator: str='-') -> str:
        """
        Reverts a given date using `separator` as separator
        """

        return separator.join(reversed(string.split('.')))


    def format_place(self, court: str, extra: str) -> str:
        """
        Turns court & additional information into something useful
        """

        string = court.replace(' ,', '').strip()

        if extra:
            string = '{} {}'.format(string, extra.strip())

        return string


    def format_people(self, string: str) -> str:
        """
        Makes a string of people human-readable
        """

        # Compile regular expression, using ..
        p = compile(r"""
            (?P<doc>(?:Dr\.)?)\s??                 # (1) .. doctoral degree (optional)
            (?P<last>[\u00C0-\u017F\w-]+)\s?       # (2) .. last name
            (?P<department>(?:\([0-9XIV]+\))?),\s  # (3) .. department number (optional)
            (?P<first>[\u00C0-\u017F\w-]+),\s      # (4) .. first name
            (?P<title>                             # (5) .. official title, being either ..
                (?:
                    # (a) .. (Erste:r / Ober-) Staatsanwalt:anwältin
                    # - OStA / OStA'in
                    # - EStA / EStA'in
                    # - StA / StA'in
                    # (b) .. (Erste:r) (Oberamts-) Anwalt:Anwältin
                    # - EOAA / EOAA'in
                    # - OAA / OAA'in
                    E?(?:O?StA|O?AA)|

                    # (c) .. Rechtsreferendar:in
                    # - Ref / Ref'in
                    #
                    # (d) .. Justizoberinspektor:in
                    # - JOI / JOI'in
                    #
                    # (e) .. Amtsanwaltsanwärter:in
                    # - AAAnw / AAAnw'in
                    Ref|JOI|AAAnw|

                    # (f) .. Regierungsrat:rätin als Amtsanwalt:anwältin
                    # - RRaAA / RR'inaAA'in
                    (?:RR(?:\'in)?aAA)
                )
                (?:\'in)?
                (?:\s\(ba\))?
            )
        """, VERBOSE)

        # Find matches
        matches = p.finditer(string)

        # If none found ..
        if not matches:
            # .. return original string
            return string

        # Create data array
        people = []

        for match in matches:
            # Clean strings & combine them
            people.append(' '.join([string.strip() for string in [
                    match.group('title'),
                    match.group('doc'),
                    match.group('first'),
                    match.group('last'),
                    match.group('department'),
                ] if string]
            ))

        # Bring people together
        return '; '.join(people)


    def extract_data(self) -> Sitzungsdienst:
        """
        Extracts data from PDF file, utilizing all of the
        above functions & returning the processed results
        """

        # Create data array
        unprocessed = []

        # Iterate over source data
        for date, raw in self.source.items():
            buffer = []
            court  = ''

            # Iterate over text blocks
            for index, text in enumerate(raw):
                if self.is_court(text):
                    court = text

                else:
                    buffer.append(text)

                if index == len(raw) - 1 or self.is_court(raw[index + 1]):
                    unprocessed.append({
                        'date': date,
                        'court': court,
                        'data': buffer,
                    })

                    # Reset buffer
                    buffer = []

        # Reset global data array
        self.data = []

        for item in unprocessed:
            events = []

            # Format data as string
            string = ' '.join(item['data']).replace(' ,', ',')

            # Compile regular expression, using ..
            p = compile(r"""
                (?P<where>(?:.*?)?\s??)                     # (1) .. location (optional)
                (?P<time>\d{2}:\s?\d{2})\s                     # (2) .. time of court date
                (?P<docket>\d{2,3}\sU?Js\s\d+\/\d{2})\s     # (3) .. docket number
                (?P<assigned>
                    (?:                                     # (4) .. name(s) of prosecutor(s), namely ..
                        (?:(?:Dr\.\s)?[\u00C0-\u017F\w-]+)  # (a) .. last name & doctoral degree (optional)
                        (?:\s(?:\([0-9XIV]+\)))?,\s         # (b) .. department number (optional)
                        (?:[\u00C0-\u017F\w-]+),\s          # (c) .. first name
                        (?:                                 # (d) .. official title
                            (?:
                                E?(?:O?StA|O?AA)|
                                Ref|JOI|AAAnw|
                                (?:RR(?:\'in)?aAA)
                            )
                            (?:\'in)?
                            (?:\s\(ba\))?
                        )\s?
                    )+
                )
            """, VERBOSE)

            # Find matches
            matches = p.finditer(string)

            # If none found ..
            if not matches:
                # .. proceed to next entry
                continue

            for match in matches:
                self.data.append({
                    'date': self.format_date(item['date']),
                    'when': match.group('time'),
                    'who': self.format_people(match.group('assigned')),
                    'where': self.format_place(item['court'], match.group('where')),
                    'what': match.group('docket'),
                })

        # Sort data
        self.data.sort(key=itemgetter('date', 'who', 'when', 'where', 'what'))

        return self


    def filter(self, query: list) -> list:
        """
        Filters the currently stored data by each
        `query`term, returning the search results
        """

        # Create data buffer
        data = []

        # Loop over search terms in order to ..
        for term in query:
            # .. filter out relevant items
            data += [item for item in self.data if term.lower() in item['who'].lower()]

        return data


    def date_range(self) -> tuple:
        """
        Determines date range for the currently stored data
        """

        return (self.data[0]['date'], self.data[-1]['date'])


    def express_service(self) -> list:
        # Fail early if no data on express service available
        if not self.express:
            return []

        # Combine data to string for easier regEx matching
        string = ' '.join(self.express).replace(' ,', ',')

        p = compile(r"""
            (?P<from>\d{2}\.\d{2}\.\d{4})\s             # (1) .. start date
            (?:-\s)                                     # (2) .. hyphen, followed by whitespace
            (?P<to>\d{2}\.\d{2}\.\d{4})\s               # (3) .. end date
            (?P<assigned>
                (?:                                     # (4) .. name(s) of prosecutor(s), namely ..
                    (?:(?:Dr\.\s)?[\u00C0-\u017F\w-]+)  # (a) .. last name & doctoral degree (optional)
                    (?:\s(?:\([0-9XIV]+\)))?,\s         # (b) .. department number (optional)
                    (?:[\u00C0-\u017F\w-]+),\s          # (c) .. first name
                    (?:                                 # (d) .. official title
                        (?:
                            E?(?:O?StA|O?AA)|
                            Ref|JOI|AAAnw|
                            (?:RR(?:\'in)?aAA)
                        )
                        (?:\'in)?
                        (?:\s\(ba\))?
                    )\s?
                )+
            )
        """, VERBOSE)

        # Find matches
        matches = p.finditer(string)

        # If none found ..
        if not matches:
            # .. return empty list
            return []

        # Create data buffer
        express = []

        for match in matches:
            express.append({
                'from': match.group('from'),
                'to': match.group('to'),
                'who': self.format_people(match.group('assigned')),
            })

        return express
