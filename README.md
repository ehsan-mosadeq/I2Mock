

# Turtle-Mock-Create

This script make c++ turtle mock from class interface.
 
Input interface file should be as the following form:

class IShape

{

public:

    virtual double GetPerimeter() const = 0;
  
    virtual double GetArea() const = 0;
  
    virtual void SetName(const std::string& name) = 0;
  
    virtual int GetNumberOfVertices() const = 0;
  
}
