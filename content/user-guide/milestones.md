---
title: 'Milestones'
weight: 70

menu:
  main:
    identifier: 'milestones'
    parent: 'user-guide'
    Pre: ""
---

This view lists the saved milestones of a diagram.

## Creating Milestones

Within the milestone view, the latest version can be saved as a new milestone. Alternatively, a new milestone can be created via the [breadcrumb menu](../home#navigation) in the [diagram view](../diagrams).

When dragging and dropping a BPMN or DMN XML file into the diagram view, new milestones are created automatically.

## Diffing

Milestones of BPMN diagrams can be compared visually. By enabling the diffing feature, the currently selected milestone will be compared to its predecessor.

The differences that are highlighted are only those that affect the execution of the BPMN process. Pure visual changes like position changes are not highlighted.

## Related Diagrams

With the [Camunda Platform Engine](../../technical-guide/integrations/engine/) or the [Camunda Modeler](../../technical-guide/integrations/modeler/) integrations, various BPMN diagrams of the same process might exist within Cawemo. All diagrams that are detected as being the same process are shown as related diagrams and can be navigated to via the milestone view.

The currently selected milestone can also be compared visually against such a related diagram. When the diffing feature is enabled, first a milestone needs to be selected and then a related diagram.
