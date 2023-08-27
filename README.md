

# Convert a C++ Interface to a [Google Mock](https://github.com/google/googletest/tree/main/googlemock) or [Turtle Mock](http://turtle.sourceforge.net/) class

The interface format could be similar to the following sample. By running the script the path of the header file and the type of generated mock, google or turtle mock, should be given so the output will be written in a file named (Mock[interface name].h), and next to the given header file.

## Sample Input

```cpp
class IShape
{
public:
    virtual double GetPerimeter() const = 0;
    virtual double GetArea() const = 0;
    virtual void SetName(const std::string& name) = 0;
    virtual int GetNumberOfVertices() const = 0;
    virtual std::pair<double, double> GetVertexPosition(int vertexIx) const = 0;
    virtual ~IShape() = default;
}
```

## Generated Google Mock
```cpp
#include "IShape.h"

class MockShape: public IShape
{
    MOCK_METHOD(double, GetPerimeter, (), (const, virtual));
    MOCK_METHOD(double, GetArea, (), (const, virtual));
    MOCK_METHOD(void, SetName, (const std::string& name), (virtual));
    MOCK_METHOD(int, GetNumberOfVertices, (), (const, virtual));
    MOCK_METHOD((std::pair<double, double>), GetVertexPosition, (int vertexIx), (const, virtual));
};
```

## Generated Trutle Mock
```cpp
#include "IShape.h"

MOCK_BASE_CLASS(MockShape, IShape)
{
    MOCK_CONST_METHOD(GetPerimeter, 0, double());
    MOCK_CONST_METHOD(GetArea, 0, double());
    MOCK_NON_CONST_METHOD(SetName, 1, void(const std::string& name));
    MOCK_CONST_METHOD(GetNumberOfVertices, 0, int());
    MOCK_CONST_METHOD(GetVertexPosition, 1, std::pair<double, double>(int vertexIx));
};
```