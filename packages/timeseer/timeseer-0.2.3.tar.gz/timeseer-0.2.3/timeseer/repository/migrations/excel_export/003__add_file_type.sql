-- depends: 002__add_export_details

alter table ExcelExport add column type text default 'excel';

