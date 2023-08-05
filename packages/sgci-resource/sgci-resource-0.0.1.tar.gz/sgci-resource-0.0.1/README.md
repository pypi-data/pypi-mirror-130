# Floatview Stats

<table>
    <tr>
        <td>Latest Release</td>
        <td>
            <a href="https://pypi.org/project/sgci_resource/"/>
            <img src="https://badge.fury.io/py/sgci_resource.svg"/>
        </td>
    </tr>
    <tr>
        <td>PyPI Downloads</td>
        <td>
            <a href="https://pepy.tech/project/sgci_resource"/>
            <img src="https://pepy.tech/badge/sgci_resource/month"/>
        </td>
    </tr>
</table>

#Introduction to SCGI Inventory


## Version
This is version 1.0.0 of the SGCI Resource Description Specification schema. This work is released under an Apache 2.0
`license <https://raw.githubusercontent.com/SGCI/sgci-resource-inventory/master/LICENSE>`_ .

## Introduction

The user-facing components of the Cyberinfrastructure (CI) ecosystem, science gateways and scientific workflow systems,
share a common need of interfacing with physical resources (storage systems and execution environments) to manage data and execute codes (applications).

However, there is no uniform, platform-independent way to describe either the resources or the applications. To address this, we propose uniform semantics for describing resources and applications that will be relevant to a diverse set of stakeholders.

The SGCI Resource Description Specification provides a standard way for institutions and service providers to describe storage and computing infrastructure broadly available to the research computing and science gateway community. SGCI Resource descriptions provide a foundation for interoperability across gateway components and other cyberinfrastructure software.

The current, initial version of the resource description language focuses on “traditional” HPC and high-throughput storage and computing resources

## Installation


```bash
pip install sgci-resource
```


## Usage



```python

from sgci_resource import core
gh = core.SCGICatalogXsede() 
#gh = core.SCGICatalogLocal(folder="REPO_PATH")
#gh = core.SCGICatalogGithub(token="GITHUB_TOKEN")



#print available resources
l = gh.listResources()
print(l)


# Print json description
resource = gh.getResource('RESOURCE.IDENTIFICATION.KEY') # e.g. stampede2.tacc.xsede
print(resource)

# Print json description
namehost = gh.searchPath("[name, host]", resource)
print(namehost)

```

#Integration

![Integration projects](https://raw.githubusercontent.com/SGCI/sgci-resource-inventory/master/docs/SGCI.png)


The SCGI Inventory is currently been integrated with Airavata, HUBzero |reg|  , and Tapis. We expect the inventory to be adapted by others soon.

**Links:**

https://github.com/SGCI/sgci-resource-inventory

https://github.com/SGCI/sgci-resource-inventory-cache-service


**Get Involved!**

Issues, Comments, PRs all welcome!

SGCI: help@sciencegateways.org

Email: jstubbs at tacc.utexas.edu, smarru at iu.edu, dmejiapa at purdue.edu