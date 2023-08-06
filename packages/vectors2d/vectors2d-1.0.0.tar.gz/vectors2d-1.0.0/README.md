# Vectors2D
It's a small module called to facilitate work with vectors in Python. Adds class Vector2D and operations with vectors in 2 dimensions.
All functions take Vector2D. They also take tuples or lists of int or float with len == 2.
Vectors can be added, subbed, multiplied by other vector or by int/float and more. You can find all the functions of the module below.

---
## Installing
Simply run `pip install vectors2d` from your command line.


## Class:
` Vector2D ` : takes ints, floats, tuple, list when creating. If not given, creates zero vector (0;0). If given only one number, assigns it to "x" coordinate. Also can take other Vector2D object.
### Class methods:
1. `iszero()` : check if vector is zero vector.
2. `isparallel(vector)` : check if the vector is parallel to the given vector. Takes Vector2D, list ot tuple.
3. `isperpendicular(vector)` : check if the vector is perpendicular to the given vector. Takes Vector2D, list ot tuple.
4. `iscodirected(vector)` : check if vector is co-directed to given vector. Takes Vector2D, list ot tuple.


## Global functions:
1. `absolute_vector(vector)` : calculates absolute value of given vector. Takes Vector2D object, list or tuple. Returns float;
2. `sum_vectors(*vectors)` : adds all the given vectors. Takes Vector2D objects, lists and tuples in any combination. Returns Vector2D;
3. `sub_vectors(*vectors)` : subtracts all the given vectors. Takes Vector2D objects, lists and tuples in any combination. Returns Vector2D;
4. `mult_vector(vector, multiplier)` : multiplies given vector by given number (can be int or float). "vector" takes Vector2D object, list and tuple as vector; "multiplier" takes int and float as multiplier. Returns Vector2D;
5. `scalar_mult_vectors(vectors*)` : calculates scalar multiplication of given vectors. Takes Vector2D objects, lists and tuples in any combination. Returns float;
6. `get_angle(vector1, vector2)` : returns angle between two given vectors in radians. Takes Vector2D objects, lists and tuples in any combination. Returns float;
7. `vector_from_dots(dot1, dot2)` : calculates vector from two given dots. Returns Vector2D.

## Examples:
1. **Creating vectors**
   ```
   >>> a = Vector2D(1)  # unit vector a(1;0)
   >>> b = Vector2D(3, 5)  # vector b(3;5)
   >>> c = Vector2D(list)  # vector from list or tuple (must have length 2)
   >>> d = Vector2D(a)  # creates vector with the same coordinates as vector a has.
   ```
2. **Getting vector's coorinates**
   1. As a list:
      ```
      >>> a()  # get list of vector's coordinates
      Output: [1, 0]  
      ```
      > You can use `vector.vector` for the same result
      
   2. Geting exact coordinate:
      ```
      >>> a[0]  # get "x" coorinate of vector a
      Output: 1

      >>> b[1]  # get "y" coordinate of vector b
      Output: 5
      ```
      > Values also can be changed this way
      
   3. Getting negative vector:
      ```
      >>> a = Vector2D(3, 2)
      >>> b = -a
      >>> b()
      Output: [-3, -2]
      ```
      
3. **Getting magnitude (absolute value) of vector**
   ```
   >>> abs(a)  # using native Python function
   Output: 1.0
   >>> abs(b)
   Output: 5.830951894845301
   ```
   > Inner function for absolute value is `absolute_vector(vector)`:
   ```
   >>> absolute_vector(a)  # using imported function of the module
   Output: 1.0
   >>> absolute_vector(b)
   Output: 5.830951894845301
   ```
4. **Operations with vectors**
   1. Addition
      ```
      >>> c = a + b  # using mathematical operator  # returns Vector2D
      >>> c()
      Output: [4, 5]
      ```
      > Inner function for addition is `sum_vectors(*vectors)`:
      ```
      >>> c = sum_vectors(a, b)  # using function of the module  # returns Vector2D
      >>> c()
      Output: [4, 5]
      ```
      > You can use `+=` with other vector to change vector directly:
      ```
      >>> a += b  # adding b to a and assigning result to a
      >>> a()
      Output: [4, 5]
      ```
      
   2. Subtraction
      ```
      >>> c = b - a  # using mathematical operator  # returns Vector2D
      >>> c()
      Output: [2, 5]
      ```
      > Inner function for substraction is `sub_vectors(*vectors)`:
      ```
      >>> c = sub_vectors(b, a)  # using function of the module  # returns Vector2D
      >>> c()
      Output: [2, 5]
      ```
      > You can use `-=` with other vector to change vector directly
      
   3. Multiplication
      1. By other vector:
      ```
      >>> a * b  # scalar multiplication of vectors using mathematical operator
      Output: 3.0  # returns float
      ```
      > Inner function for scalar multiplication is `scalar_mult_vectors(*vectors)`:
      ```
      >>> scalar_mult_vectors(a, b)  # using function of the module
      Output: 3.0
      ```
      **Note that while you using mathematical operators to multiply vectors you CAN'T use it more than once in a row, because you cant myltyply float by Vector2D:**
      ```
      >>> a * b * c
      Output:
         TypeError: unsupported operand type(s) for *: 'float' and 'Vector2D'
      ```
      > Code `a * (b * c)` will multiply vector a by cross product of vectors b and c. If you need to get cross product of more than two vectors at once, you should use       `scalar_mult_vectors(a, b, c)` instead.
      
      2. By number:
      ```
      >>> c = b * 2  # using mathematical operator  # returns Vector2D
      >>> c()
      Output: [6, 10]
      ```
      > Inner function for multiplication by number is `mult_vector(vector, modifier)`:
      ```
      >>> c = mult_vector(b, 3)  # returns Vector2D
      >>> c()
      Output: [9, 15]
      ```
      > You can use `*=` *only* with other vector to change vector directly
      
   4. Getting angle between vectors:
      ```
      >>> get_angle(a, b)  # returns angle between vectors in radians
      Output: 1.0303768265243125
      ```
      *Returns angle in radians*
      
5. **Boolean operations**
   1. Check if vector is zero vector:
      ```
      >>> a = Vector2D(0, 0)
      >>> a.iszero()
      Output: True
      
      >>> b = Vector2D(1, 2)
      >>> b.iszero()
      Output: False
      ```
      
   2. Check if vector is parallel with other vector:
      ```
      >>> a = Vector2D(1, 0)
      >>> b = Vector2D(-3, 0)
      >>> a.isparallel(b)  # takes Vector2D, list or tuple
      Output: True
      
      >>> c = Vector2D(3, 7)
      >>> c.isparallel(b)
      Output: False
      ```
   3. Check if vector is perpendicular with other vector:
      ```
      >>> a = Vector2D(3, 0)
      >>> b = Vector2D(0, 4)
      a.isperpendicular(b)
      Output: True
      
      >>> c = Vector2D(1, 5)
      >>> c.isperpendicular(b)
      Output: False
      ```
      

### TODO list:
- [x] Two-dimensional vector class
- [x] Vector operations 
  - [x] Sum
  - [x] Sub
  - [x] Mult by number
  - [x] Scalar multilpication with vector
  - [ ] Power by number
- [x] Vector calculations
  - [x] Absolute value - `absolute_vector()`
  - [x] Angle between vectors - `get_angle()`
  - [x] Vector from two dots - `vector_from_dots()`
  - [x] Is zero - `vector.iszero()`
  - [x] Is (not) parallel - `vector.isparallel()`
  - [x] Is perpendicular - `vector.isperpendicular()`
  - [x] Is co-directed - `vector.iscodirected()`
- [x] Assignment operations
  - [x] +=
  - [x] -=
  - [x] \*= (only for numbers)
  - [ ] \**=
  - [ ] /= (only for numbers)
- [x] Other
  - [x] Negative vector
