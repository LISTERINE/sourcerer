from sourcerer import Name, Call, Document

d = Document()

calls = [Name("MyClass"),
         Call(name=Name("call1")),
         Call(name=Name("call2"))]
c = Call(caller_list=calls, name=Name("main"))

d.add_child(c)
d.output()