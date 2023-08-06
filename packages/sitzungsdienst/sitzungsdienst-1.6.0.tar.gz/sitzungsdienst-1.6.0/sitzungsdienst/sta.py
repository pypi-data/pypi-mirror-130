from io import BufferedReader
from re import compile, match, VERBOSE
from operator import itemgetter


class Sitzungsdienst:
    """
    This class represents the weekly assignments of a single
    PDF file as published by the Staatsanwaltschaft Freiburg
    """

    def __init__(self, input_file: BufferedReader) -> None:
        """
        Parses & processes the given file object,
        storing the result as the `data` property
        """

        self.data = self.extract_data(input_file)


    def process_pages(self, pages: list) -> dict:
        """
        Processes PDF content per-page,
        returning its contents per-date
        """

        # Create data array
        source = {}

        # Initialize weekday buffer
        date = None

        # Extract data
        for page in pages:
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

                    if date not in source:
                        source[date] = []

                    # Proceed with next entry
                    continue

                # Proceed with next entry if it indicates ..
                # (1) .. current date
                if text == date:
                    continue

                # (2) .. follow-up appointment for main trial
                if text in ['F', '+']:
                    continue

                source[date].append(text)

        return source


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

        return ' '.join([court.replace(' ,', '')]) + extra.strip()


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
                    # (b) .. (Erste:r) Oberamtsanwalt:anwältin
                    # - EOAA / EOAA'in
                    # - OAA / OAA'in
                    E?(?:O?StA|OAA)|

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


    def extract_data(self, pdf_file: BufferedReader) -> list:
        """
        Extracts data from PDF file, utilizing all of the
        above functions & returning the processed results
        """

        # Import library
        import PyPDF2

        # Create page data array
        pages = []

        # Fetch content from PDF file
        for page in PyPDF2.PdfFileReader(pdf_file).pages:
            pages.append([text.strip() for text in page.extractText().splitlines() if text])

        # Process data
        source = self.process_pages(pages)

        # Create data array
        unprocessed = []

        # Iterate over source data
        for date, raw in source.items():
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

        # Create data array
        data = []

        for item in unprocessed:
            events = []

            # Format data as string
            string = ' '.join(item['data']).replace(' ,', ',')

            # Compile regular expression, using ..
            p = compile(r"""
                (?P<where>(?:.*?)?\s??)                     # (1) .. location (optional)
                (?P<time>\d{2}:\d{2})\s                     # (2) .. time of court date
                (?P<docket>\d{2,3}\sU?Js\s\d+\/\d{2})\s     # (3) .. docket number
                (?P<assigned>
                    (?:                                     # (4) .. name(s) of prosecutor(s), namely ..
                        (?:(?:Dr\.\s)?[\u00C0-\u017F\w-]+)  # (a) .. first name & doctoral degree (optional)
                        (?:\s(?:\([0-9XIV]+\)))?,\s         # (b) .. department number (optional)
                        (?:[\u00C0-\u017F\w-]+),\s          # (c) .. last name
                        (?:                                 # (d) .. official title
                            (?:
                                E?(?:O?StA|OAA)|
                                Ref|JOI|AAAnw|
                                (?:RR(?:\'in)?aAA)
                            )
                            (?:\'in)?
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
                data.append({
                    'date': self.format_date(item['date']),
                    'when': match.group('time'),
                    'who': self.format_people(match.group('assigned')),
                    'where': self.format_place(item['court'], match.group('where')),
                    'what': match.group('docket'),
                })

        return sorted(data, key=itemgetter('date', 'who', 'when', 'where', 'what'))


    def filter(self, query: list) -> list:
        """
        Filters the currently stored data by each
        `query`term, returning the search results
        """

        # Create data buffer
        buffer = []

        # Loop over search terms in order to ..
        for term in query:
            # .. filter out relevant items
            buffer += [item for item in self.data if term.lower() in item['who'].lower()]

        # Apply data buffer
        return buffer


    def date_range(self) -> tuple:
        """
        Determines date range for the currently stored data
        """

        return (self.data[0]['date'], self.data[-1]['date'])
