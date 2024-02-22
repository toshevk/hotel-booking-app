import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df['id'] == self.hotel_id, "name"].squeeze()
        self.hotel_location = df.loc[df['id'] == self.hotel_id, "city"].squeeze()

    def available(self):
        # Check hotel availability
        availability = df.loc[df['id'] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        # Book a hotel by changing its availability
        df.loc[df['id'] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def view_hotel(self):
        pass


class Spa(Hotel):
    def book_spa_package(self):
        pass


class ReservationTicket:
    def __init__(self, guest_name, hotel_name):
        self.guest_name = guest_name
        self.hotel = hotel_name

    def generate_ticket(self):
        content = f"""
        Thank you for your reservation, {self.guest_name}! \n
        Feel free to contact us on our email for any questions
        regarding your stay at {self.hotel.hotel_name} in
        {self.hotel.hotel_location}
        """
        return content


class SpaTicket:
    def __init__(self, guest_name, hotel_name):
        self.guest_name = guest_name
        self.hotel = hotel_name

    def generate_spa_ticket(self):
        content = f"""
        Thank you for your SPA reservation, {self.guest_name}! \n
        Feel free to contact us on our email for any questions
        regarding your Spa-day at {self.hotel.hotel_name} in
        {self.hotel.hotel_location}
        """
        return content


class CreditCard:
    def __init__(self, acc_number):
        self.account_number = acc_number

    def validate(self, exp_date, holder, cvc):
        card_data = {"number": self.account_number,
                     "expiration": exp_date,
                     "holder": holder,
                     "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False

    def pay(self, price):
        pass


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security['number'] == self.account_number, "password"].squeeze()
        if password == given_password:
            return True


print(df)
requested_hotel_id = input("Enter the id of the hotel: ")
requested_hotel = Spa(requested_hotel_id)

if requested_hotel.available():
    guest_name = input("Enter your name: ")
    credit_card = SecureCreditCard(acc_number="1234567890123456")
    if credit_card.validate(exp_date="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            requested_hotel.book()
            reservation_ticket = ReservationTicket(guest_name=guest_name, hotel_name=requested_hotel)
            print(reservation_ticket.generate_ticket())

            spa_option = input("Do you wish to book a Spa package also? (y/n) ")
            spa_option.lower()
            if spa_option == "y":
                requested_hotel.book_spa_package()
                spa_ticket = SpaTicket(guest_name=guest_name, hotel_name=requested_hotel)
                print(spa_ticket.generate_spa_ticket())
        else:
            print("Credit card authentication failed.")
    else:
        print("There is a problem with your payment")
else:
    print("Sorry, this hotel is booked")
print("We look forward to welcoming you!")
