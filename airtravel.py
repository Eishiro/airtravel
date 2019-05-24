"""Model for aircraft flights"""

class Flight:
    """A flight with a passenger aircraft"""

    def __init__(self,number,aircraft):

        #first 2 letters must be alphabet
        if not number[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(number))

        #first 2 letters must be capital alphabet
        if not number[:2].isupper():
            raise ValueError("Invalid airline code '{}'".format(number))

        #later than  2nd first letters must be digit and less than 9999
        if not (number[2:].isdigit() and int(number[2:]) <=9999):
            raise ValueError("Invalid route number '{}'".format(number))

        self._number = number
        self._aircraft = aircraft

        #Unpacking seating Plan --> initializing seats
        rows, seats = self._aircraft.seating_plan()
        #Create full seating map
        #first list entry to account for offset
        #Dictionary comprehensions and all is list comprehension
        #discard the row number with dummy variables
        self._seating = [None] + [ {letter :None for letter in seats} for _ in rows]


    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self,seat):
        """Parse a seat designator into a valid row and letter
        Args:
            seat: A seat designator such as 12F

        returns:
            A turple containing an integer and string for row and seat
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()

        #checking the input seat that exist in aircraft
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))

        row_text = seat[:-1]
        try:
            row =int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in row_numbers:
            raise ValueError("Invalid row number {}".format(row))

        return row,letter

    def allocate_seat(self,seat, passenger):
        """Allocate a seat to a passenger

        Args:
            seat:A seat designator such as "12C" or "21F"
            passenger: The passenger name

        Raise:
            ValueError :If the seat if unavailable

        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied.".format(seat))

        #Allocating
        self._seating[row][letter] = passenger

    def relocate_passenger(self,from_seat,to_seat):
        """Replicate a passenger to a differencet seat.

        Args:
            from_seat: The exisiting seat designator for the passenger to be moved
            to_seat: the new sewat designator
        """
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
                raise ValueError("No Passenger to reloicate in seat {}".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} already occupied". format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() is s is None)
                    for row in self._seating
                    if row is not None)


    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        """ An iterable series of passenger sewating allocations."""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row, letter))


class Aircraft:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registration

    def model(self):
        return self._model

    def seating_plan(self):
        return (range(1, self._num_rows + 1),
                "ABCDEFGHJK"[:self._num_seats_per_row])

def make_flight():
    f = Flight("AA123", Aircraft("Regist","Airbus", num_rows=22, num_seats_per_row=6) )
    f.allocate_seat("1A", "Eishiro Kinoshiat")
    f.allocate_seat("3C", "David")
    f.allocate_seat("7D", "Cathy")
    f.allocate_seat("8B", "Nuodrtouhh")
    return f

def console_card_printer(passenger, seat, flight_number, aircraft):
    output = "| Name {0}"       \
             "  Flight:{1}"     \
             "  Seat:{2}"       \
             "  Aircraft:{3}"   \
             " |".format(passenger, seat, flight_number, aircraft)
    banner = '+' + '-' * (len(output) - 2) + '+'
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()
