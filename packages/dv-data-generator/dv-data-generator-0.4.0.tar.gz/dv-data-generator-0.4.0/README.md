# DV360 data Generator

To be able to retrieve different data reports from DV360 we use different API's. These API's are the DBM API and DV360 REST API. To make the code more maintanable we have turned the applied "builder" pattern into a package. This package can be used to retreive different types of reports or be extended to support reports, for different purposes.


## Example

To use the package and get our data from the platform, we must have a valid user oauth file. This can be created using the dqna authflow script.

We need to init the director:

```py
director = DvDataDirector(credentials="../some-cerdentials-file.json")
```

After this we can get different reports, see the methods of `director`



