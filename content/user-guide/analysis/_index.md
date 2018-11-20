---

title: 'Analysis'
weight: 70

menu:
  main:
    identifier: "analysis"
    parent: "user-guide"
    pre: "Find out which paths process instances that reached a desired outcome took"
---

If a process contains more than one end event, it is useful to know which path tokens take when they get to an end event. Camunda Optimize can show you a statistical analysis for a given end event and a gateway. This analysis includes how tokens were split at the gateway in question and how many of the tokens of each branch reached the end event.

{{< img src="analysis-1.png" title="Branch Analysis in Camunda Optimize" >}}

A branch analysis can only be performed on a specific version of a process definition. You can select any process definition using the "Select Process Definition" option in the top left of the page. After selecting a process definition and version, the diagram of the process is displayed on the page.

By default, all process instances for the selected process definition are included in the analysis. You can reduce this set of process instances by appying a filter. Read more about filters in the [Filter section]({{< ref "/user-guide/filter/_index.md" >}})

In order to perform a statistical analysis on the selected process, you need to specify a gateway and an end-event. Moving your mouse cursor over the End Event and Gateway inputs at the top of the screen highlights available elements in the diagram. Likewise you can mouse over an element to see whether it is an end event or gateway. Additionally, if you move your mouse over an end-event, you see detailled information about this end event, like how many instances reached this end event. Click on an element to select it. Click on any already selected element to deselect it. You can also clear the selection using the x button in the control panel on top. Changing the process definition also clears the selection.

After you selected both end event and gateway, a statistical analysis will be shown next to the diagram. The analysis consists of two bar charts as well as a statistical summary. Both charts contain a bar for every sequence flow leaving the selected gateway.

{{< img src="analysis-2.png" title="Statistical Analysis of Gateway and End Event" >}}

The first chart shows the distribution of process instances to the sequence flows, showing how often each sequence flow has been taken, independently of whether the process instance then reached the selected end event. A larger bar indicates more process instances have taken this sequence flow.

The second chart displays the relative amount of process instances that reached the selected end event after taking the respective outgoing sequence flow. A value of 100% indicates that every process instance that took a sequence flow reached the selected end-event. Accordingly, a value of 0% indicates that no process instance reached the selected end event after taking that sequence flow.

Process instances, which have taken more than one path, e.g. by looping back to a flow node before the gateway and then taking a different sequence flow, are not considered in the statistical analysis.
