import uuid

from dv_data_generator.builders.dv_request_builder import DvEntityStatusTypes, DvRequestBuilder, DvRequestTypes
from dv_data_generator.builders.dv_report_builder import DvReportBuilder


class DvDataDirector:
    def __init__(self, credentials=None, token=None, service_account=False, debug=False, api_host=None):
        self._credentials = credentials
        self._token = token
        self._service_account = service_account
        self._debug = debug
        self._api_host = api_host

    def billable_outcome_report(self, **kwargs) -> DvReportBuilder:
        dimensions = [
            "FILTER_ADVERTISER",
            "FILTER_LINE_ITEM_TYPE",
            "FILTER_INVENTORY_COMMITMENT_TYPE",
            "FILTER_ADVERTISER_CURRENCY",
            "FILTER_LINE_ITEM_NAME",
            "FILTER_LINE_ITEM",
            "FILTER_BILLABLE_OUTCOME",
            "FILTER_PARTNER",
        ]

        metrics = ["METRIC_IMPRESSIONS"]

        title = f"billable_outcome_{uuid.uuid4()}"

        builder = (
            DvReportBuilder(credentials=self._credentials,
                            token=self._token, service_account=self._service_account, debug=self._debug, api_host=self._api_host, **kwargs)
            .set_title(title)
            .set_dimensions(dimensions)
            .set_metrics(metrics)
        )

        return builder

    def platform_fee_report(self, **kwargs) -> DvReportBuilder:
        dimensions = [
            "FILTER_ADVERTISER",
            "FILTER_LINE_ITEM_TYPE",
            "FILTER_INVENTORY_COMMITMENT_TYPE",
            "FILTER_ADVERTISER_CURRENCY",
            "FILTER_LINE_ITEM_NAME",
            "FILTER_LINE_ITEM",
            "FILTER_PARTNER",
        ]

        metrics = ["METRIC_PLATFORM_FEE_RATE", "METRIC_IMPRESSIONS"]

        title = f"platform_fee_{uuid.uuid4()}"

        builder = (
            DvReportBuilder(credentials=self._credentials,
                            token=self._token, service_account=self._service_account, debug=self._debug,  api_host=self._api_host, **kwargs)
            .set_title(title)
            .set_dimensions(dimensions)
            .set_metrics(metrics)
        )

        return builder

    def spend_report(self, **kwargs) -> DvReportBuilder:
        dimensions = [
            "FILTER_DATE",
            "FILTER_PARTNER",
            "FILTER_ADVERTISER",
            "FILTER_ADVERTISER_CURRENCY",
        ]

        metrics = [
            "METRIC_MEDIA_COST_ADVERTISER",
            "METRIC_TOTAL_MEDIA_COST_ADVERTISER",
            "METRIC_CPM_FEE1_ADVERTISER",
            "METRIC_CPM_FEE2_ADVERTISER",
            "METRIC_MEDIA_FEE2_ADVERTISER",
            "METRIC_MEDIA_FEE3_ADVERTISER",
            "METRIC_PLATFORM_FEE_ADVERTISER",
            "METRIC_PLATFORM_FEE_RATE",
            "METRIC_REVENUE_ADVERTISER",
            "METRIC_MEDIA_FEE1_ADVERTISER",
            "METRIC_PROFIT_ADVERTISER",
            "METRIC_DATA_COST_ADVERTISER",
            "METRIC_CPM_FEE3_ADVERTISER",
            "METRIC_CPM_FEE4_ADVERTISER",
            "METRIC_CPM_FEE5_ADVERTISER",
            "METRIC_MEDIA_FEE4_ADVERTISER",
            "METRIC_MEDIA_FEE5_ADVERTISER",
            "METRIC_FEE22_ADVERTISER",
            "METRIC_FEE13_ADVERTISER",
            "METRIC_FEE12_ADVERTISER",
        ]

        title = f"spend_{uuid.uuid4()}"

        builder = (
            DvReportBuilder(credentials=self._credentials,
                            token=self._token, service_account=self._service_account, debug=self._debug,  api_host=self._api_host,**kwargs)
            .set_title(title)
            .set_dimensions(dimensions)
            .set_metrics(metrics)
        )

        return builder

    def advertisers_report(self, **kwargs) -> DvReportBuilder:
        dimensions = [
            "FILTER_PARTNER_NAME",
            "FILTER_PARTNER",
            "FILTER_ADVERTISER_NAME",
            "FILTER_ADVERTISER",
            "FILTER_LINE_ITEM_NAME",
            "FILTER_LINE_ITEM",
            "FILTER_ADVERTISER_CURRENCY",
        ]

        metrics = ["METRIC_TOTAL_MEDIA_COST_ADVERTISER"]

        title = f"advertisers_{uuid.uuid4()}"

        builder = (
            DvReportBuilder(credentials=self._credentials,
                            token=self._token, service_account=self._service_account, debug=self._debug,  api_host=self._api_host, **kwargs)
            .set_title(title)
            .set_dimensions(dimensions)
            .set_metrics(metrics)
        )

        return builder

    def partner_list(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_PARTNERS
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug, api_host=self._api_host, **kwargs)
            .set_request_type(request_type)
        )
        return builder

    def partner_list_of_ids(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_PARTNER_IDS
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug, api_host=self._api_host, **kwargs)
            .set_request_type(request_type)
        )
        return builder

    def advertiser_list(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_ADVERTISER
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug,  api_host=self._api_host,**kwargs)
            .set_request_type(request_type)
        )
        return builder

    def advertiser_list_of_ids(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_ADVERTISER_IDS
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug, api_host=self._api_host, **kwargs)
            .set_request_type(request_type)
        )
        return builder

    def active_lineitem_list(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_LINEITEM
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug, api_host=self._api_host, **kwargs)
            .set_request_type(request_type)
        )
        return builder

    def paused_lineitem_list(self, **kwargs) -> DvRequestBuilder:
        request_type = DvRequestTypes.LIST_LINEITEM
        builder = (
            DvRequestBuilder(credentials=self._credentials,
                             token=self._token, service_account=self._service_account, debug=self._debug,  api_host=self._api_host,**kwargs)
            .set_request_type(request_type)
            .set_entity_status(DvEntityStatusTypes.PAUSED)
        )
        return builder
