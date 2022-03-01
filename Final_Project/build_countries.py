#Kevin Zhao 260952439
import copy

class Country:
    
    """
    This class represents a country including its data information as follows
    Instance attributes: iso_code (a string), name (a string), continents (a list of strings),
    co2_emissions (a dictionary mapping integers to floats), population (a dictionary mapping integers to integers)
    Class attributes: min_year_recorded (an integer), max_year_recorded (an integer).
    These indicate the lowest and highest year (respectively) for which we have data recorded of all countries that have been created.
    """
    
    min_year_recorded = float('inf')
    max_year_recorded = float('-inf')
    
    def __init__(self, iso, country_name, continents, the_year, emissions, population):
        
        """
        (Country, str, str, list, dict, dict) -> Country
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> r.iso_code
        'RUS'
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.name
        'Qatar'
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> p.continents
        ['EUROPE']
        """
        
        co2 = {}
        pop = {}
        if emissions != -1:
            co2[the_year] = emissions
        if population != -1:
            pop[the_year] = population
        if len(iso) != 3 and  iso != 'OWID_KOS':
            raise AssertionError("Invalid ISO code")
        self.iso_code = iso
        self.name = country_name
        self.continents = copy.deepcopy(continents) #creating a deepcopy
        self.co2_emissions = co2
        self.population = pop
        
        if the_year < Country.min_year_recorded: #recording the min and max year
            Country.min_year_recorded = the_year
        if the_year > Country.max_year_recorded:
            Country.max_year_recorded = the_year
        
    def __str__(self):
        
        """
        (Country) -> str
        
        returns a string representation of a country containing the name,
        the continents (separated by a comma if more than one),
        and a string representation of both the co2_emissions dictionary and the population dictionary.
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> str(r)
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> str(d)
        'Qatar\tASIA\t{1971: 1000.778}\t{1971: 14230000}'
        
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> str(p)
        'Denmark\tEUROPE\t{1906: 6.544}\t{1906: 2746271}'
        """
        
        return self.name + "\t" + ",".join(self.continents) + "\t" + str(self.co2_emissions) + "\t" + str(self.population)
    
    def add_yearly_data(self, info):
        
        """
        (Country, str) -> NoneType
        
        takes as input a string with the year,co2 emissions,and population, all separated by a tab.
        This method updates the appropriate attributes of the country.
        Note that if the co2 emission or the population data is an empty column,
        then no changes should be made to the corresponding attribute.
        (updates the min_year_recorded and max_year_recorded)
        
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.co2_emissions == {1949: 0.015, 2018: 9.439}
        True
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> d.co2_emissions
        {1971: 1000.778, 1990: 19.439}
        
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> p.add_yearly_data("2020\\t\\t")
        >>> p.population
        {1906: 2746271}
        """
        
        update = info.strip('\n').split('\t')
        if update[1] != "": #will not update if these are empty columns
            self.co2_emissions[int(update[0])] = float(update[1])
        if update[2] != "":
            self.population[int(update[0])] = int(update[2])
        if int(update[0]) < Country.min_year_recorded:
            Country.min_year_recorded = int(update[0])
        if int(update[0]) > Country.max_year_recorded:
            Country.max_year_recorded = int(update[0])
        
    def get_co2_emissions_by_year(self, year):
        
        """
        (Country, int) -> num
        
        takes an integer(year) as input.
        It returns the co2 emission of the country in the specified year if available.
        It returns 0.0 otherwise.
        
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.get_co2_emissions_by_year(1949)
        0.015
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> d.get_co2_emissions_by_year(1989)
        0.0
        
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> p.get_co2_emissions_by_year(1906)
        6.544
        """
        
        
        if year in self.co2_emissions: #returns the emission if the year was recorded
            return self.co2_emissions[year]
        else:
            return 0.0
    
    def get_co2_per_capita_by_year(self, year):
        
        """
        (Country, int) -> num
        
        takes an integer(year) as input. It return the co2 emission per capita in tonnes for the specified year if available.
        If either the co2 emissions or the population of the country are not available for the specified year,
        the method returns None.
        
        >>> a = Country("AFG", "Afghnistan", ["ASIA"], 1949, -1, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> round(a.get_co2_per_capita_by_year(2018), 5)
        0.25427
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> d.get_co2_per_capita_by_year(2018)
        None
        
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> p.get_co2_per_capita_by_year(1906)
        2.3828675320097688 
        """
        
        if year not in self.co2_emissions or year not in self.population: #checks whether the year was recorded
            return None
        co2 = self.get_co2_emissions_by_year(year)
        return (co2 * 1000000)/self.population[year]

    def get_historical_co2(self, year):
        
        """
        (Country, int) -> num
        
        takes an integer(year) as input.
        It return the historical (total) co2 emission in millions of tonnes that the country has produced for all years up to
        and including the specified year.
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> q.get_historical_co2(2000)
        45.277
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> d.get_historical_co2(2000)
        1020.217
        
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> p.get_historical_co2(2000)
        6.544
        """
        
        total = 0.0
        for years in self.co2_emissions:
            if years <= year: #check if the year is before the setted integer(year)
                total += self.co2_emissions[years]
        return total
    
    @classmethod
    def get_country_from_data(cls, data):
        
        """
        (type, str) -> Country
        
        takes as input a string which has the format of iso code, country, continent, year, co2 emission and population(seperated by tab)
        The method should return a new Country object created from the data in the input string.
        
        >>> a = Country.get_country_from_data("ALB\\tAlbania\\tEUROPE\\t1991\\t4.283\\t3280000")
        >>> str(a)
        'Albania\tEUROPE\t{1991: 4.283}\t{1991: 3280000}'
        
        >>> p = Country.get_country_from_data('RUS\\tRussia\\tASIA,EUROPE\\t2007\\t1604.778\\t14266000')
        >>> str(p)
        'Russia\tASIA,EUROPE\t{2007: 1604.778}\t{2007: 14266000}'
        
        >>> i = Country.get_country_from_data('QAT\\tQatar\\tASIA\\t1971\\t1000.778\\t14230000')
        >>> str(i)
        'Qatar\tASIA\t{1971: 1000.778}\t{1971: 14230000}'
        """
        
        split = data.strip('\n').split('\t')#making a list with those items
        continent_list = []
        for continents in split[2].split(","): #in case of continents presented like "ASIA,EUROPE" and this would be one str in a list
            continent_list.append(continents)
        if split[4] == "" and split[5] == "": #the case when empty co2 and population
            return cls(split[0],split[1],continent_list,int(split[3]),-1,-1)
        elif split[4] == "": #empty co2 emission
            return cls(split[0],split[1],continent_list,int(split[3]),-1,int(split[5]))
        elif split[5] == "": #empty population
            return cls(split[0],split[1],continent_list,int(split[3]),float(split[4]),-1)
        else:
            return cls(split[0],split[1],continent_list,int(split[3]),float(split[4]),int(split[5]))

    @staticmethod
    def get_countries_by_continent(countries):
        
        """
        (list) -> dict
        
        takes input a list of countries and returns a dictionary mapping a string representing a continent to a list of countries
        which belong to that country
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> d = Country.get_countries_by_continent(c)
        >>> str(d['ASIA'][1])
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> cc = [d,p]
        >>> k = Country.get_countries_by_continent(cc)
        >>> str(k['ASIA'][0])
        'Qatar\tASIA\t{1971: 1000.778, 1990: 19.439}\t{1971: 14230000}'
        
        >>> kp = Country("IRN", "Iran", ["ASIA"], 2018, 720.414, 81800000)
        >>> pd = Country("RUS",	"Russia",	["ASIA","EUROPE"],	1971,	1533.262,	130831000)
        >>> l = [kp,pd]
        >>> y = Country.get_countries_by_continent(l)
        >>> str(y['ASIA'][0])
        'Iran\tASIA\t{2018: 720.414}\t{2018: 81800000}'
        """
        
        result = {}
        for country in countries:
            for str_continent in country.continents:
                for continent in str_continent.split(","): #in case many continents are in one string
                    if continent in result:
                        result[continent].append(country)
                    else:
                        result[continent] = [country]
        return result
        
    @staticmethod
    def get_total_historical_co2_emissions(countries, year):
        
        """
        (list, int) -> float
        
        takes as input a list of countries
(i.e., objects of type Country) and an integer representing a year.
        returns a float
 representing the total co2 emissions (in millions of tonnes)
        produced by all the countries in the
 input list for all years up to and including the specified year.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> Country.get_total_historical_co2_emissions(c, 2007)
        1608.717
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> cc = [d,p]
        >>> Country.get_total_historical_co2_emissions(cc, 1990)
        1026.761
        
        >>> kp = Country("IRN", "Iran", ["ASIA"], 2018, 720.414, 81800000)
        >>> pd = Country("RUS",	"Russia",	["ASIA","EUROPE"],	1971,	1533.262,	130831000)
        >>> l = [kp,pd]
        >>> Country.get_total_historical_co2_emissions(l, 1971)
        1533.262
        """
        
        total = 0
        for country in countries: 
            total += country.get_historical_co2(year)#using a method created before to calculate individual emissions
        return total
        
    @staticmethod
    def get_total_co2_emissions_per_capita_by_year(countries, year):
        
        """
        (list, int) -> float
        
        takes as input a list of countries
(i.e., objects of type Country) and an integer representing a year.
        returns 
the co2 emissions per capita in tonnes produced by the countries in the given list in the specified 
year.
        if the total co2 or the
total population is 0, then the function should return 0.0.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> Country.get_total_co2_emissions_per_capita_by_year(c, 2007)
        92.98855491329479
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> cc = [d,p]
        >>> Country.get_total_co2_emissions_per_capita_by_year(cc, 1990)
        0.0
        
        >>> kp = Country("IRN", "Iran", ["ASIA"], 2018, 720.414, 81800000)
        >>> pd = Country("RUS",	"Russia",	["ASIA","EUROPE"],	1971,	1533.262,	130831000)
        >>> l = [kp,pd]
        >>> Country.get_total_co2_emissions_per_capita_by_year(l, 1971)
        11.719409008568306
        """
        
        total = 0.0
        population = 0.0
        for country in countries:
            #not considering if no population or no emission recorded
            if year not in country.co2_emissions or year not in country.population:
                continue
            total += country.co2_emissions[year]
            population += country.population[year]
        try: #the case when no data fits in the specified year
            return (total * 1000000)/population
        except ZeroDivisionError:
            return 0.0
        
    @staticmethod
    def get_co2_emissions_per_capita_by_year(countries, year):
        
        """
        (list, int) -> dict
        
        takes as input a list of countries
(i.e., objects of type Country) and an integer representing a year.
        returns a 
dictionary mapping objects of type Country to floats representing the co2 emissions per capita in
 tonnes
        produced by the country in the specified year.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> d = Country.get_co2_emissions_per_capita_by_year(c,2007)
        >>> len(d)
        3
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> cc = [d,p]
        >>> ppp = Country.get_co2_emissions_per_capita_by_year(cc, 1990)
        >>> print(ppp[d])
        None
        
        >>> kp = Country("IRN", "Iran", ["ASIA"], 2018, 720.414, 81800000)
        >>> pd = Country("RUS",	"Russia",	["ASIA","EUROPE"],	1971,	1533.262,	130831000)
        >>> l = [kp,pd]
        >>> pppp = Country.get_co2_emissions_per_capita_by_year(l, 1971)
        >>> pppp[pd]
        11.719409008568306
        """
        
        co2_emissions = {}
        for country in countries:
            co2_emissions[country] = country.get_co2_per_capita_by_year(year) #using method created before to get co2 emission
        return co2_emissions
            
    @staticmethod
    def get_historical_co2_emissions(countries, year):
        
        """
        (list, int) -> dict
        
        takes as input a list of countries
(i.e., objects of type Country) and an integer representing a year.
        returns a dictionary 
mapping objects of type Country to floats representing the total co2 emissions (in millions of 
tonnes)
        produced by that country for all years up to and including the specified year.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        
>>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> c = [b, r, q]
        >>> d1 = Country.get_historical_co2_emissions(c,2007)
        >>> len(d1)
        3
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> d2 = Country.get_historical_co2_emissions(c,2007)
        >>> d2[b]
        3.924
        
        >>> d = Country("QAT", "Qatar", ["ASIA"], 1971, 1000.778, 14230000)
        >>> d.add_yearly_data("1990\\t19.439\\t")
        >>> p = Country("DNK",	"Denmark",	["EUROPE"],	1906,	6.544,	2746271)
        >>> cc = [d,p]
        >>> ppp = Country.get_historical_co2_emissions(cc, 1990)
        >>> ppp[d]
        1020.217
        """
        
        co2_emissions = {}
        for country in countries:
            co2_emissions[country] = country.get_historical_co2(year)#using previous method to calculate individual historical emission
        return co2_emissions
    
    @staticmethod
    def get_top_n(countries, n):
        
        """
        (dict, int) -> list
        
        takes as input a dictionary mapping objects of type Country
 to numbers, and an integer n.
        returns a list of tuples
        Each tuple is made up by the
 iso code of a country and the number to which the country is mapped in the input dictionary.
        Only
 the countries that map to the top n values should appear in the list.
        The tuples in the list should 
appear sorted on the values in descending order.
        If there are countries that map to the same values,
        the countries should be compared based on the alphabetical order of their names.
        
        >>> a = Country("ALB", "Albania", [], 0, 0.0, 0)
        >>> b = Country("AUT", "Austria", [], 0, 0.0, 0)
        >>> c = Country("BEL", "Belgium", [], 0, 0.0, 0)
        >>> d = Country("BOL", "Bolivia", [], 0, 0.0, 0)
        >>> e = Country("BRA", "Brazil", [], 0, 0.0, 0)
        >>> d = {a: 5, b: 5, c: 3, d: 10, e: 3}
        >>> t = Country.get_top_n(d, 10)
        >>> t
        [('BOL', 10), ('ALB', 5), ('AUT', 5), ('BEL', 3), ('BRA', 3)]
        
        >>> aa = Country("RUS", "Russia", [], 0, 0.0, 0)
        >>> bb = Country("LBY", "Libya", [], 0, 0.0, 0)
        >>> cc = Country("COM", "Comoros", [], 0, 0.0, 0)
        >>> dd = {aa:0, bb:80, cc:3}
        >>> tt = Country.get_top_n(dd, 2)
        >>> tt
        [('LBY', 80), ('COM', 3)]
        
        >>> aaa = Country("PER",	"Peru", [], 0, 0.0, 0)
        >>> bbb = Country("VNM", "Vietnam", [], 0, 0.0, 0)
        >>> ddd = {aaa:99, bbb:98}
        >>> ttt = Country.get_top_n(ddd,1)
        >>> ttt
        [('PER', 99)]
        """
        
        result = []
        numbers = {}
        names = []
        number_rank = []
        
        #making a dictionary with keys being the number each country maps to
        #and items being a list of country object that shares the same key value
        for country in countries:
            if countries[country] in numbers:
                numbers[countries[country]].append(country)
            else:
                numbers[countries[country]] = [country]
        #making a list of those values
        all_the_nums = list(countries.values())
        for the_number in all_the_nums: #checking whether there are None which means original data(co2,population) wasn't recorded
            if the_number == None:
                continue
            number_rank.append(the_number)
        number_rank.sort() #sort the numbers in order
        for number in number_rank[::-1]: #iterating backwards
            for the_country in numbers[number]:
                names.append(the_country.name) #making a list with the country name that has the same value 
            small_alphabet = min(names)#finding the name that comes first in terms of alphabet order(country name)
            result.append(((numbers[number][names.index(small_alphabet)]).iso_code, number))#appending the smallest alphabet's iso code
            del numbers[number][names.index(small_alphabet)]
            names = []
        if len(result) > n:#keeping the top n values
            del result[n:]
        return result

def get_countries_from_file(filename):
    
    """
    (str) -> dict
    
    takes as input a string representing a filename
    which has exactly the same format as
 the output file generated by the function add_continents_to_data
    "NPL\\tNepal\\tASIA\\t2009\\t4.191\\t26884000"
    creates and return a
 dictionary mapping ISO country codes (strings) to objects of type Country based on the data in the file.
    
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> len(d2)
    193
    
    >>> d1 = get_countries_from_file("large_mars_data.tsv")
    >>> str(d1['BAY'])
    'Baybya\\tWONDERLAND\\t{2002: 3.748}\\t{2002: 3126000}'
    
    >>> d3 = get_countries_from_file("read_files.tsv")
    >>> len(d3)
    3
    """
    
    ISO_dict = {}
    fobj = open(filename, "r", encoding="utf-8")
    for line in fobj:
        split = line.strip('\n').split('\t')
        if split[0] in ISO_dict: #using the method add_yearly_data to add the data if same country
            ISO_dict[split[0]].add_yearly_data(split[3] + '\t' + split[4] + '\t' + split[5])
        else: #using the method created before to create a Country object
            ISO_dict[split[0]] = Country.get_country_from_data(line)
    return ISO_dict
            