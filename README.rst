ngSe
====
Pronounced: en-gee-see

ngSe is a browser abstraction on top of the Selenium driver, designed specifically to ease testing of apps using heavy
asynchronous javascript DOM manipulation (specifically, AngularJS).

The idea here is centered around defining things as a "how to find" rather than concrete objects, and using smart
retry-loops to properly wait for things to happen. This can be expanded much more than it currently is (I'm thinking
lazy evaluation of an 'Element' abstract type), but for now this is helpful.

There are a lot of things left to do within its current scope:

- Better documentation and introduction material
- Have the adaptor work on other-than-chromedriver (might be my first dive into meta-classes and/or class factories :D)
- Support Python 3
- Slice out the design-by-contract stuff into a separate library (and expand it)
- Figure out what is still fairly application specific, and remove/rework it.
- Come up with a clear definition of responsibility: when to return values and when to raise exceptions.
- Find bugs.
- Fix bugs.
- Expand, EXPAND!!!!!

And there are ideas on expanding the scope!

- Create an 'Element' type which holds the search definition, rather than test-level search paths (normalization yo)
- More help around finding elements in more specific applications (currently just targeting AngularJS setups)
