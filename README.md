

# Convert a C++ Interface to a [Turtle Mock](http://turtle.sourceforge.net/) class

The interface file should be like the following sample:

```cpp
class IShape
{
public:
    virtual double GetPerimeter() const = 0;
    virtual double GetArea() const = 0;
    virtual void SetName(const std::string& name) = 0;
    virtual int GetNumberOfVertices() const = 0;
    virtual ~IShape() = default;
}
```
