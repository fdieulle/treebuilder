# Tree builder

[![Build Status](https://travis-ci.com/fdieulle/treebuilder.svg?branch=main)](https://travis-ci.com/github/fdieulle/treebuilder)

It's a python package which helps you to build a tree data model to generate configuration files like XML or JSON for example.
It provides a xpath syntax like to apply values recursively on your building tree.

## Prerequisites

* python 3.6 or higher

## Installation

```
pip install treebuilder
```

## Examples

### Build a book store tree

We create a book store with 2 books and 2 copies of each.
We also setup the lang as an attribute and a price for each of them.

```{python}
import treebuilder as tb

builder = tb.TreeBuilder()
# Create 2 books in a bookstore
builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter'])
# Set the lang to all books
builder.set('bookstore/book/@lang', 'en')
# Set the price to each book
builder.nest('bookstore/book/price', [39.95, 29.99])
# Duplicate each book to make 2 copies
builder.cross('bookstore/book/copy_number', [1, 2]) 

builder.to_xml('bookstore.xml')
```

The output stored into `bookstore.xml` file looks like:

```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>1</copy_number>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>1</copy_number>
  </book>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>2</copy_number>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>2</copy_number>
  </book>
</bookstore>
```
The next parts of this example suppose that you call `builder.to_xml('bookstore.xml')` to generate the output after each modification.

### Set values with filter

We want now add the author for each book. Each book has its own author so we need to select a sub tree to apply the author.

```{python}
builder.set('bookstore/book[title=\'Harry Potter\']/author', 'J K. Rowling')
builder.set('bookstore/book[title=Sapiens]/author', 'Y N. Harari')
```
Output
```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>1</copy_number>
    <author>Y N. Harari</author>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>1</copy_number>
    <author>J K. Rowling</author>
  </book>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>2</copy_number>
    <author>Y N. Harari</author>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>2</copy_number>
    <author>J K. Rowling</author>
  </book>
</bookstore>
```

# Set values in distinct sub trees

We want add a details section for a book where we will store addtional informations like the publish year.

```{python}
builder.set('bookstore/book[title=\'Harry Potter\']/details/published_year', '2005')
builder.set('bookstore/book[title=Sapiens]/details/published_year', '2014')
```
Output
```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>1</copy_number>
    <author>Y N. Harari</author>
    <details>
      <published_year>2014</published_year>
    </details>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>1</copy_number>
    <author>J K. Rowling</author>
    <details>
      <published_year>2005</published_year>
    </details>
  </book>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>2</copy_number>
    <author>Y N. Harari</author>
    <details>
      <published_year>2014</published_year>
    </details>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>2</copy_number>
    <author>J K. Rowling</author>
    <details>
      <published_year>2005</published_year>
    </details>
  </book>
</bookstore>
```

### Expand values for distinct sub tree

Now we want to set the list of calient which has borrowed books
Let's that there is 5 people which borrow Spaiens and 3 Harry Potter

```{python}
builder.expand('bookstore/book[title="Harry Potter"]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(3)])
builder.expand('bookstore/book[title=Sapiens]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(5)])
```
Output
```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>1</copy_number>
    <author>Y N. Harari</author>
    <details>
      <published_year>2014</published_year>
    </details>
    <borrowers>
	  <borrower><name>Client_1</name></borrower>
	  <borrower><name>Client_3</name></borrower>
	  <borrower><name>Client_5</name></borrower>
	</borrowers>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>1</copy_number>
    <author>J K. Rowling</author>
    <details>
      <published_year>2005</published_year>
    </details>
    <borrowers>
	  <borrower><name>Client_1</name></borrower>
	  <borrower><name>Client_3</name></borrower>
	</borrowers>
  </book>
  <book lang="en">
    <title>Sapiens</title>
    <price>39.95</price>
    <copy_number>2</copy_number>
    <author>Y N. Harari</author>
    <details>
      <published_year>2014</published_year>
    </details>
    <borrowers>
	  <borrower><name>Client_2</name></borrower>
	  <borrower><name>Client_4</name></borrower>
	</borrowers>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <price>29.99</price>
    <copy_number>2</copy_number>
    <author>J K. Rowling</author>
    <details>
      <published_year>2005</published_year>
    </details>
    <borrowers>
	  <borrower><name>Client_2</name></borrower>
	</borrowers>
  </book>
</bookstore>
```
 ...

## Contributing

Issue tracker: [https://github.com/fdieulle/treebuilder/issues](https://github.com/fdieulle/treebuilder/issues)

If you want to checkout the project and propose your own contribution, you will need to setup the project with the following steps:

### Create a virtual environment:

```
python -m venv venv
```

### Activate your virtual environment:

```
venv/Scripts/activate
```

### Install package dependencies

```
pip install -r requirements.txt
```

## License

This project is open source under the [MIT license](https://github.com/fdieulle/treebuilder/blob/main/LICENSE).