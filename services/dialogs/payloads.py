from faker import Faker

fake = Faker()


class Payloads:
    send_message = {'body': fake.sentence()}
