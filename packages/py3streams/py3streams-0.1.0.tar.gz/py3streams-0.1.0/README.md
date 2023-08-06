# py3streams - manipulate collections

Package contains classes to support operations on collection like set, list, dict or range using chain of generators.

## Table of contents
* [Description](#Description)
* [Installation](#Installation)
* [Usage](#Usage)

## Description
Classes from the package are: *Stream*, *IntStream* and *DictStream*. Classes are not collections but they are iterable. Only few methods executed stored lazy generators and evaluate result. Streams cannot be reused, chain of filters, maps and/or fmaps can be evaluated once.
Filters, maps and fmaps do not invoke stream. After stream is invoked, stream cannot be reused. Methods which invoke stream are: to_list, to_dict, count, sum, max, min, any_match, all_match.

```
example_list = ["1", "5", "2", "10", "11"]
sum = Stream(example_list).map_to_int().filter(lambda x: x < 10).sum()
# result: [1, 5, 2] -> 8
```

In the example class *Stream* has been used on the *example_list*. First there is registered generator for changing strings to ints, then registered generator with lambda expression for elements lower than *10* and sum them.

Classes *Stream*, *IntStream* and *DictStream* hold provided collection as an *iterable object* and generators which are related with *filter(s)* and *map(s)* methods for future **lazy** evaluation.

#### Iteration example
Streams can be used with python *for-loop*. 
```
for element in IntStream(1, 9).filter(lambda x: x % 2 == 0):
    print(element)
# result: 2, 4, 6 and 8
```

## Installaton
To use the streams install the package.
```
pip install py3stream
```

## Usage
Streams help manipulate collections. For most actions its enough to use filter(), map() and fmap() methods.
Classes contain build-in functions which include lambdas and allow use short-name methods for similar result.

#### Example 1

Lets define a list
```
elements = [0, 1, "2", 3, None, [5, 6, "7"], ["8"]]
```
Stream will find elements lower than 3. Sub-lists and None values should be ignored.
Class stream can be created like:
```
stream = Stream(elements).filter(lambda x: x is not None).filter(lambda x: not isinstance(x, list)).map(lambda x: int(x)).filter(lambda x: x < 3) # still we have a stream 
for e in stream:
    print(e)
# result 0, 1 and 2
```
and alternative with Stream's functions:
```
stream = Stream(elements).no_list().no_none().map_to_int().lt(3)
for e in stream:
    print(e)
# result 0, 1 and 2
```

#### Example 2

Lets define a list
```
elements = ["a", "b", 3, 4]
```
Stream will find first int
```
value = Stream(elements).filter(lambda x: isinstance(x, int)).get_first()
# result 3
```
**get_first(default_value=None)** returns None if Stream does not find element by default.
```
value = Stream(elements).filter(lambda x: isinstance(x, list)).get_first(5)
# result is 5
```






