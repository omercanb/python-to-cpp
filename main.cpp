#include "list.h"
#include "ptr.h"
#include "print.h"
using namespace py;
int main() {
    int x;
    ptr<list<int>> l;
    int step;
    ptr<list<double>> l2;
    ptr<range> r;
    x = 2;
    l = ptr(new list({2, 3, 4}));
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(len)(Name(l)))
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(x))
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(x), OpExpr)
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(x), OpExpr, IntExpr)
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(x), OpExpr, UnaryExpr)
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    step = x;
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(Name(x), OpExpr, Name(step))
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    step = -2;
    // ForStmt {
//   target: Name(i)
//   iter: Name(range)(OpExpr, OpExpr, Name(step))
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    // ForStmt {
//   target: Name(n)
//   iter: Name(l)
//   item_type: int
//   iterator_type: typing.Iterator[int]
// }
    // For loop not yet implemented
    l2 = ptr(new list({2.0, 3.0}));
    r = range(10);
    return 0;
}
