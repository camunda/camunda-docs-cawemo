---
title: 'Diagrams'
weight: 50

menu:
  main:
    identifier: 'diagrams'
    parent: 'user-guide'
    Pre: ""
---

This view is used to see and edit a diagram, provided that the user has the required access right. Through the milestone history icon in the diagram actions or the drop down menu in the [breadcrumb navigation](../home#navigation), the [milestones](../milestones) for this diagram can be seen.

## BPMN

Business Process Model and Notation (BPMN) is a standard for Workflow and Process Automation. Further details can be read in our [learning section](https://camunda.com/bpmn).

### Specification

When selecting an element of the BPMN diagram, a description or specification text can be attached to the element. This text is stored within the documentation property of the BPMN standard. This way, the text will be part of the BPMN XML file when the diagram is exported, and can be seen in other tools like the [Camunda Modeler](https://camunda.com/products/modeler).

### Call Activity

When you add a new link to a Call Activity, the process ID of the child process is written to the `calledElement` attribute of the Call Activity. Assuming you would export both diagrams as BPMN 2.0 XML files and deploy them to the Camunda Engine, then the parent process would call its associated child process correctly.

In Cawemo, you can see all other process diagrams that would call the given (child) process. This information is visible above the documentation property field within the sidebar on the diagram page.

### Comments

When selecting an element of the BPMN diagram, a discussion can be attached to this element. If no element is selected, then the discussion will be attached to the diagram itself.

New comments can be added to the discussion. Afterwards, the comment can be edited or deleted via the context menu icon.

Existing discussions are highlighted within the diagram via additional icons.

In order to be allowed to add comments, the user needs the Editor or Commenter [access right](../projects#collaboration-access-rights).

#### Mentioning in Comments

By typing the '@' character, a list of users shows up and one user can be selected. When submitting the comment, this user will receive an email as a notification about the new comment.

### BPMN Diagram Actions

In the upper right corner of the diagram view, the following actions are available:

* Show milestone history
* Share
* Download or export
* Help

## DMN

Decision Model and Notation (DMN) is a standard for Business Decision Management. Further details can be read in our [Get started with Camunda and DMN tutorial](https://docs.camunda.org/get-started/dmn).

### Decision Tables and Literal Expressions

After adding a Decision to your DMN diagram its type can be specified to either Decision Table or Literal Expression. Both a Decision Table and Literal Expression can be opened for further editing by clicking on the icon within the decision shape. Please refer to the [Decision Modeling guide](https://docs.camunda.org/get-started/dmn/model) for further details.

### DMN Diagram Actions

In the upper right corner of the diagram view, the following actions are available:

* Show milestone history
* Share
* Download
* Help

## Import / Export

New versions of the diagram can be imported by dragging and dropping a BPMN or DMN XML file from the local file system onto the currently opened diagram. When this happens, new [milestones](../milestones) are created to save the previous and the new version of the diagram.

* BPMN diagrams can be exported as
  * PNG (raster image)
  * SVG (printable vector image)
  * BPMN 2.0 XML (executable process model)
* DMN diagrams can be exported as
  * DMN XML (executable decision model)

The XML files can be opened and used with other tools like the [Camunda Modeler](https://camunda.com/products/modeler).

The export options are available via the "Download or export" icon in the upper right corner.

## Sharing / Embedding

Diagrams can be shared with various people via a sharing link. This link can also be protected with an additional password.

Similar to the sharing link, a diagram can be included into HTML pages via an iframe tag. This tag can be copied from the sharing dialog via the embed button.

For wiki systems like [Confluence](https://www.atlassian.com/software/confluence), we recommend using the HTML macro and adding the iframe tag from the sharing dialog. This way, diagrams can be easily included in documentation pages. To adjust the dimensions of the diagram, the width and height values of the iframe tag can be modified.
