# Check Price
I made this script to get the prices of the product and waiting for them to get lower w/o opening the browser and 
searching for the product again and again..

Build using **python==3.7**

### Executing the script
Execute the script in terminal by **python check_price.py urls/urls.txt**<br>
Pass more than one url separated by a whitespace or a single text file containing the full urls on a separate line.

The scraped data will be stored as **prices.csv** file in the same directory.

Modules/Packages used:
- **requests**: to download the page's source code
- **BeautifulSoup4**: to scrape the data and extract the price and title of product
- **csv**: to store the data as csv file
- **sys**: to check the command line arguments
- **os**: to check the path of the file
- **re**: to get price cause the pattern changes for a regular product and a product in deal
- **datetime**: to store the date

Till now the script can only scrape the data from **https://www.amazon.in**
