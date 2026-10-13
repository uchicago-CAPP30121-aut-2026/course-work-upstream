This directory contains sample cities and sample for-sale lists.

sample-writeup.txt: sample city from the writeup

sample-writeup-1-0.65-1.txt, sample-writeup-1-0.65-1-for-sale.txt: the city and for-sale lists that
  result from running do_simulation with:

  - sample city from the writeup
  - R of 1
  - target score of 0.65
  - a maximum of one step

  To run this test in ipython run:
  
    city = utility.load_city_file('sample_cities/sample-writeup.txt')
    for_sale = utility.find_homes_for_sale(city)
    schelling.do_simulation(city, for_sale, 1, 0.65, 1)
  
sample-writeup-1-0.65-10.txt, sample-writeup-1-0.65-10-for-sale.txt: the city and for-sale lists that
  result from running do_simulation with:

  - sample city from the writeup
  - R of 1
  - target score of 0.65
  - a maximum of ten steps

  To run this test in ipython run:
  
    city = utility.load_city_file('sample_cities/sample-writeup.txt')
    for_sale = utility.find_homes_for_sale(city)
    schelling.do_simulation(city, for_sale, 1, 0.65, 10)


grid-blue-stripe.txt: a 5x5 city with a stripe of blue homeowners. Used in the medium tests

grid-sea-of-red.txt: a 5x5 city that has mostly maroon homeowners. Used in th medium tests

grid-ten: a 10x10 city.  Used in the medium tests

large-grid.txt: a 40x40 city.  Used in the large tests

README.txt: this file
