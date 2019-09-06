---
title: 'Milestones'
weight: 40

menu:
  main:
    identifier: 'milestones'
    parent: 'user-guide'
    Pre: ""
---

This view lists the saved milestones of a diagram.

## Creating Milestones

In the [diagram view](../diagrams), a new milestone can be created via the [breadcrumb menu](../home#navigation).

When dropping a BPMN XML file into the diagram view, new milestones are created automatically.

## Diffing (Enterprise only)

With the enterprise license, milestones can be compared visually. By enabling the Diffing, the currently selected milestone will be compared to its predecessor.

The differences that are highlighted are only those that affect the execution of the BPMN process. Pure visual changes like position changes are not highlighted.

## Related Diagrams (Enterprise only)

With the enterprise license and the [Camunda BPM Engine](../../technical-guide/integrations/engine/) or the [Camunda Modeler](../../technical-guide/integrations/modeler/) integration, various diagrams of the same process might exist within Cawemo. All diagrams that are detected as being the same process are shown as related diagrams and can be navigated to via the milestone view.

The currently selected milestone can also be compared visually against such a related diagram. When Diffing is enabled, first a milestone needs to be selected and then a related diagram.
