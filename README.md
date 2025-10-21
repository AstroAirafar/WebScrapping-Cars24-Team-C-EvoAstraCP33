# Cars24 Used Car Data Analysis - Team C Mini Project

This project focuses on **web scraping**, **data cleaning**, and **exploratory data analysis (EDA)** of used car listings from the Cars24 website. The goal is to extract Hyundai car listings, clean and process the data, and perform comprehensive visualizations to uncover insights about pricing trends, fuel types, transmission types, and more.

---

## Table of Contents
1. [Understanding the Dataset](#understanding-the-dataset)
2. [Data Extraction](#data-extraction)
3. [Web Scraping](#web-scraping)
4. [Data Preprocessing and Cleaning](#data-preprocessing-and-cleaning)
5. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
6. [Visualizations](#visualizations)
7. [Technologies Used](#technologies-used)
8. [How to Run](#how-to-run)

---

## Understanding the Dataset

The dataset is scraped from **Cars24.com** and contains used car listings specifically for **Hyundai** vehicles. The dataset includes the following features:

- **Car_Name**: Model name of the car
- **Year**: Year of manufacture
- **Kilometers_Driven**: Total kilometers the car has been driven
- **Fuel_Type**: Type of fuel (Petrol, Diesel, CNG, Electric, Hybrid)
- **Transmission**: Transmission type (Manual, Automatic)
- **Price(INR)**: Listing price in Indian Rupees

The raw data is extracted from dynamic web pages using Selenium WebDriver, which handles JavaScript-rendered content and pagination.

---

## Data Extraction

### Extraction Function
A custom `extract_car_data()` function was developed to parse the text content from each car listing element. The function uses **regular expressions** to identify and extract:

- **Year**: 4-digit year (19xx or 20xx)
- **Car Name**: Full model name including year
- **Kilometers Driven**: Distance values with units (km, k, lakh)
- **Fuel Type**: Petrol, Diesel, CNG, Electric, Hybrid
- **Transmission**: Manual or Automatic
- **Price**: Price in Indian Rupees (₹) with lakh notation

The extraction handles various text formats and edge cases to ensure robust data collection.

---

## Web Scraping

### Tools and Approach
- **Selenium WebDriver** with Chrome in headless mode
- **Dynamic scrolling** to load all available listings
- **Pagination handling** by detecting and clicking "Next" buttons
- **Iterative loading** with scroll detection to ensure all cars are loaded

### Scraping Process
1. Navigate to Cars24 Hyundai listings page
2. Scroll through the page incrementally (300px at a time)
3. Detect and click pagination buttons ("Next", "Load More")
4. Monitor car count to detect when all listings are loaded
5. Extract text content from all car listing elements
6. Parse extracted text using the extraction function
7. Save data to CSV format

The scraper implements multiple strategies to handle dynamic content:
- Multiple scroll methods (incremental, full page, container-specific)
- Button detection using various XPath selectors
- Click fallback mechanisms (standard click, JavaScript click)
- Iteration limits to prevent infinite loops
- Change detection to know when all content is loaded

---

## Data Preprocessing and Cleaning

### Initial Data Loading
The scraped data is saved as `Cars24_DataSet.csv` and loaded into a pandas DataFrame for processing.

### Cleaning Operations

#### 1. **Car Name Cleaning**
Remove year prefix from car names using regex:
```python
df['Car_Name'] = df['Car_Name'].str.replace(r'^\d{4}\s+', '', regex=True)
```

#### 2. **Kilometers Driven Conversion**
Convert various formats to standard numeric values:
- Handle thousands (k, K) → multiply by 1,000
- Handle lakhs (L, lakh) → multiply by 100,000
- Convert to integer type

```python
def clean_kilometers(value):
    # Handles: "50k km", "1.2 lakh km", "75000 km"
    # Returns: standardized integer values
```

#### 3. **Price Conversion**
Standardize price formats and convert to INR:
- Remove currency symbols (₹) and commas
- Handle lakhs → multiply by 100,000
- Handle crores → multiply by 10,000,000
- Rename column to `Price(INR)`

```python
def clean_price(value):
    # Handles: "₹3.35 lakh", "₹5.5 lakh", etc.
    # Returns: numeric value in INR
```

### Refined Dataset
The cleaned dataset is saved as `Refined_Cars24_DataSet.csv` with consistent data types and formats.

---

## Exploratory Data Analysis (EDA)

### Dataset Information
- **Shape**: Analysis of total rows and columns
- **Data Types**: All numeric and categorical columns properly typed
- **Missing Values**: Check using `isnull().sum()`
- **Duplicate Records**: Verification using `duplicated().sum()`
- **Unique Values**: Count of unique entries per column using `nunique()`

### Descriptive Statistics
Using `df.describe()` to get:
- **Count, Mean, Std**: Statistical measures for numeric features
- **Min, 25%, 50%, 75%, Max**: Distribution quartiles
- Key insights about:
  - **Year**: Manufacturing year distribution
  - **Kilometers_Driven**: Mileage patterns
  - **Price(INR)**: Pricing ranges and outliers

### Additional Analysis
The notebook also explores:
- **Car Age**: Calculated as `current_year (2025) - Year`
- **Price per Kilometer**: Calculated as `Price(INR) / Kilometers_Driven`

---

## Visualizations

The project includes **9 comprehensive visualizations** using Matplotlib and Seaborn:

### 1. **Distribution of Car Prices**
- Histogram with KDE (Kernel Density Estimation)
- Shows price distribution and density
- Identifies most common price ranges

### 2. **Count of Cars by Fuel Type**
- Count plot showing distribution across fuel types
- Reveals market composition (Petrol vs Diesel vs CNG)

### 3. **Count of Cars by Transmission Type**
- Comparison of Manual vs Automatic transmissions
- Market preference insights

### 4. **Average Price by Fuel Type**
- Bar plot showing mean prices for each fuel type
- Identifies premium fuel type categories

### 5. **Boxplot of Car Prices by Year**
- Price distribution across manufacturing years
- Shows depreciation trends and outliers
- Year-wise price variance

### 6. **Scatter Plot: Kilometers Driven vs Price**
- Relationship between mileage and pricing
- Color-coded by fuel type
- Shows depreciation patterns with usage

### 7. **Correlation Heatmap**
- Correlation matrix for numeric features
- Identifies relationships between:
  - Year and Price
  - Kilometers_Driven and Price
  - Year and Kilometers_Driven

### 8. **Top 10 Most Common Car Models**
- Bar chart of most frequently listed models
- Popular car models in the used car market

### 9. **Pairplot: Exploring Relationships**
- Pairwise scatter plots for key numeric features
- Hue by fuel type for pattern identification
- Comprehensive view of feature interactions

---

## Technologies Used

### Core Libraries
- **Selenium**: Web scraping and browser automation
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization

### Tools
- **ChromeDriver**: Selenium browser driver
- **Jupyter Notebook**: Interactive development environment
- **Regular Expressions**: Text parsing and pattern matching
- **CSV**: Data storage format

### Environment
- **Python 3.x**: Primary programming language
- **Chromium Driver**: Headless browser for scraping

---

## How to Run

### Prerequisites
```bash
pip install selenium pandas matplotlib seaborn
```

For Google Colab:
```bash
!apt-get update
!apt install chromium-driver
```

### Execution Steps

1. **Initialization**
   - Run the initialization cells to set up Selenium WebDriver with headless Chrome options

2. **Web Scraping**
   - Execute the web scraping cells to extract data from Cars24
   - The scraper will automatically scroll and load all Hyundai listings
   - Data will be saved to `Cars24_DataSet.csv`

3. **Data Cleaning**
   - Run preprocessing cells to clean:
     - Car names (remove year prefix)
     - Kilometers driven (standardize units)
     - Prices (convert lakh notation to INR)
   - Refined data saved to `Refined_Cars24_DataSet.csv`

4. **Analysis and Visualization**
   - Execute EDA cells to view dataset statistics
   - Run visualization cells to generate all 9 plots

---

## Team Information

**Project**: Cars24 Used Car Data Analysis  
**Team**: Team C  
**Type**: Mini Project  
**Focus**: Web Scraping, Data Cleaning, Exploratory Data Analysis  

---

*This project is for educational purposes.*
