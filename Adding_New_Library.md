> ### Libraries & Bureaus Overview
> - **Libraries** and **Bureaus** work the same way each entry represents one searchable website or catalog.  
> - A **Bureau search** is only used if a **Library search** fails to find results.  
> - Each record describes **where to search**, **how to extract results**, and **how to recognize result links**.
> - The only required fields are country, name and url_start however other feilds listed below will be required in most examples. 

---

> ### Fields & How to Find Them 
> | **Field** | 
> | Description | 
> | How to Get the Value |
> |-----------------------|
> | **country** |
> | The country where the library/bureau is based. |
> | Write the country name normally (e.g., `"France"`). |
> |-----------------------------------------------------|
> | **name** |
> | The name of the library or bureau. | 
> | Copy directly from the website’s homepage or title. |
> |-----------------------------------------------------|
> | **url_start** | 
> | The part of the search URL *before* your test search term. | 
> | Perform a sample search (e.g., for “history”), then copy everything in the address bar **before** the search word into `url_start`. |
> |-----------------------------------------------------|
> | **url_end** | 
> | The part of the search URL *after* your test search term. 
> | From the same test search, copy everything **after** your search word into `url_end`. Leave blank if not needed. |
> |-----------------------------------------------------|
> | **result_url_start** | 
> | Used only if the links in the HTML are *relative*. | 
> | Right-click result link **Inspect**. If the `<a href>` shows a partial link (e.g., `/record/123`), copy the missing beginning URL here (e.g.`https://examplelibrary.org`). |
> |-----------------------------------------------------|
> | **attribute** | 
> | A unique attribute of the `<a href>` tag if one exists. |
> | In Inspect, look for something like `<a href="..." ng-class="...">`. If this attribute appears **on all result links**, use it here (e.g., `{"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"}`). |
> |-----------------------------------------------------|
> | **tag** | 
> | The HTML tag that contains the result link. |
> | Often `<h3>` or `<a>`. Use if you need to specify which tags hold the search result titles. |
> |-----------------------------------------------------|
> | **tag_class** | 
> |The CSS class of that tag. 
> | Copy the value inside `class="..."` from Inspect (e.g., `item-title`). |
> |-----------------------------------------------------|

---

### Example Entry
```json
{
   "name": "National Library of France",
   "url_start": "https://data.bnf.fr/search?term=",
   "url_end": "",
   "country": "France"
}
```


```json
 {
   "name": "University of Texas Libraries",
   "url_start": "https://search.lib.utexas.edu/discovery/search?query=any,contains,",
   "url_end": "&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
   "attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
   "tag": "h3",
   "tag_class": "item-title",
   "result_url_start": "",
   "country": "United States"
 }
```


```json
{
  "name": "SS. Cyril and Methodius National Library",
  "url_start": "https://plus.cobiss.net/cobiss/bg/bg/bib/search?q=",
  "url_end": "",
  "attribute": {"class": "title value"},
  "tag": "div",
  "tag_class": "message",
  "result_url_start": "https://plus.cobiss.net/cobiss/bg/bg/",
  "country": "Bulgaria"
}
```


# Add National Library of France
```bash
curl -X POST http://localhost:8000/api/libraries \
  -H "Content-Type: application/json" \
  -d '{
    "name": "National Library of France",
    "url_start": "https://data.bnf.fr/search?term=",
    "url_end": "",
    "country": "France"
  }'
```

# Add Statistics Canada (Canada) as a bureau
```bash
curl -X POST http://localhost:8000/api/bureaus \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Statistics Canada",
    "url_start": "https://www.statcan.gc.ca/search/results/site-search?q=",
    "url_end": "&op=&fq=stclac:2",
    "attribute": {"ng-click":"openurl(url);"},
    "tag": "li",
    "tag_class": "mrgn-bttm-md",
    "result_url_start": "",
    "country": "Canada"
  }'
```