# Prepared Azure quota support request

Status: draft; not sent. Owner: Dr. Moore. Prepared 2026-10-11.

Subject: Enable two standard Bsv2-family vCPUs in East US 2 for a single-node reference demo

Subscription: `b31e9bd1-6179-4504-819b-f212ed36f609`.
Resource group: `rg-pulse-reference`.
Requested limit: **2** dedicated vCPUs for `standardBsv2Family` in `eastus2`, sufficient for one non-zonal `Standard_B2ls_v2`.

The subscription has 10 regional vCPUs available but this family has a zero limit. The CLI quota request returned `ContactSupport`, request ID `a8d93a07-0d4b-4071-a9a1-0c3979c21178`. Please confirm whether this offer is eligible and enable the requested two vCPUs, or identify an eligible equivalent region/SKU. Do not upgrade the subscription offer or enroll any paid support plan without the owner's decision.

An alternative two-vCPU request for `standardBasv2Family` in `centralus` failed with `QuotaNotAvailableForResource`, request ID `6d185545-3a32-49ad-b869-c336a41dff29`. The workload is an isolated Linux/K3s bearing-assessment reference demo with a USD 50 monthly ceiling; production capacity is not claimed. No paid VM has been created.

Submitting this draft requires an authorized support contact and explicit permission to send the external support request. The application build and local validation can continue independently.
