# Mission to Mars - Web Scrape
### UC Berkeley - jmerkel_Module_10

### Summary
This module scrapes high resolution martian hemisphere pictures from the webpage 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'. The scrape is specifically looking for each thumbnail and clicking the link to the main picture page. From there, the web application pulls the image link from the "wide-image" class and the title from the text of H2 tags. Once scraped, the image links and titles of the pictures are stored in the Mars MongoDB collection. From there, Flask is set up to show each hemisphere via different routes.


### Improvement
There are multiple options to improve the Flask webpage

##### Flask Main Page
- The addition of the hemisphere pictures are simply added as hyperlinks. This webpage can be improved by scraping the thumbnail pictures as well, and display a table at bottom of the page.
- Updating the font and style of the martian hemisphere table
- Adding specificity on which elements should be scraped/updated
- Updating the facts table

##### Updating hemisphere picture pages
- Updating the Flask route redirects to host the pictures directly on the page
- Adding navigation back to the main page

##### General
- Adding more thematic material such as background pictures, logos, different fonts
