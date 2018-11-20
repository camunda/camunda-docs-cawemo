---
title: "Report"
weight: 50

menu:
  main:
    identifier: "report"
    parent: "user-guide"
    pre: "Explore, discover and get insights into your that otherwise would be hidden by creating a report."
---

Reports provide you with the ability to view your data from different angles and thus capture all aspects that influence your process, show new trends or depict your current business state.

Each report consists of the [edit mode](#edit-mode) and the [view mode](#view-mode) to perform different kinds of actions on it.

# Edit Mode

The edit mode allows you to configure the report and adjust it to your needs. Therefore, you can perform all kinds of changing operations such as

- rename your report
- build a report
- save the current state with your applied changes
- cancel changes you already applied to the report

{{< img src="report-reportEditActions.png" title="Report actions to perform in edit mode in Camunda Optimize" >}}

Building a report is the crux of the report edit mode. The building process itself is composed of several steps, which happen in the control panel.

## Select a Process Definition

Every report relates to a specific process definition and version. You always need to choose a process definition you want to create a report for. If you open the process definition popover, you see two select items displayed. On the left one you can choose the process defintion name and on the right item the version. Independent from all other configuration options you can always adjust the process defintion.

{{< img src="report-processDefinitionSelection.png" title="Process definition selection in the report builder in Camunda Optimize" >}}

There is one particular option in the version selection, which is called `all`. This option is available for every definition and indicates that you create a report which uses data across all versions of the report. The latest version of the definition is the reference point, which means that data from older version is mapped to the most recent version. Therfore, the report data can seem to be inconsistent, which is due to changes that occured within the diagram throught the different versions, e.g. old version do not contain newly added tasks or a part of the diagram was removed because it was considered to be obsolete.

By default, all process instances for the selected process definition are included in a report. You can reduce this set of process instances by appying a filter. Read more about filters in the [Filter section]({{< ref "/user-guide/filter/_index.md" >}})

## Define the Report

In this section of the report builder you are characterizing the output of the report. Basically, you writing the following "I want to view ... grouped by ... visualized as ...". To understand better what view and group by mean, you can use the analogy of a graph, where view is the y-axis and group by is the x-axis. First you need to select, which part of the data you want to view. Optimize enables you to perform the view part in five different ways:

1. Raw Data: View just a table with the actual data listed as rows. This can come in handy if you found interesting insights in certains process instances and need detailed information about those instances or you are exploring a process definition with a limited number of instances. The maximum number of rows shown in the table is limited to 1000.
2. Count Process Instance Frequency: View how many process instances were started.
3. Count Flow Node Frequency: View how often the flow nodes (e.g. tasks, gateways, etc.) have been executed.
4. Process Instance Duration: View how long the process instances took until they finished. You can view the minimum, average, median and maximum duration with the median being an estimate and the other operations being exact values.
5. Flow Node Duration: View how long each flow node (e.g. task, gateway, etc.) took for executions. You can view the minimum, average, median and maximum duration with the median being an estimate and the other operations being exact values.

Subsequently, you need to define how to group the data. Think of it as applying a metric to your input, where you break out your data by date, flow nodes or variable values. Essentially, you have four different options:

1. None: Don't split up the data by any means and just use the total number.
2. Flow Nodes: Cluster the data by flow nodes.
3. Start Date of the Process Instance: Group process instances together that were started during the same date period or time, e.g. hour, day or month.
4. Variable: Process instances with the same value for the selected variable are grouped together.

Finally, you just need to define how you want the data to be visualized. Examples are heatmap, table, bar or line chart.

Throughout the definition of the report it might be hard to find out which combinations are valid. For this reason you get assisted during the building process such that only those configuration options are enabled that might lead to a result. For instance, if you choose `Count Flow Node Frequency` as view, the data is automatically grouped by Flow Nodes as no other combination would be valid. All possible combinations can also be found in the following table:

<table class="table table-striped">
  <tr>
    <td><b>View</b></td>
    <td><b>Group By</b></td>
    <td><b>Visualize as</b></td>
  </tr>
  <tr>
    <td>Raw Data</td><td>None</td><td>Table</td>
  </tr>
  <tr>
    <td>Count Process Instance Frequency</td><td>None</td><td>Number</td>
  </tr>
  <tr>
    <td>Count Process Instance Frequency</td><td>Start Date of Process Instance</td><td>Table, Bar, Line, Pie</td>
  </tr>
  <tr>
    <td>Count Process Instance Frequency</td><td>Variable</td><td>Table, Bar, Line, Pie</td>
  </tr>
  <tr>
    <td>Count Flow Node Frequency</td><td>Flow Nodes</td><td>Table, Bar, Line, Pie, Heatmap</td>
  </tr>
  <tr>
    <td>Process Instance Duration</td><td>None</td><td>Number</td>
  </tr>
  <tr>
    <td>Process Instance Duration</td><td>Start Date of Process Instance</td><td>Table, Bar, Line, Pie</td>
  </tr>
  <tr>
    <td>Process Instance Duration</td><td>Variable</td><td>Table, Bar, Line, Pie</td>
  </tr>
  <tr>
    <td>Flow Node Duration</td><td>Flow Nodes</td><td>Table, Bar, Line, Pie, Heatmap</td>
  </tr>
</table>

### Raw Data Table Configuration

{{< img src="tableInteractions.gif" title="Reordering and Hiding Columns in Raw Data Tables" >}}

When working with raw data table reports, you can hide specific columns using the menu on the right side next to the table. You can also re-order the table columns using drag-and-drop on the header of the respective column.

Changes to a columns visibility or order are persisted and also apply to the report view mode and any dashboard this report is displayed on.

## Target Value Comparison

Based on flow node duration heatmaps, Optimize allows you to specify a target value for every activity. For example, if a user task has to be completed within one day, you can set the target value to one day. If the time it takes to complete the user task exceeds this target value, the task is highlighted in the heatmap.

To set target values and create a target value comparison heatmap, you need to be in the edit mode of a report which has the following configuration:

<table class="table table-striped">
  <tr>
    <td>View</td><td>Flow Node Duration</td>
  </tr>
  <tr>
    <td>Group by</td><td>Flow Nodes</td>
  </tr>
  <tr>
    <td>Visualize as</td><td>Heatmap</td>
  </tr>
</table>

If your report has this configuration, the target value button is enabled. Clicking on the Target Value button for the first time opens an overlay containing the process diagram and a table with all flow nodes. You can also see the actual duration value for every flow node. If you want to set a target value for a flow node, use the number and unit fields in the last column. If the target value number field for a flow node is empty, this flow node has no target value set (the selected time unit is ignored in that case).

{{< img src="targetvalue-2.png" title="Setting Target Values" >}}

If you set a target value for a flow node, this target value is represented as a badge on the flow node in the diagram in the upper part of the overlay. You can click on any flow node in the diagram to jump to the target value input field in the table. When selecting a target value input field in the table, the corresponding diagram element is highlighted. To save the target value configuration, click the Apply button.

If you saved the target values, the normal duration heatmap is replaced with a target value visualization. In this new visualization, flow nodes with an average duration larger than the specified target value are highlighted in red. If you mouse over one of the nodes the tooltip shows the target duration value, the actual duration and the relative percentage the actual value is of the target value. You can also see the target value as a badge on the diagram.

{{< img src="targetvalue-1.png" title="Target Value Comparison" >}}

After the initial target values for a report are set, you can use the Target Value button to toggle between the Target Value and the regular Duration view mode. If you want to change target values, you can use the gear button to open the overlay again.

As with any change to a report configuration, in order to persist target values and show them in the Report view mode and on Dashboards, you need to save the report using the Save button in the upper right corner.

### Progress Bar Visualization

{{< img src="progress.png" title="Progress Bar Visualization on a Dashboard" >}}

To create a progress bar visualization, create any report that is visualized as single number (e.g. Count Process Instances grouped by None or Average Process Instance Duration Grouped by None). Then, click on the target value button to set the baseline and the target value for this report. After confirming the modal, the report is visualized as progress bar.

You can switch between the progress bar and single number visualization by clicking the Target Value button again. Using the gear button, you can adjust the target and baseline values.

### Chart Goal Line

Optimize allows you to set a goal line in bar chart and line chart visualizations. Using this feature, it is possible to highlight anything above or below a certain value.

A good use case for such functionality is the following example:

Let us say that the number of completed process instances every month should always be above 10. A goal line can be used to visualize that:

First, go to the edit mode of a report and choose the following configuration:

<table class="table table-striped">
  <tr>
    <td>View</td><td>Count Frequency of Process Instance</td>
  </tr>
  <tr>
    <td>Group by</td><td>Start Date of Process Instance: Month</td>
  </tr>
  <tr>
    <td>Visualize as</td><td>Barchart</td>
  </tr>
</table>

Now click on the target value button in the control panel to see the following:
{{< img src="bargoal1.png" title="Target Value modal" >}}

Set the target value input field to 10 and select the above button. Now if the number of process instances is below 10 in any month, that month will be highlighted in red as shown.
{{< img src="bargoal2.png" title="Bar Chart Report with a Goal line" >}}

This feature can be also used with every other bar chart and line chart visualization.
Here is another example where the target value is used with line chart visualization:
{{< img src="lineGoal.png" title="Line Chart Report with a Goal line" >}}

### Process Instance Parts

In some cases you are not interested in the duration of the whole process instance, but only a certain part of it. For that scenario, there is an additional button called "Process Instance Part" available for every Process Instance Duration view. Clicking this button opens an overlay letting you select the start and end of the part of the process instance you are interested in. After confirming the selection, the displayed duration refers to the selected part only instead of the whole instance.

In some cases it can happen that the same activity is executed multiple times in the same process instance, e.g. if the process contains loops or parallel gateways. In such cases, Optimize considers only the part between the start date of the first instance of the start node and the end date of the first instance of the end node.

{{< img src="process-part.png" title="Process Instance Part Modal" >}}

# View Mode

Once you have defined how your report should look like, the view mode provides you with different kinds of actions, such as switch to the [edit mode](#the-edit-mode) by clicking on the edit button or delete the whole report, if you do not have any use for it anymore. If you want to see more details about the report, you can interact with it. The kind of interaction always depends on the report itself, but the following shows some examplary actions:

{{< video src="report-reportInteractions.mp4" title="Report interactions in Camunda Optimize" >}}

In case you want to share the report with other people or want to embed it in a webpage, you can use the sharing feature of the report. Just click on the share button, which opens up a pop over. You can enable the sharing by pressing the switch. Now, you can send the link to people who do not have access to Camunda Optimize and thus enable them to see the report. Also you can use the provided code in the embed section of the sharing popover and paste it into your webpage. Everyone that views the webpage can then see content of the report. The shared versions of the report allow to view the report itself only. There is no possibility to alter it or perform other actions that might abuse Optimize. You can revoke the sharing anytime by disabling the share switch.

{{< img src="report-sharingPopover.png" title="Report sharing pop over in Camunda Optimize" >}}
