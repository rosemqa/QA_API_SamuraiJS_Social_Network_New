from faker import Faker

fake = Faker()


class Payloads:
    edit_profile_status = {'status': fake.sentence()}
    long_status_string = {'status': ''.join(fake.random_letters(301))}

    def edit_user_profile(self):
        return {
            'aboutMe': fake.sentence(),
            'contacts': {
                "facebook": fake.url(),
                'website': fake.url(),
                'vk': fake.url(),
                'twitter': fake.url(),
                'instagram': fake.url(),
                'youtube': fake.url(),
                'github': fake.url(),
                'mainLink': fake.url()
            },
            'lookingForAJob': fake.boolean(),
            'lookingForAJobDescription': fake.sentence(),
            'fullName': fake.user_name()
        }
