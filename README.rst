ngSe
====
Pronounced: en-gee-see

ngSe is a browser abstraction on top of the Selenium driver, designed specifically to ease testing of apps using heavy asynchronous javascript DOM manipulation (specifically, AngularJS).

There are a lot of things left to do:

- Package it so it works like an actual package
- Have the adaptor work on other-than-chromedriver (might be my first dive into meta-classes and/or class factories :D)
- Slice out the design-by-contract stuff into a separate library (and expand it)
- Figure out what is still fairly application specific, and remove/rework it.
- Come up with a clear definition of responsibility: when to return values and when to raise exceptions.
- Find bugs.
- Fix bugs.
- Expand, EXPAND!!!!!
