from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import query, session

Base = declarative_base()

class Country(Base):
    """
    A class representing a country table in the database.

    Attributes
    ----------
    name : str
        The name of the country. This attribute is the primary key.
    population : int
        The population of the country.
    ethnicity : str
        The main ethnicity group of the country.
    founding_year : int
        The year the country was founded.
    in_war : bool
        A boolean value indicating whether the country is currently at war.
    """

    __tablename__ = "Countries"


    name = Column("name", String, primary_key=True)
    population = Column("population", Integer)
    ethnicity = Column("ethnicity", String)
    founding_year = Column("founding_year", Integer)
    in_war = Column("in_war", Boolean)


    def __init__(self, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> None:
        """
        Constructor for the Country class.

        Parameters
        ----------
        name : str
            The name of the country.
        population : int
            The population of the country.
        ethnicity : str
            The main ethnicity group of the country.
        founding_year : int
            The year the country was founded.
        in_war : bool
            A boolean value indicating whether the country is currently at war.
        """
        self.name = name
        self.population = population
        self.ethnicity = ethnicity
        self.founding_year = founding_year
        self.in_war = in_war


    def __repr__(self) -> str:
        """
        Defines how the object should be represented as a string.

        Returns
        -------
        str
            A string representation of the object.
        """
        return f"(Country: {self.name}, current population: {self.population}, main ethnicity group: {self.ethnicity}, founded in {self.founding_year}, in war={self.in_war})"


    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary.

        Returns
        -------
        dict
            A dictionary representing the object.
        """
        return {"name": self.name, "population": self.population,
                "ethnicity":self.ethnicity, "founding_year": self.founding_year,
                "in_war": self.in_war}


def get_session():
    """
    Creates and returns a session instance for the database.

    Returns
    -------
    sqlalchemy.orm.session.Session
        A session instance for the database.
    """
    try:
        engine = create_engine("sqlite:///mydb.db", echo=False)
    except Exception as e:
        print("\n\Exception in creating database engine\n\n")
        return
    
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session_instance = Session()
    return session_instance

def add_value_to_db(session_instance: session.Session, name: str, population: int, ethnicity: str, founding_year: int , in_war: bool) -> bool:
    """Add a new country to the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        name (str): The name of the new country.
        population (int): The population of the new country.
        ethnicity (str): The ethnicity of the new country.
        founding_year (int): The year the new country was founded.
        in_war (bool): The war status of the new country.
        
    Returns:
        bool: True if the country was added successfully, False otherwise.
    """
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

def get_all_countries(session_instance: session.Session) -> list:
    """Get all countries from the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        
    Returns:
        list: A list of all countries in the database.
    """
    result = session_instance.query(Country).all()
    return result

def get_country_by_name(session_instance: session.Session, country_name: str) -> query:
    """Get a country by its name from the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        country_name (str): The name of the country to retrieve.
        
    Returns:
        Query: The country object matching the given name.
    """
    result = session_instance.query(Country).filter(Country.name == country_name)
    return result


def get_countries_by_ethnicity(session_instance: session.Session, ethnicity: str) -> list:
    """Get all countries with a certain ethnicity from the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        ethnicity (str): The ethnicity to filter by.
        
    Returns:
        list: A list of all countries with the specified ethnicity.
    """
    result = session_instance.query(Country).filter(Country.ethnicity == ethnicity).all()
    return result

def get_counties_by_war_status(session_instance: session.Session, in_war: bool) -> list:
    """Get all countries that are currently in war or not from the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        in_war (bool): True to retrieve countries currently in war, False to retrieve those not in war.
        
    Returns:
        list: A list of all countries with the specified war status.
    """
    result = session_instance.query(Country).filter(Country.in_war == in_war).all()
    return result

def get_counties_with_population_over_number(session_instance: session.Session, min_number_of_people: int) -> list:
    """Get all countries with a population greater than or equal to the specified value from the database.
    
    Args:
        session_instance (Session): A session instance used to communicate with the database.
        min_number_of_people (int): The minimum population value to filter by.
        
    Returns:
        list: A list of all countries with a population greater than or equal to the specified value.
    """
    result = session_instance.query(Country).filter(Country.population >= min_number_of_people).all()
    return result


def get_countries_founded_after_year(session_instance: session.Session, year: int) -> list:
    """
    This function takes a session instance and an integer year as inputs 
    and returns a list of Country objects that were founded after year.

    Args:
        session_instance (Session): An instance of the SQLAlchemy Session class.
        year (int): The year after which to filter the countries.

    Returns:
        list: A list of Country objects.

    """
    result = session_instance.query(Country).filter(Country.founding_year > year).all()
    return result


def change_country_name(session_instance: session.Session, old_name: str, new_name: str) -> bool:
    """
    This function takes a session instance, the old country name old_name, and the new country name new_name as inputs 
    and changes the name of the country in the database. 
    If the operation is successful, it returns True; otherwise, it returns False.

    Args:
        session_instance (Session): An instance of the SQLAlchemy Session class.
        old_name (str): The name of the country to be changed.
        new_name (str): The new name of the country.

    Returns:
        bool: True if the operation is successful; otherwise, False.

    """
    try:
        session_instance.query(Country).filter(Country.name == old_name).update({"name": new_name})
        session_instance.commit()
        return True
    except Exception as e:
        return False


def change_country_war_status(session_instance: session.Session, name: str, new_in_war: str) -> bool:
    """
    This function takes a session instance, the name of the country name, and a new boolean value new_in_war as inputs  
    and changes the war status of the country in the database. 
    If the operation is successful, it returns True; otherwise, it returns False.

    Args:
        session_instance (Session): An instance of the SQLAlchemy Session class.
        name (str): The name of the country whose war status is to be changed.
        new_in_war (str): The new war status of the country.

    Returns:
        bool: True if the operation is successful; otherwise, False.

    """
    try:
        session_instance.query(Country).filter(Country.name == name).update({"in_war": new_in_war})
        session_instance.commit()
        return True
    except Exception as e:
        return False


def change_country_population(session_instance: session.Session, name: str, new_population: int) -> bool:
    """
    This function takes a session instance, the name of the country name, and a new population value new_population as inputs  
    and changes the population of the country in the database. 
    If the operation is successful, it returns True; otherwise, it returns False.

    Args:
        session_instance (Session): An instance of the SQLAlchemy Session class.
        name (str): The name of the country whose population is to be changed.
        new_population (int): The new population of the country.

    Returns:
        bool: True if the operation is successful; otherwise, False.

    """
    try:
        session_instance.query(Country).filter(Country.name == name).update({"population": new_population})
        session_instance.commit()
        return True
    except Exception as e:
        return False
