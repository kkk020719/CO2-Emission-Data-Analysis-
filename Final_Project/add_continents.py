#Kevin Zhao 260952439
def get_iso_codes_by_continent(filename):
    
    """
    (str) -> dict
    
    takes as input a string representing a filename of a file
    returns a  dictionary mapping continents’ names (all upper case) to a list of ISO codes (strings) of countries
    that belongs to that continent
    
    >>> d = get_iso_codes_by_continent("iso_codes_by_continent.tsv")
    >>> len(d['NORTH AMERICA'])
    23
    
    >>> d = get_iso_codes_by_continent("codes_of_provinces.tsv")
    >>> len(d['QUEBEC'])
    17
    
    >>> d = get_iso_codes_by_continent("continent__codes.tsv")
    >>> d['WONDERLAND'][1]
    'PYT'
    """
    
    continents = {}
    fobj = open(filename, "r", encoding="utf-8")
    for line in fobj:
        country = line.strip("\n").split("\t") #split by tabs
        if country[1].upper() in continents: #since first is iso codes and second one is continent
            continents[country[1].upper()].append(country[0])
        else:
            continents[country[1].upper()] = [country[0]]
    fobj.close()
    return continents

def add_continents_to_data(input_,continents_file,output_):
    
    """
    (str, str, str) -> int
    
    takes as input three strings representing file
    names, read from first two and write on the last file
    in the output file a column(3rd column)should be added
    with the continent to which each country belongs
    the continents are in the second file and the original data is stored in the first file
    Note that there are some countries that are considered to
    be part of two continents.
    For these countries, write both continents separated by a comma.
    The function should return an integer indicating the number of lines written to output_
    
    >>> add_continents_to_data("small_clean_co2_data.tsv", "iso_codes_by_continent.tsv",
    "small_co2_data.tsv")
    10
    >>> add_continents_to_data("data1.tsv", "iso_codes_by_continent.tsv",
    "data2.tsv")
    10232
    >>> add_continents_to_data("read_here.tsv", "continent_codes_mars.tsv",
    "write_here.tsv")
    55
    """
    
    input_file = open(input_, "r", encoding="utf-8")
    output_file = open(output_, "w", encoding="utf-8")
    line_count = 0
    its_continent = ''
    continents = get_iso_codes_by_continent(continents_file)
    for line in input_file:
        split = line.split('\t')
        for continent in continents:
            if split[0] in continents[continent]:
                its_continent += continent + "," #seperate them by a comma
        final = its_continent.strip(",") #reduce extra commas
        split.insert(2, final) #adds to the third column
        output_file.write('\t'.join(split))
        its_continent = ''
        line_count += 1
    return line_count
        
        