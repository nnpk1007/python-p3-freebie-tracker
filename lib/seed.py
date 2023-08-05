#!/usr/bin/env python3

# Script goes here!
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, company_dev

fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///freebies.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    #clear old data
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.query(company_dev).delete()

    # Add a console message so we can see output when the seed file runs
    print("Seeding data...")

    fake_companies = [
        {"name": "Goggle", "founding_year": 1998},
        {"name": "Amazon", "founding_year": 1994},
        {"name": "Facebook", "founding_year": 2004},
        {"name": "Tesla", "founding_year": 2003},
        {"name": "Nextflix", "founding_year": 1997},
    ]

    companies = [Company(name=fake_company["name"], founding_year=fake_company["founding_year"]) for fake_company in fake_companies]
    
    session.add_all(companies)
    session.commit()

    devs = [Dev(name=fake.name()) for _ in range(20)]
    session.add_all(devs)
    session.commit()

    fake_freebies = [
        {"item_name": "sticker", "value": 5},
        {"item_name": "T-shirt", "value": 25},
        {"item_name": "hat", "value": 15},
        {"item_name": "bag", "value": 20},
        {"item_name": "cup", "value": 10},
        ]

    freebies = []
    for company in companies:
        for dev in devs:
            dev = random.choice(devs)

            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()

            fake_freebie = random.choice(fake_freebies)
            freebie = Freebie(item_name=fake_freebie["item_name"], value=fake_freebie["value"], company_id=company.id, dev_id=dev.id)
            
            freebies.append(freebie)
            session.add(freebie)
            session.commit()
            
    session.close()