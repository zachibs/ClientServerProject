from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import query, session

# declare a base for the database tables
Base = declarative_base()

# define a Country class that inherits from Base and represents a database table
class Country(Base):
    # set the table name
    __tablename__ = "Countries"

    # define columns of the table
    name = Column("name", String, primary_key=True)
    population = Column("population", Integer)
    ethnicity = Column("ethnicity", String)
    founding_year = Column("founding_year", Integer)
    in_war = Column("in_war", Boolean)

    # define the constructor for the class
    def __init__(self, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> None:
        self.name = name
        self.population = population
        self.ethnicity = ethnicity
        self.founding_year = founding_year
        self.in_war = in_war
    
    # define how the object should be represented as a string
    def __repr__(self) -> str:
        return f"(Country: {self.name}, current population: {self.population}, main ethnicity group: {self.ethnicity}, founded in {self.founding_year}, in war={self.in_war})"

    # define a method to convert the object to a dictionary
    def to_dict(self) -> dict:
        return {"name": self.name, "population": self.population,
                "ethnicity":self.ethnicity, "founding_year": self.founding_year,
                "in_war": self.in_war}

# define a function to create a session with the database
def get_session():
    try:
        engine = create_engine("sqlite:///mydb.db", echo=False)
    except Exception as e:
        print("\n\Exception in creating database engine\n\n")
        return
    
    # create all tables that are defined in the database
    Base.metadata.create_all(bind=engine)
    # create a session instance and return it
    Session = sessionmaker(bind=engine)
    session_instance = Session()
    return session_instance

# define a function to add a new country to the database
def add_value_to_db(session_instance: session.Session, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> bool:
    # create a new Country object
    country_instance = Country(name, population, ethnicity, founding_year, in_war)
    try:
        # check if the country already exists in the database
        if (get_country_by_name(session_instance, name)):
            print("Country already exist")
            return False
        # add the new country to the database and commit the transaction
        session_instance.add(country_instance)
        session_instance.commit()
        return True
    except Exception as e:
        # if there is an exception, rollback the transaction and return False
        session_instance.rollback()
        return False

# define a function to get all countries from the database
def get_all_countries(session_instance) -> list:
    result = session_instance.query(Country).all()
    return result

# define a function to get a country by its name
def get_country_by_name(session_instance: session.Session, country_name: str) -> query.Query:
    result = session_instance.query(Country).filter(Country.name == country_name)
    return result

# define a function to get all countries with a certain ethnicity
def get_countries_by_ethnicity(session_instance: session.Session, ethnicity: str) -> list:
    result = session_instance.query(Country).filter(Country.ethnicity == ethnicity).all()
    return result

# This function takes a session instance and a boolean value in_war as inputs 
# returns a list of Country objects that are currently in war (in_war is True) or not (in_war is False).
def get_counties_by_war_status(session_instance: session.Session, in_war: bool) -> list:
    result = session_instance.query(Country).filter(Country.in_war == in_war).all()
    return result

# This function takes a session instance and an integer min_number_of_people as inputs 
# returns a list of Country objects that have a population greater than or equal to min_number_of_people.
def get_counties_with_population_over_number(session_instance: session.Session, min_number_of_people: int) -> list:
    result = session_instance.query(Country).filter(Country.population >= min_number_of_people).all()
    return result

# This function takes a session instance and an integer year as inputs 
# returns a list of Country objects that were founded after year.
def get_countries_founded_after_year(session_instance: session.Session, year) -> list:
    result = session_instance.query(Country).filter(Country.founding_year > year).all()
    return result

# This function takes a session instance, the old country name old_name, and the new country name new_name as inputs 
# changes the name of the country in the database. 
# If the operation is successful, it returns True; otherwise, it returns False.
def change_country_name(session_instance: session.Session, old_name: str, new_name: str) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == old_name).update({"name": new_name})
        session_instance.commit()
        return True
    except Exception as e:
        return False

# This function takes a session instance, the name of the country name, and a new boolean value new_in_war as inputs 
# changes the war status of the country in the database. 
# If the operation is successful, it returns True; otherwise, it returns False.
def change_country_war_status(session_instance: session.Session, name: str, new_in_war: str) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == name).update({"in_war": new_in_war})
        session_instance.commit()
        return True
    except Exception as e:
        return False

# This function takes a session instance, the name of the country name, and a new population value new_population as inputs  
# changes the population of the country in the database. 
# If the operation is successful, it returns True; otherwise, it returns False.
def change_country_population(session_instance: session.Session, name: str, new_population: int) -> bool:
    try:
        session_instance.query(Country).filter(Country.name == name).update({"population": new_population})
        session_instance.commit()
        return True
    except Exception as e:
        return False
