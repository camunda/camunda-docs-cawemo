---

title: 'Dashboard'
weight: 40

menu:
  main:
    identifier: "dashboard"
    parent: "user-guide"
    pre: "Consolidate all important information by grouping several reports together in a dashboard."
---

Often it is desired to get a quick overview of the business performance by monitoring the underlying processes. To achieve that, you can define reports in Camunda Optimize according to your KPIs (Key Performance Indicators) relavant to your business objectives. A dashboards shows multiple report so you can get an up-to-date view of the productivity of your system at one glance.

The dashboard itself consists of the [edit mode](#edit-mode) and the [view mode](#view-mode):

# Edit Mode

The edit mode allows you to configure the dashboard and adjust it to your needs. Therefore, you can perform all kinds of changing operations such as

* rename your dashboard
* add/remove a report
* save the current state with your applied changes
* cancel changes you already applied to the dashboard

{{< img src="dashboard-dashboardEditActions.png" title="Dashboard actions to perform in edit mode in Camunda Optimize" >}}

Once you have prepared all your reports, you can now start to assemble them into the dashboard. On the dashboard grid you will always find a `Add a report` button. Clicking on it, opens a modal, where you can select one of your defined reports and add it to the dashboard:

{{< img src="dashboard-editMode.png" title="Dashboard edit mode in Camunda Optimize" >}}
{{< img src="dashboard-addAReportModal.png" title="Dashboard add a report modal in Camunda Optimize" >}}

In the Add Report modal, you can click on the "Add External Source" link to enter the URL of an external datasource which should be added to the dashboard. This allows you to create dashboards that combine Optimize reports with data from other services. Such external reports are added as iframes to the dashboard.

You can drag the handle on the lower right corner of each report to resize it. To move the report to your desired place, you can simply drag it in any direction. As soon as you release the dragged report, it snaps to the closest grid position. Finally, you can delete the report from your dashboard by clicking on the `x` button on the upper right corner of each report.

{{< img src="dashboard-reportEditActions.png" title="Dashboard actions to perform in edit mode in Camunda Optimize" >}}


# View Mode

Once you have defined how your dashboard should look like, the view mode provides you with all the features to monitor you process, such as:

* fullscreen: display the dashboard in fullscreen and only see the essential information of your dashboard - the reports - and hide the header, control panel and footer. While in fullscreen mode, you can click on the Toggle Theme button to switch between the default light theme and a dark theme.

{{< img src="nightmode.png" title="Dark theme in Dashboard full screen view mode" >}}

* auto-refresh: this feature periodically updates the dashboard with the latest data. You can decide how often the update should be performed by setting a time span reaching from 1 to 60 minutes. An animation indicates when the next update is occuring. If you do not wish to use that feature anymore, you can disable it anytime. Note: when refreshing the dashboard page manually or switching to another page in between, the auto-refresh must be enabled again.

{{< img src="dashboard-viewMode-monitorFeatures.png" title="Dashboard view mode monitoring features in Camunda Optimize" >}}

In case you want to share the dashboard with other people or want to embed it in a webpage, you can use the sharing feature of the dashboard. Just click on the share button, which opens up a pop over. You can enable the sharing by pressing the switch. Now, you can send the link to people who do not have access to Camunda Optimize and thus enable them to see the dashboard. Also you can use the provided code in the embed section of the sharing pop over and paste it into your webpage. Everyone that views the webpage can then see content of the dashboard. The shared versions of the dashboard allow only to view the dashboard itself. There is no possibility to alter it or perform other actions that might abuse Optimize. You can revoke the sharing anytime by disabling the share switch.

{{< img src="dashboard-sharingPopover.png" title="Dashboard view mode monitoring features in Camunda Optimize" >}}

On top of that your are able to switch to the [edit mode](#the-edit-mode) by clicking on the edit button or delete the whole dashboard, if you do not have any use for it anymore. If you want to see some more details about the report on the dashboard, you can interact with the reports. The kind of interaction always depends on the report itself, but following shows some examplary actions:

{{< video src="dashboard-reportInteractions.mp4" title="Dashboard report interactions in Camunda Optimize" >}}

If the interactions do not suffice to get the desired information or you want to edit the report, you can directly go to it by clicking on the report title.


