import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    dict_return = {}
    with open(filename, "r", encoding="utf-8") as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in file_reader: 
            key = row[keyfield]
            dict_return[key] = dict(row)
    return dict_return


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    list_of_tuples = []
    min_year = gdpinfo["min_year"]
    max_year = gdpinfo["max_year"]
    for year in range(int(min_year), int(max_year)+1):
        if str(year) in gdpdata and gdpdata[str(year)] != "":
            list_of_tuples.append((year, float(gdpdata[str(year)])))
    return list_of_tuples


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    plot_dict = {}
    nested_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo['country_name'],
                                           gdpinfo["separator"], gdpinfo["quote"])
    for country in country_list:
        if country in nested_dict:
            plot_dict[country] = build_plot_values(gdpinfo, nested_dict[country])
        else:
            plot_dict[country] = []
    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict = build_plot_dict(gdpinfo,country_list)
    result = []
    vals = plot_dict.values()
    for val in vals:
        for country in val:
            result.append(country)
    print(result)
    xyplot =  pygal.XY(height=400)
    xyplot.title = "GDP"
    xyplot.add("Data",result)
    xyplot.render_in_browser()
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")




test_render_xy_plot()
