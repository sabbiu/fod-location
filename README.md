# Fod-Location-Retriever

This file contains finding of location of restaurant near to you

Model Development
---

* find max rectangle that can cover the location
* sort them

During Checking
----

* check using binary search and find the possible hotels for that max_location developed
* for these filtered location, now check location in polygon

Complexity
---
From the algorithm used in code,
    
    O(log n + n/2)
    = O(n)
    
    ----
    for 60 locations,
        time = 0.403082 seconds
    
If the latitude and longitude were checked one by one with each and every hotels then,

     O(n * complexity_of_finding_point_in_polygon )
     where, time_complexity_of_finding_point_in_polygon ~ 0.15 (best_case)
 
     ----
     for 60 locations,
         time = 3.470986 seconds

So, finally =>
    
    8.611 * time(model_used) = time(best_case_if_second_scenario_was_considered)

Preview
----
If you open index.html, you can see the polygons which represent area covered by each hotels. And the pointer represents user location. When you hover over the user location, then a number will appear. It corresponds to the number as shown in command prompt in the next figure.
![test_01](https://user-images.githubusercontent.com/19733021/29241086-04dadb54-7f92-11e7-8d52-7df170539686.JPG)
Now, this is the output for locationchooser.py. You can see number assigned to each one of them. Hovering over the location in html file you can see if it matches or not. Some of the pointer lies in multiple hotels. In the command prompt you can see that, for such location, multiple hotels are returned.
![test_02](https://user-images.githubusercontent.com/19733021/29241096-500f7b20-7f92-11e7-9ea2-631d76ac8289.JPG)
