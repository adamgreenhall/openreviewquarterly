/builder was the bridge between ORQ v1.0 and the modern Rails version. 

In ORQ v.10 issues used to get built out from Google Docs to a set of .html files using Python. This all got held together by a [Middleman](http://middlemanapp.com/) app, which is basically Rails without a database.

The code currently in /builder used Python to convert those files into series of Rails database **.new()** calls to be run through the console to build out the initial database. 