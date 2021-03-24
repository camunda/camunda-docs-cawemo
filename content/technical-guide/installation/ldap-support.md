---
title: 'LDAP Support'
weight: 60

menu:
  main:
    identifier: 'technical-guide-ldap-support'
    parent: 'installation'
---

The Camunda Account LDAP integration enables users with an account on your organization's LDAP server to log in to Cawemo without signing up first.
  
# Configuration Options

In order to activate the LDAP integration, you must configure the required of the following environment variables in
 [step 3 of the on-premise installation]({{< ref "_index.md#3-create-an-env-file">}}):

<table class="table table-striped">
 <tr>
   <th>Environment Variable</th>
   <th>Example Value</th>
   <th>Description</th>
   <th>Active Directory</th>
   <th>Other LDAP Server</th>
 </tr>
  <tr>
    <td>IAM_LDAP_SERVER_URL</td>
    <td>ldaps://ldap.example.com/</td>
    <td>URL at which the LDAP server can be reached</td>
    <td>Required</td>
    <td>Required</td>
  </tr>  
  <tr>
    <td>IAM_LDAP_DOMAIN</td>
    <td>camunda.org</td>
    <td>Domain of an Active Directory LDAP Server</td>
    <td>Required</td>
    <td>Not allowed</td>
 </tr>
 <tr>
    <td>IAM_LDAP_MANAGER_DN</td>
    <td>cn=admin,dc=camunda,dc=org</td>
    <td>Dn (Distinguished name) to bind to the LDAP server</td>
    <td>Not allowed</td>
    <td>Required</td>
 </tr>
 <tr>
    <td>IAM_LDAP_MANAGER_PASSWORD</td>
    <td>myPassword123</td>
    <td>Password to bind to the LDAP server</td>
    <td>Not allowed</td>
    <td>Required</td>
 </tr>
 <tr>
   <td>IAM_LDAP_BASE_DN</td>
   <td>dc=camunda,dc=org</td>
   <td>Start location for LDAP search (for AD: derive from IAM_LDAP_DOMAIN)</td>
   <td>Required</td>
   <td>Required</td>
 </tr>
 <tr>
   <td>IAM_LDAP_USER_SEARCH_BASE</td>
   <td>ou=berlin</td>
   <td>Start location for user search; relative to IAM_LDAP_BASE_DN</td>
   <td>Optional</td>
   <td>Optional</td>
 </tr>
 <tr>
   <td>IAM_LDAP_USER_SEARCH_FILTER</td>
   <td>(&(objectClass=inetOrgPerson)(employeeType=engineer))</td>
   <td>Filter to restrict the group of users to search in</td>
   <td>Optional</td>
   <td>Optional</td>
 </tr>
 <tr>
   <td>IAM_LDAP_UUID_ATTRIBUTE</td>
   <td>entryUUID</td>
   <td>Name of the attribute containing the UUID of the user (for AD: objectGUID)</td>
   <td>Required</td>
   <td>Required</td>
 </tr> 
 <tr>
   <td>IAM_LDAP_USER_NAME_ATTRIBUTES</td>
   <td>firstName,lastName</td>
   <td>Name(s) of the attribute(s) containing the user name; multiple names separated by a comma</td>
   <td>Required</td>
   <td>Required</td>
 </tr>
 <tr>
   <td>IAM_LDAP_USER_EMAIL_ATTRIBUTE</td>
   <td>mail</td>
   <td>Name of the attribute containing the user's email</td>
   <td>Required</td>
   <td>Required</td>
 </tr>
</table>

# Migration of Existing User Accounts

Please back up the Camunda Account and Cawemo databases before you migrate to LDAP as we do not offer a 
mechanism for reversing the account migration.

Users that are already registered in Cawemo through Camunda Account can keep using their accounts with LDAP enabled. 
Each account is matched automatically on the user's first login after LDAP is configured by your organization. 
For this to work, the email addresses used for the Camunda Account and saved on the LDAP server must match. 
After migrating an existing account, it can only be accessed with the user's LDAP credentials.
  
The diagrams a user has previously created in Cawemo will still be associated to their account after the migration.
Their personal data is updated in Camunda Account and Cawemo with the data from the LDAP server on the first login.

# Handling of User Data

Camunda Account retrieves the user's name from your LDAP server on each login and saves/updates it in the Camunda Account
 and Cawemo databases, so it can be displayed in the applications.
We do not read or save the user's password, instead the password comparison is performed by the LDAP server.
