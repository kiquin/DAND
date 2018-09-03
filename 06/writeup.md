# [Are delayed flights common?](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008v3/Story)

## Summary
My data visualization's goal is to provide more information on delayed flights, to understand them better. By using data from 2008 we can visualize how many flights are delayed during a year and how long those delays are. The data can usually be filtered by month, as to be able to see the effect of holidays and seasons; it's also possible to chose specific carriers. At the end, I show the causes of delay and a visualization of how common each one is.

## Design
I focused on utilizing the DepDelay field in the [data](http://stat-computing.org/dataexpo/2009/the-data.html). This field, however, had negative values, so I had to compute a new field that only had the positive values that correspond to the actually delayed flights.

I begin my story with a simple bar chart that counts the total number of delayed flights for each month of 2008. The bar chart is side-by-side to make the comparison clearer. After this introduction, I move over to a plot of the average delay for each month, which let's me see that it gets worse during the holidays. I decided to add the median line as the relationship between it and the average says a lot about the distribution of the data.

Those two visualizations were a nice introduction, so I decided to explore the delay time in a new perspective with a histogram. The distribution of the times is quite skewed so I reduced the x-axis. Furthermore, I added the months as pages so it could be related to the last plot. I checked the option to visualize the past months as faded bars.

Afterwards I returned to the first plot, but this time categorized by the carriers. This allows for a quick comparison between them, as well as to see the number of flights each of them operated that year. As with the last time, I decided to add the month filter for consistency. For easier reading, I had to search for the complete airline names and add them as aliases.

Finally, I decided to add a dashboard that went over the causes for delay. I thought that it would be nice to have the time related to each of those apart from just the count. This visualization was tricky to build, but I'm satisfied with the result. The month and carrier filter show up again, for consistency.

## Feedback
Feedback was very valuable for this project. I showed the [first version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008/Story) of the story to two people and collected their thoughts:

### Person #1 (Engineering student)
- The histograms axis are lacking titles so it's not easy to understand what it's supposed to be about
- The per-airline plot has two titles which confuse the reading.
- Cannot know which airline is which.

### Person #2 (Law student)
- The visualization is too large for their PC's screen and they have to scroll a lot.
- Histograms have no x-axis title, and the first one has marks while the second one doesn't.
- Needs the full airline name instead of the code.
- Each plot should have a legend to know what the colored parts refer to.
- Would be nice to see the delay distribution over time, with the other months faded in the background.
- More fun and interactive.

There were some common items in both, especially regarding the histograms. Due to this I decided to focus on fixing those: add titles and make them have the same marks. However during that time I realized that having two histograms on different scales was not very productive, so I got rid of the first one.

Another common point was the airline names. No normal person knows the codes to every airline so it was mandatory that I fixed it.

Person #2's feedback included many things I hadn't thought about, including the size of the story and legends (I thought it was self-explanatory when it wasn't). I incorporated the feedback and added filters to more plots, as well as legends. The result was a much more streamlined story, more interactive as well. Readers could now easily visualize changes over time.

I actually showed the visualization to a third person before uploading, which helped me identify some little mistakes involving tooltips before publishing it. The [second version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008v2/Story) was complete.

### Udacity review
After submitting the second version for review, I received more feedback. In the bar plots, bars were stacked on top of eachother, which was fine, but, it would be better if they were side-by-side. This way, it's easier to compare the values by comparing heights. This change was also applied to the carriers plot. 
A second point of feedback was that the chart would benefit from having a way to select multiple months at the same time. According to this, I replaced the month filters with multiple-value ones. Furthermore, I looked over the rest of the filters and replaced those I found lacking with better options. For example, in the final slide, I updated the carrier dropdown to a list to make better use of the space available.
Finally, some labelling was changed to a better languange; less academic. I also changed some colors to a more muted palette. All of the feedback was taken into account for the [third version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008v3/Story). 

### Links to every version
1. [First version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008/Story)
2. [Second version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008v2/Story)
3. [Current version](https://public.tableau.com/profile/enrique2711#!/vizhome/FlightDelays2008v3/Story)

## Resources

- [The IATA Airline and Airport Code search](https://www.iata.org/publications/Pages/code-search.aspx). Which helped me name all those airlines that I do not know of.
- [The 2008 flights data from stat-computing.org](http://stat-computing.org/dataexpo/2009/2008.csv.bz2)