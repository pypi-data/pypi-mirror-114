# limsmock 

Clarity LIMS system mainly consist of a postgress database, a REST API and a web interface. 

The REST API is the fundamental data access interface using XML over HTTP. Its data structure looks as below.

```
<ri:index xmlns:ri="http://genologics.com/ri">
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/artifactgroups" rel="artifactgroups"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/artifacts" rel="artifacts"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/configuration/automations" rel="configuration/automations"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/configuration/protocols" rel="protocols"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/configuration/udfs" rel="udfs"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/configuration/udts" rel="udts"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/configuration/workflows" rel="workflows"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/containers" rel="containers"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/containertypes" rel="containertypes"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/controltypes" rel="controltypes"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/files" rel="files"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/instruments" rel="instruments"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/labs" rel="labs"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/permissions" rel="permissions"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/processes" rel="processes"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/processtemplates" rel="processtemplates"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/processtypes" rel="processtypes"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/projects" rel="projects"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/reagentkits" rel="reagentkits"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/reagentlots" rel="reagentlots"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/reagenttypes" rel="reagenttypes"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/researchers" rel="researchers"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/roles" rel="roles"/>
<link uri="https://clinical-lims-stage.scilifelab.se/api/v2/samples" rel="samples"/>
</ri:index>
```

This package serves as a LIMS REST API mock for testing purposes.

Some examples of how it can be used can be fount in tests directory.

