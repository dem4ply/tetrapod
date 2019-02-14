import factory
import random
from faker import Factory as Faker_factory

from tetrapod.factories import _Dict_Date, _Dict_Partial_Date
from tetrapod.iei.factories.iei import IEI_with_results, IEI_no_results

fake = Faker_factory.create()


class IEI_Address_information(factory.Factory):
    message = factory.lazy_attribute(
        lambda x: "SSN IS VALID.  ISSUED IN {}".format(fake.state_abbr()))
    year = factory.lazy_attribute(
        lambda x: "IN THE YEAR {}".format(random.randint(1980, 2018)))
    records = factory.lazy_attribute(
        lambda x: {'record': IEI_Fact_Record.build_batch(
            random.randint(1, 5))})

    class Meta:
        model = dict


class IEI_Fact_Record(factory.Factory):
    sourceorjurisdiction = factory.lazy_attribute(
        lambda x: fake.sentence(nb_words=3))
    firstname = factory.lazy_attribute(
        lambda x: fake.first_name())
    lastname = factory.lazy_attribute(
        lambda x: fake.last_name())
    middlename = factory.lazy_attribute(
        lambda x: random.choice((fake.first_name(), '')))
    fullname = factory.lazy_attribute(
        lambda x: " ".join([x.firstname, x.middlename, x.lastname]))
    dob = factory.SubFactory(_Dict_Date)
    fulldob = factory.lazy_attribute(
        lambda x: "/".join([x.dob['month'], x.dob['day'], x.dob['year']]))
    ssn = factory.lazy_attribute(
        lambda x: fake.ssn().replace('-', ''))
    age = factory.lazy_attribute(lambda x: random.randint(21, 110))

    addresses = factory.lazy_attribute(
        lambda x: {'address': IEI_Fact_Address.build_batch(
            random.randint(1, 10))})

    class Meta:
        model = dict


class IEI_Fact_Address(factory.Factory):

    street_name = factory.lazy_attribute(
        lambda x: fake.street_name())
    street_number = factory.lazy_attribute(
        lambda x: fake.building_number())
    street_suffix = factory.lazy_attribute(
        lambda x: fake.street_suffix())

    fullstreet = factory.lazy_attribute(
        lambda x: fake.street_address())

    city = factory.lazy_attribute(lambda x: fake.city())
    state = factory.lazy_attribute(lambda x: fake.state_abbr())
    county = factory.lazy_attribute(lambda x: fake.city())
    from_date = factory.SubFactory(_Dict_Partial_Date)
    to_date = factory.SubFactory(_Dict_Partial_Date)
    zip = factory.lazy_attribute(lambda x: fake.postalcode())
    zip4 = factory.lazy_attribute(lambda x: fake.numerify(text="####"))
    street_pre_direction = factory.lazy_attribute(lambda x: fake.city_prefix())

    class Meta:
        model = dict


class IEI_Fact(IEI_with_results):
    addressinformation = factory.SubFactory(IEI_Address_information)


class IEI_Fact_no_results(IEI_no_results):
    addressinformation = factory.SubFactory(IEI_Address_information)
