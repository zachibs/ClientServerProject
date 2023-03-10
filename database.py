from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base



Base = declarative_base()
class Country(Base):
    __tablename__ = "Countries"

    name = Column("name", String, primary_key=True)
    population = Column("population", Integer)
    ethnicity = Column("ethnicity", String)
    founding_year = Column("founding_year", Integer)
    in_war = Column("in_war", Boolean)


    def __init__(self, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> None:
        self.name = name
        self.population = population
        self.ethnicity = ethnicity
        self.founding_year = founding_year
        self.in_war = in_war
    
    def __repr__(self) -> str:
        return f"(Country: {self.name}, current population: {self.population}, main ethnicity group: {self.ethnicity}, founded in {self.founding_year}, in war={self.in_war})"

    def to_dict(self) -> dict:
        return {"name": self.name, "population": self.population,
                "ethnicity":self.ethnicity, "founding_year": self.founding_year,
                "in_war": self.in_war}

def get_session():
    try:
        engine = create_engine("sqlite:///mydb.db", echo=False)
    except Exception as e:
        print("\n\Exception in creating database engine\n\n")
        return
    
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session_instance = Session()
    return session_instance
    


def add_value_to_db(session_instance, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> bool:
    country_instance = Country(name, population, ethnicity, founding_year, in_war)
    try:
        if (get_country_by_name(session_instance, name)):
            print("Country already exist")
            return False
        session_instance.add(country_instance)
        session_instance.commit()
        return True
    except Exception as e:
        session_instance.rollback()
        return False

def get_all_countries(session_instance):
    result = session_instance.query(Country).all()
    return result

def get_country_by_name(session_instance, country_name: str):
    result = session_instance.query(Country).filter(Country.name == country_name)
    return result

def get_countries_by_ethnicity(session_instance, ethnicity: str):
    result = session_instance.query(Country).filter(Country.ethnicity == ethnicity).all()
    return result

def get_counties_by_war_status(session_instance, in_war: bool):
    result = session_instance.query(Country).filter(Country.in_war == in_war).all()
    return result

def get_counties_with_population_over_number(session_instance, min_number_of_people: int):
    result = session_instance.query(Country).filter(Country.population >= min_number_of_people).all()
    return result


def get_countries_founded_after_year(session_instance, year):
    result = session_instance.query(Country).filter(Country.founding_year > year).all()
    return result

def change_country_name(session_instance, old_name: str, new_name: str) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == old_name).update({"name": new_name})
        session_instance.commit()
        return True
    except Exception as e:
        return False

def change_country_war_status(session_instance, name: str, new_in_war: str) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == name).update({"in_war": new_in_war})
        session_instance.commit()
        return True
    except Exception as e:
        return False

def change_country_population(session_instance, name: str, new_population: int) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == name).update({"population": new_population})
        session_instance.commit()
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    pass

