# Tree builder

[![Build Status](https://travis-ci.com/fdieulle/treebuilder.svg?branch=main)](https://travis-ci.com/github/fdieulle/treebuilder)

`treebuilder` is a python package which helps you to **build a tree data model** like XML or JSON configuration files.<br />
All **operations** of insert/update are **vectorized**.<br />
The **`xpath`** syntax is supported to **select sub set trees recursively** where your operations will apply.

## Prerequisites

* python 3.6 or higher

## Installation

```
pip install treebuilder
```

## Features

### Make a simple tree

In this example we want to build a simple tree which represents a breakfast menu.
The following code shows you the long way to proceed (non vectorized). 
In the next section we will see how to vectorize it.

```{python}
import treebuilder as tb

builder = tb.TreeBuilder()
builder.set('/breakfast_menu/food[name="Belgian Wafles"]/name', 'Belgian Wafles')
builder.set('/breakfast_menu/food[name="Belgian Wafles"]/price', '$5.95')
builder.set('/breakfast_menu/food[name="Belgian Wafles"]/calories', '650')

builder.set('/breakfast_menu/food[name="French Toast"]/name', 'French Toast')
builder.set('/breakfast_menu/food[name="French Toast"]/price', '$4.50')
builder.set('/breakfast_menu/food[name="French Toast"]/calories', '650')

builder.set('/breakfast_menu/food[name="Homestyle Breakfast"]/name', 'Homestyle Breakfast')
builder.set('/breakfast_menu/food[name="Homestyle Breakfast"]/price', '$6.95')
builder.set('/breakfast_menu/food[name="Homestyle Breakfast"]/calories', '950')

builder.to_xml('output.xml')
```

The output is stored here into a xml file named `output.xml`. And looks like:

```{xml}
<breakfast_menu>
  <food>
    <name>Belgian Wafles</name>
    <price>$5.95</price>
    <calories>650</calories>
  </food>
  <food>
    <name>French Toast</name>
    <price>$4.50</price>
    <calories>650</calories>
  </food>
  <food>
    <name>Homestyle Breakfast</name>
    <price>$6.95</price>
    <calories>950</calories>
  </food>
</breakfast_menu>
```
All the following examples assume that your output is an xml.

#### Reduce the code

We can produce the same result with the less code by using vectorization:

```{python}
builder = tb.TreeBuilder()

names = ['Belgian Wafles', 'French Toast', 'Homestyle Breakfast']
builder.expand('/breakfast_menu/food/name', names)
builder.nest('/breakfast_menu/food/price', ['$5.95', '$4.50', '$6.95'])
builder.nest('/breakfast_menu/food/calories', ['650', '650', '950'])
```

#### Insert a property

Imagine that we want to add a discount on our food about `5%` by default.

```{python}
builder.set('/breakfast_menu/food/discount', '5%')
```
Output:
```{xml}
<breakfast_menu>
  <food>
    <name>Belgian Wafles</name>
    <price>$5.95</price>
    <calories>650</calories>
    <discount>5%</discount>
  </food>
  <food>
    <name>French Toast</name>
    <price>$4.50</price>
    <calories>650</calories>
    <discount>5%</discount>
  </food>
  <food>
    <name>Homestyle Breakfast</name>
    <price>$6.95</price>
    <calories>950</calories>
    <discount>5%</discount>
  </food>
</breakfast_menu>
```

#### Update a sub set tree

To keep our clients healthy, we prefer providing a better discount for the food with less calories.
For example we want to apply a `7%` discount for all foods with 650 calories.

```{python}
builder.set('/breakfast_menu/food[calories=650]/discount', '7%')
```
Output:
```{xml}
<breakfast_menu>
  <food>
    <name>Belgian Wafles</name>
    <price>$5.95</price>
    <calories>650</calories>
    <discount>7%</discount>
  </food>
  <food>
    <name>French Toast</name>
    <price>$4.50</price>
    <calories>650</calories>
    <discount>7%</discount>
  </food>
  <food>
    <name>Homestyle Breakfast</name>
    <price>$6.95</price>
    <calories>950</calories>
    <discount>5%</discount>
  </food>
</breakfast_menu>
```

### Expand

The expand method allows you to extract a sub set of leaves in your tree then expands it with a list of values.

This method provided on the `TreeBuilder` class is based on a generalized function named `expand` which is also exposed in the package.
This function takes 3 parameters:

* `source`: The source list to expand. Each element is represented by a dictionary of key values pair.
* `entry`: The entry key where the values are stored (Inserted or Updated). 
* `values`: A list of values to set on the entry key.

In the `TreeBuilder` class the source list correspond to the selected leaves in the tree.

3 cases can happen during expansion:

* If the length of `values`is longer than the `source` list, the `source` list expands up to the `values` length. 
For each new element created in the `source`, we do a clone of an existing element by keeping the source's order and
by using a ring logic for overlaps.

* If the length of `values` and `source` list are the same, this is a perfect match and the values are set one by one to each element of the `source` list. No expansion happens here on both list, only on the entry of each element if it doesn't exist (insert), an update otherwise.

* If the length of `values` is smaller than the `source` list, the `values` are applied one by one to each source's element by using a ring logic on `values`.

A ring logic means that when the end of the list is reached the iterator goes back to the first element then continue.

#### Examples

The easiest example is at the begining when the tree is empty. So we create 1 leaf by value.
Here `len(values) > len(source)`

```{python}
builder = tb.TreeBuilder()
builder.expand('bookstore/book/title', ['Sapiens', 'Harry Potter'])
```
Output:
```{xml}
<bookstore>
  <book>
    <title>Sapiens</title>
  </book>
  <book>
    <title>Harry Potter</title>
  </book>
</bookstore>
```

Now we can give a price to each book:
Here `len(values) == len(source)`

```{python}
builder.expand('bookstore/book/price', ['$39.95', '$29.99'])
```
Output:
```{xml}
<bookstore>
  <book>
    <title>Sapiens</title>
    <price>$39.95</price>
  </book>
  <book>
    <title>Harry Potter</title>
    <price>$29.99</price>
  </book>
</bookstore>
```

We test the last case by setting a discount on all books.
Here `len(values) < len(source)`
```{python}
builder.expand('bookstore/book/discount', ['5%'])
```
Output:
```{xml}
<bookstore>
  <book>
    <title>Sapiens</title>
    <price>$39.95</price>
    <discount>5%</discount>
  </book>
  <book>
    <title>Harry Potter</title>
    <price>$29.99</price>
    <discount>5%</discount>
  </book>
</bookstore>
```

### Cross

The `cross` method allows you to select a tree sub set then expands if by crossing with a list of `values`.
The result of this operation gives you an expansion with a length of`S x V` where `S` is the number of your selected leaves in the tree and `V` the number of `values`.

This method provided on the `TreeBuilder` class is based on a generalized function named `cross` which is also exposed in the package.
This function takes 3 parameters:

* `source`: The source list to expand. Each element is represented by a dictionary of key values pair.
* `entry`: The entry key where the values are stored (Insert or update). 
* `values`: A list of values to set on the entry key.

In the `TreeBuilder` class the source list correspond to the selected leaves in the tree.

#### Examples

Imagine we have a bookstore and we want to duplicate our books with 2 different copies.
An identifier should be provided for each copy, let's say `1` and `2`.

```{python}
builder.cross('bookstore/book/copy_id', [1, 2])
```
Output:
```{xml}
<bookstore>
  <book>
    <title>Sapiens</title>
    ...
    <copy_id>1</copy_id>
  </book>
  <book>
    <title>Harry Potter</title>
    ...
    <copy_id>1</copy_id>
  </book>
  <book>
    <title>Sapiens</title>
    ...
    <copy_id>2</copy_id>
  </book>
  <book>
    <title>Harry Potter</title>
    ...
    <copy_id>2</copy_id>
  </book>
</bookstore>
```

### Nest 

The `nest` method is based on the `expand` method. It guaranties that your list of `values` won't be longer than the `source` list.
If the case happen the method truncates the input `values` list as `values[0:len(source)]`

### Set

The `set` method is based on the `expand` method but it takes a single value which is wrapped into a list then given to the `expand` method.
It is equivallent than calling `expand` with a `values` list of 1 element.

### XML attributes

The syntax is based on the `xpath` convention, so the character `@` is used to distinct an attribute from a leaf.
In the underlying Dict/List data structure, attributes are stored in a dictionary under the key `__ATTRIBUTES__` of the node which own them.
This key is defined as a constant in the package if you need to use it: `from treebuilder.constant inport ATTRIBUTES`.

#### How to set an attribute

```{python}
builder.set('bookstore/book/@lang', 'en')
```
Output:
```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    ...
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    ...
  </book>
</bookstore>
```

## Examples

### Build a book store tree

We create a book store with 2 books and 2 copies of each.
We also setup the lang as an attribute and a price for each of them.
It takes only 4 lines of code to acheive as follow:

```{python}
import treebuilder as tb

builder = tb.TreeBuilder()

# Create 2 books in a bookstore
builder.expand('/bookstore/book/title', ['Sapiens', 'Harry Potter'])

# Set the lang to all books as attribute
builder.set('/bookstore/book/@lang', 'en')

# Set the price for each book
builder.nest('/bookstore/book/price', [39.95, 29.99])

# Duplicate each book to make 2 copies
builder.cross('/bookstore/book/copy_number', [1, 2]) 

builder.to_xml('bookstore.xml')
```
Output:

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

### Set values with filter

We want now add the author for each book. Each book has its own author so we need to select a sub tree to apply the author.

```{python}
builder.set('/bookstore/book[title=\'Harry Potter\']/author', 'J K. Rowling')
builder.set('/bookstore/book[title=Sapiens]/author', 'Y N. Harari')
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

### Set values in distinct sub trees

We want add a details section for a book where we will store addtional informations like the publish year.

```{python}
builder.set('/bookstore/book[title=\'Harry Potter\']/details/published_year', '2005')
builder.set('/bookstore/book[title=Sapiens]/details/published_year', '2014')
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
builder.expand('/bookstore/book[title="Harry Potter"]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(3)])
builder.expand('/bookstore/book[title=Sapiens]/borrowers/borrower/name', [f'Client_{i+1}' for i in range(5)])
```
Output
```{xml}
<bookstore>
  <book lang="en">
    <title>Sapiens</title>
    <copy_number>1</copy_number>
    ...
    <borrowers>
      <borrower><name>Client_1</name></borrower>
      <borrower><name>Client_3</name></borrower>
      <borrower><name>Client_5</name></borrower>
    </borrowers>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <copy_number>1</copy_number>
    ...
    <borrowers>
      <borrower><name>Client_1</name></borrower>
      <borrower><name>Client_3</name></borrower>
    </borrowers>
  </book>
  <book lang="en">
    <title>Sapiens</title>
    <copy_number>2</copy_number>
    ...
    <borrowers>
      <borrower><name>Client_2</name></borrower>
      <borrower><name>Client_4</name></borrower>
    </borrowers>
  </book>
  <book lang="en">
    <title>Harry Potter</title>
    <copy_number>2</copy_number>
    ...
    <borrowers>
      <borrower><name>Client_2</name></borrower>
    </borrowers>
  </book>
</bookstore>
```
 

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