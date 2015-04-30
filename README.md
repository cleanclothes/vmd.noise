Make some Noise
===============
This product is designed to make some noise. Selectable media include *Twitter*, *E-mail* and *Hardcopy*. *Facebook* has been switched off for now.

## Buildout
The noise.addon module has not yet been released on PyPI or wherever, but can be found on git@github.com:milieudefensie/vmd.noise.git should you have the proper authorization. Add this source to your buildout, build it and quickinstall the **Noise** module, as well as the **Relation Field** module.
## Manual
Add a Noise content item in Plone and add relevant data. Once that item has been created, there's several ways to get some statistics and data that may have been stored by users that have made some noise.
###Stats
Statistics can be viewed by adding **/stats** to the URL of you Noise item, for example if your noise item is called *makesomenoise*:

**https://www.milieudefensie.nl/makesomenoise/stats**

You need to be logged in as administrator in order to be able to have a look at this.
### Data
Data can be downloaded as CSV files. You can do this on a per medium base. Using the example above, data can be downloaded like this:

**https://www.milieudefensie.nl/makesomenoise/csv/twitter/download**
**https://www.milieudefensie.nl/makesomenoise/csv/facebook/download**
**https://www.milieudefensie.nl/makesomenoise/csv/email/download**
**https://www.milieudefensie.nl/makesomenoise/csv/hardcopy/download**

### JSForms
Noise uses jsforms for form validation. You can find the gory details over here: https://github.com/wyldebeast-wunderliebe/jsforms
 


