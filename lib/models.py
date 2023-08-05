from sqlalchemy import ForeignKey, Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()

company_dev = Table(
    "company_devs",
    Base.metadata,
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("dev_id", ForeignKey("devs.id"), primary_key=True),
    extend_existing=False,
)


class Company(Base):

    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref=backref("company"))
    devs = relationship("Dev", secondary=company_dev, back_populates="companies")
    
    def __repr__(self):

        return f'<Company {self.name}>'
    
    # Company.give_freebie(dev, item_name, value) takes a dev (an instance of the Dev class), 
    # an item_name (string), and a value as arguments, 
    # and creates a new Freebie instance associated with this company and the given dev.
    def give_freebie(self, dev, item_name, value):

        freebie = Freebie(item_name=item_name, value=value, company_id=self.id,dev_id=dev.id)
        session.add(freebie)
        session.commit()

        return freebie
    
    # Class method Company.oldest_company()returns the Company instance with the earliest founding year.
    @classmethod
    def oldest_company(cls):
        
        return session.query(cls.name).order_by(cls.founding_year).limit(1).all()
        

class Dev(Base):

    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship("Freebie", backref=backref("dev"))
    companies = relationship("Company", secondary=company_dev, back_populates="devs")

    def __repr__(self):

        return f'<Dev {self.name}>'
    
    # Dev.received_one(item_name) accepts an item_name (string) and returns True 
    # if any of the freebies associated with the dev has that item_name, otherwise returns False.
    def received_one(self, item_name):

        items_owned_by_dev = session.query(Freebie).filter(Freebie.dev_id == self.id,
        Freebie.item_name == item_name).all()

        if items_owned_by_dev:
            return True
        
        return False
    
    # Dev.give_away(dev, freebie) accepts a Dev instance and a Freebie instance, 
    # changes the freebie's dev to be the given dev; your code should only make the change 
    # if the freebie belongs to the dev who's giving it away
    def give_away(self, dev, freebie):

        if self.id == freebie.dev_id:
            freebie.dev_id = dev.id
            session.commit()


class Freebie(Base):

    __tablename__ = "freebies"

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey("companies.id"))
    dev_id = Column(Integer(), ForeignKey("devs.id"))

    def __repr__(self):

        return f'<Freebie {self.item_name}'
    
    # Freebie.print_details()should return a string formatted as follows: 
    # {dev name} owns a {freebie item_name} from {company name}.
    def print_details(self):

        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"


# Copy and paste (line by line) the code under this line to IPDB to test (run seed.py before test)
# company = Company(name = "Costco", founding_year = 1961)
# session.add(company)
# session.commit()
# dev1 = Dev(name = "Khang Nguyen")
# session.add(dev1)
# session.commit()
# freebie = Company.give_freebie(company, dev1, "glass", 10)
# freebie.print_details()
# Company.oldest_company()
# Dev.received_one(dev1, "glass")
# Dev.received_one(dev1, "hat")
# dev2 = Dev(name = "Anthony Nguyen")
# session.add(dev2)
# session.commit()
# Dev.give_away(dev1, dev2, freebie)
# freebie.print_details()