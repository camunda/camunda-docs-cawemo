---

title: 'Filter'
weight: 60

menu:
  main:
    identifier: "filter"
    parent: "user-guide"
    pre: "Narrow down your view on the process by creating reports or perform analysis based on a subset of all process instances, i.e., by variable value or start date"
---

Locating flaws in your process models can be a huge challenge when you have millions of process instances to sift through. Define filters in Optimize to narrow down your view to only a subset of process instances.

Camunda Optimize offers various ways of filtering your data, such as filter by:

* [Running/Completed process instances](#running-completed-instances-only-filter)
* [Start/End dates](#date-filters)
* [Process instance duration](#duration-filter)
* [Executed flow nodes](#flow-node-filter)
* [Variables](#variable-filter)
* [Combined filters](#combined-filters)

All the listed filters can be applied to [reports]({{< ref "/user-guide/report/_index.md" >}}) and during the [analysis]({{< ref "/user-guide/analysis/_index.md" >}}). Here you can see how to select one of the filters in a report:

{{< img src="report-with-filterlist-open.png" title="Report with open filter list in Camunda Optimize" >}}

# Running/Completed Instances Only Filter

By default, a report considers all process instances, regardless of whether they are still running or not. With the filters `Running Instances Only` and `Completed Instances Only`, you can decide only to consider only those process instances that are still running or those that already completed. Be aware that setting one of those filters (e.g. `Running Instances Only`) while the other one is already set (e.g. `Completed Instances Only`), will show a warning messsage since these two filters are incompatible with each other and will not show any data.

# Canceled Instances Only Filter

If the `Canceled Instances Only Filter` is applied, the report will consider only those instances, which were terminated before completion, either
internally or externally. Be aware that adding this filter along with the `Running Instances Only` will show a warning messsage since having such combination is incompatible and will not show any data.

# Date Filters

In Optimize, there are two kinds of date filters: the start date filter and the end date filter.
Applying the start date filter will result in report considering only process instances that started within the defined range of dates. The end date filter will work same way for the end dates of the processes.

{{< img src="date-filters.png" title="Date filters in the dropdown" >}}

A date filter can be defined in to different ways - filter by `Fixed Date` or `Relative Date`. The first version considers only process instances that were started or ended (depending on the kind of date filter you selected) within a fixed date range, e.g. filter all process instances between 2018-01-01 and 2018-01-26. That does not change even when days pass on. To simplify the process of picking such a date range, there are common shortcuts for the most used date ranges that can be used, for instance to get all process instances that were started/ended within the last seven days you can just click the "Past 7 days" button.

{{< img src="fixed-start-date-filter.png" title="Fixed start date filter in Camunda Optimize" >}}

With the `Relative Date` date filter you define a date range that does not remain static, but delivers a subset of the process instances in a rolling fashion, e.g. all process instances started/ended in the past seven days. For every day that passes, this range is automatically adjusted. To make it more clear, let's take an example: today is the March 28th. If you set a relatve date of the past three days, you get all process instances which were started/ended from 2018-03-26 to 2018-03-28. Now a day passes and we have March 29th. Applying the same filter now filters the process instances which were started/ended from 2018-03-27 to 2018-03-29.

{{< img src="relative-start-date-filter.png" title="Relative start date filter in Camunda Optimize" >}}


The start date filter and the end date filter are independent and can be applied to a report simultaneously. However, be aware that each of these filters can only exist once. For instance, you can set a `Fixed Date` start date filter. Defining now a `Relative Date` start date filter will replace the former start date filter. Defining a second `Relative Date` start date filter will also replace the first one. Applying any type of an end date filter at this point won't change the applied start date filters.

Also note, that reports with the end date filter applied, will consider only completed process instances.

# Duration Filter

The `Duration Filter` allows you to only regard process instances that took a certain time span for their whole execution. For instance, you can filter process instances that took more than three days or less than five seconds. Note: This filter shows only completed process instances, since the total duration of running process instances is not yet known.

{{< img src="duration-filter.png" title="Duration filter in Camunda Optimize" >}}

# Flow Node Filter

Retrieve only those process instances that executed certain flow nodes (e.g. a task) within your process by using the `Flow Node Filter`. Selecting several values at once, means that all of the selected flow nodes need to have been executed at least once in the process instance lifetime. At the top of the flow node filter modal you can see a preview of the filter you are beeing about to create. You can also filter process instances where certain flow nodes were not executed.

{{< img src="flownode-filter.png" title="Flow node filter in Camunda Optimize" >}}

# Variable Filter

Use the `Variable Filter` to retrieve only those process instances, where during the execution certain variables with specific values were used. For instance, assume you want to analyze only those process instances, which used the variable 'department' with the value 'marketing'. The variable filter can only filter for the final value of the variable. Let's take the example from before with the 'department' variable: on start of the process instance the variable has the value 'sales' and then is somewhere along the way reassigned to the value 'marketing' until the process instance finishes. In case you filter process instances for the variable 'department' with value 'sales', you won't get the process instance described in the previous sentence.

Start creating a variable filter by searching and selecting from the suggestions list of variable names, where the list contains only primitive types.

{{< img src="variable-filter.png" title="Searching through the variables in variable filter" >}}


There are now three type of variables that you can filter for:

* Boolean variables: They can have the state `true` or `false`. Therefore, you can choose if the boolean variable should have the value true or false in the process instance.

{{< img src="variable-filter-boolean.png" title="Boolean variable filter in Camunda Optimize" >}}

* String variables: The first 10 values are loaded and displayed. If the variable has more than 10 values a `Load More` button is shown to be able to extend the list as much as you need. You can also search through the whole list of values using the search input field. In case the `is` option of the toggle button is selected, checking one or more values means that you want to see only those process instances where the variable value equals one of the checked values (this corresponse to the `or` operator in the boolean logic). In case the `is not` option of the toggle button is selected, checking one or more values means that you want to see only those process instances where the variable value does not equal any of the checked values (this corresponse to the `and` operator in the boolean logic).

{{< img src="variable-filter-string.png" title="String variable filter in Camunda Optimize" >}}

* Numeric variables: Here you have an input field to define if a variable value in the process instance should be equal, not equal, less than or greater than a certain value. You can even add more input fields and apply the same operation serveral times at once. In case the `is` option of the toggle button is selected, adding one or more values means that you want to see only those process instances where the variable value equals one of the checked values (this corresponse to the `or` operator in the boolean logic). In case the `is not` option of the toggle button is selected, adding one or more values means that you want to see only those process instances where the variable value does not equal any of the checked values (this corresponse to the `and` operator in the boolean logic). In case the `is less than` or `is greater than` option is selected, only one value can be entered.

{{< img src="variable-filter-numeric.png" title="Numeric variable filter in Camunda Optimize" >}}

* Date variables: This filters all instances where the selected date variable has a value within a specified date range. You can click on one of the input fields to open a datepicker. Clicking on any day sets the start- or end date. After setting the start date, the next click sets the end date, allowing a convinient way to select a range when clicking on the start date field first. In addition to the datepicker, you can choose from multiple predetermined ranges using the buttons below the input fields.

{{< img src="variable-filter-date.png" title="Date variable filter in Camunda Optimize" >}}

{{< note title="Heads Up!" class="info" >}}
The variable filter can only filter for variables of a [primitive type](https://docs.camunda.org/manual/latest/user-guide/process-engine/variables/#supported-variable-values). If you want use complex types like object, you can use the [Variable Import Customization]({{< ref "/technical-guide/import/plugins.md#variable-import-customization" >}}) feature to transform your object variables into primitive type variables.

{{< /note >}}

# Combined Filters

All the previous mentioned filters can be combined together by adding one filter after another. Only those process instances where all of the configured filters are vaild are regarded in the report or analysis. The [duration filter](#duration-filter), [flow node filter](#flow-node-filter) and [variable filter](#variable-filter) can be defined several times. See the following screenshot for possible very long combination of filters:

{{< img src="combined-filter.png" title="Combined filter in Camunda Optimize" >}}
