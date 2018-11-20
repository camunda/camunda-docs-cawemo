---
title: "Combined Report"
weight: 60

menu:
  main:
    identifier: "combined-report"
    parent: "report"
    pre: "Compare and get insights by combining multiple reports in one view."
---

Sometimes, it is necessary to compare multiple reports or visualize them together in one diagram. To achieve that, it is possible to create a special type of report called 'combined report'. To create a new combined report, please click on 'create combined report' button available in the report list page.

{{< img src="combined-report-create.png" title="Creating a combined report" >}}

Then, you are redirected to the combined report builder. There you can see on the right a selection panel to select multiple reports to combine. The selected reports will show up combined in the report preview panel on the left.

{{< img src="combined-report.png" title="Combined report builder" >}}

For example, combining two reports with a table visualization results in the following view:

{{< img src="table-report.png" title="Combining two reports with a table visualization" >}}

And combining two reports with line chart visualization results in the following view:

{{< img src="area-chart-report.png" title="Combining two reports with line chart visualization" >}}

It is also possible to drag items in list of selected reports to top or bottom to change their order in the report view.

Please note that not all reports can be combined with each other since there are a couple of differences between them. Therefore, when selecting a report, only the other reports that are combinable with the selected one will appear.

Only reports that match the following criteria can be combined:

- Same group by
- Same visualization
- Same view but combining avg, min, max, median (operations) is possible
- Process definition can be different

Moreover, only the following visualizations are possible to combine and will show up in the combined selection list:

- Bar Chart
- Line Chart
- Table
- Number

It is also possible to update the name of the report, save it and add it to a dashboard exactly like the normal report. The combined reports will also show up in the report list along with the normal reports.
